"""Compile inline contract references without changing the legacy GT grammar.

Distinct contract policies survive subset erasure and classical projection.
The symbols are decoded onto runtime transitions, never sent as wire labels.
"""
from contextlib import contextmanager
import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory

_INTERACTION = re.compile(
    r'(?P<sender>[A-Z][A-Za-z0-9]*)\s*->\s*'
    r'(?P<receiver>[A-Z][A-Za-z0-9]*)\s*:\s*'
    r'(?P<label>[a-z][A-Za-z0-9]*)'
    r'(?:\s*\(\s*(?P<schema>[A-Za-z][A-Za-z0-9_]*)\s*\))?'
    r'(?:\s*@contract\s*\(\s*(?P<reference>"(?:[^"\\]|\\.)*")\s*\))?\s*\.'
)
_RESERVED = re.compile(r'\bmpstcontract[0-9]+\b', re.I)


def compile_annotations(text):
    # Comments cannot introduce executable references or affect ordinal IDs.
    clean = re.sub(r'//[^\r\n]*', '', text)
    if _RESERVED.search(clean):
        raise ValueError('Reserved interaction symbol mpstcontract... in protocol')
    bindings = {}
    policies = {}
    ordinal = 0

    def replace(match):
        nonlocal ordinal
        ordinal += 1
        reference = json.loads(match['reference']) if match['reference'] else None
        if reference is not None and not re.fullmatch(r'[A-Za-z][A-Za-z0-9_.-]*', reference):
            raise ValueError('Invalid contract reference')
        if reference is None and match['schema'] is None:
            return match.group(0)
        policy = (match['sender'], match['receiver'], match['label'], reference, match['schema'])
        if policy in policies:
            symbol = policies[policy]
            bindings[symbol]['interaction_ids'].append(f'interaction-{ordinal:06d}')
            return f"{match['sender']} -> {match['receiver']} : {symbol}."
        symbol = f'mpstcontract{ordinal:06d}'
        policies[policy] = symbol
        bindings[symbol] = {
            'interaction_id': f'interaction-{ordinal:06d}',
            'interaction_ids': [f'interaction-{ordinal:06d}'],
            'sender': match['sender'], 'receiver': match['receiver'],
            'label': match['label'], 'contract_ref': reference,
            'payload_schema': match['schema'],
        }
        return f"{match['sender']} -> {match['receiver']} : {symbol}."

    compiled = _INTERACTION.sub(replace, clean)
    if '@' in compiled:
        raise ValueError('Malformed or unsupported @contract annotation')
    # A payload declaration that was not consumed must not reach ANTLR as a
    # partially parsed protocol (its generated parser reports some errors only).
    if re.search(r'->\s*\w+\s*:\s*\w+\s*\(', compiled):
        raise ValueError('Malformed payload schema declaration')
    return compiled, bindings


@contextmanager
def projection_input(path):
    path = Path(path)
    text, bindings = compile_annotations(path.read_text(encoding='utf-8'))
    if not bindings:
        yield str(path), bindings
        return
    with TemporaryDirectory(prefix='mpst-contract-projection-') as directory:
        prepared = Path(directory) / path.name
        prepared.write_text(text, encoding='utf-8')
        type_path = path.with_suffix('.type.json')
        if type_path.exists():
            types = json.loads(type_path.read_text(encoding='utf-8'))
            for symbol, binding in bindings.items():
                if binding['label'] in types:
                    types[symbol] = types[binding['label']]
            prepared.with_suffix('.type.json').write_text(json.dumps(types), encoding='utf-8')
        yield str(prepared), bindings


def display_projection(text, bindings):
    for symbol, binding in bindings.items():
        suffix = f"({binding['payload_schema']})" if binding['payload_schema'] else ''
        if binding['contract_ref']:
            suffix += f" @contract({json.dumps(binding['contract_ref'])})"
        text = re.sub(r'\b' + re.escape(symbol) + r'\b', binding['label'] + suffix, text)
    return text


def bind_projected_transitions(protocol, bindings, role):
    """Restore public labels and attach metadata to each compiled FSM edge."""
    for state in protocol.states.values():
        for transition in state.transitions:
            binding = bindings.get(transition.label)
            if binding is None:
                continue
            sending = transition.action.value == 'send'
            expected_role = binding['sender'] if sending else binding['receiver']
            peer = binding['receiver'] if sending else binding['sender']
            if role != expected_role or transition.peer != peer:
                raise ValueError('Projected contract reference attached to the wrong role/peer')
            transition.label = binding['label'].lower()
            transition.contract_ref = binding['contract_ref']
            transition.interaction_id = binding['interaction_id']
            transition.interaction_ids = tuple(binding['interaction_ids'])
            transition.payload_schema = binding['payload_schema']
