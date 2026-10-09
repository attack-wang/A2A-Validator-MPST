"""Export readable local types and executable transitions with references."""
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'integrations/ChatDev1.0')]
os.environ.update(CHATDEV_CONTENT_ENABLED='true', MPST_A2A_ROOT=str(ROOT))
from chatdev.mpst_global import GlobalPilotMonitor
from gt_projection import GTProjection

monitor = GlobalPilotMonitor().monitor
protocol = ROOT / 'integrations/ChatDev1.0/protocol/mpst_content.gt'
roles = {}
for role, validator in monitor.validators.items():
    projected = GTProjection().project_protocol(str(protocol), 'mpst_content', role)
    if projected['error']:
        raise RuntimeError(projected['error'])
    roles[role] = {'readable_local_protocol': projected['display_local_protocol'],
                   'contract_bindings': projected['contract_bindings'],
                   'states': {name: state.to_dict() for name, state in validator.protocol.states.items()}}
output = ROOT / 'output/projected-contracts.json'
output.parent.mkdir(exist_ok=True)
output.write_text(json.dumps({'global_type': str(protocol), 'registry': str(ROOT / 'chatdev-contracts.json'),
                              'roles': roles}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'output': str(output), 'roles': len(roles),
                  'distinct_contracts': len({b['contract_ref'] for b in monitor.contract_bindings.values()})}))
