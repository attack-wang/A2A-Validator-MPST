import unittest

from a2a.types import Message, Part, Role, TextPart
from google.adk.events.event import Event as ADKEvent
from google.genai import types
from host_agent import HostAgent
from mpst_ext import MPSTValidator
from types import SimpleNamespace

from service.server.adk_host_manager import ADKHostManager
from service.types import Conversation


class _FakeSessionService:
    async def get_session(self, **_kwargs):
        return object()

    async def append_event(self, _session, _event):
        return None


class _FakeRunner:
    def __init__(self, runs):
        self._runs = runs
        self.calls = []

    async def run_async(self, *, new_message, **_kwargs):
        self.calls.append(new_message)
        run = self._runs[len(self.calls) - 1]
        for event in run:
            yield event


def _model_event(parts):
    return ADKEvent(
        author='host_agent',
        invocation_id=ADKEvent.new_id(),
        content=types.Content(role='model', parts=parts),
    )


def _manager_with_runs(runs):
    manager = object.__new__(ADKHostManager)
    manager._pending_message_ids = []
    manager._messages = []
    manager._events = {}
    manager._conversations = [
        Conversation(conversation_id='conversation-1', is_active=True)
    ]
    manager._session_service = _FakeSessionService()
    manager._host_runner = _FakeRunner(runs)
    manager.validation_enabled = True
    manager.user_id = 'test_user'
    manager.app_name = 'A2A'
    return manager


def _user_message():
    return Message(
        role=Role.user,
        parts=[Part(root=TextPart(text='run the workflow'))],
        message_id='message-1',
        context_id='conversation-1',
    )


class EmptyResponseRecoveryTest(unittest.IsolatedAsyncioTestCase):
    def test_resolves_protocol_role_alias_to_registered_agent(self):
        host = object.__new__(HostAgent)
        host.remote_agent_connections = {
            'Transport Select Agent': object(),
            'Public Transport Agent': object(),
        }

        self.assertEqual(
            'Transport Select Agent',
            host._resolve_agent_name('Transportselectagent'),
        )
        self.assertEqual(
            'Public Transport Agent',
            host._resolve_agent_name('Publictransportagent'),
        )

    def test_empty_and_empty_code_fence_are_not_visible(self):
        self.assertFalse(ADKHostManager._text_has_visible_content(''))
        self.assertFalse(
            ADKHostManager._text_has_visible_content('```json\n\n```')
        )
        self.assertTrue(ADKHostManager._text_has_visible_content('done'))

    def test_detects_textual_tool_call_payload(self):
        leaked = (
            'Tool Calls: [{"type":"function","function":'
            '{"name":"send_message","arguments":{"agent_name":"OP3"}}}]'
        )
        self.assertTrue(MPSTValidator.contains_tool_call_payload(leaked))
        validator = MPSTValidator()
        self.assertTrue(
            validator.set_protocol(
                'Host?number . Host!result . 0',
                'Agent',
            )
        )
        result = validator.validate_tool_call_completion(leaked)
        self.assertFalse(result['is_valid'])
        self.assertEqual(result['code'], 'ToolCallIncomplete')
        self.assertFalse(
            MPSTValidator.contains_tool_call_payload(
                'The workflow completed without exposing tool calls.'
            )
        )

    async def test_retries_empty_response_at_start(self):
        manager = _manager_with_runs(
            [
                [_model_event([])],
                [_model_event([types.Part.from_text(text='workflow done')])],
            ]
        )

        await manager.process_message(_user_message())

        self.assertEqual(len(manager._host_runner.calls), 2)
        self.assertIn(
            'Continue from the current session',
            manager._host_runner.calls[1].parts[0].text,
        )
        conversation = manager._conversations[0]
        self.assertEqual(len(conversation.messages), 2)
        self.assertEqual(
            conversation.messages[-1].parts[0].root.text,
            'workflow done',
        )
        self.assertFalse(manager._pending_message_ids)
        self.assertTrue(
            all(event.content.parts for event in manager._events.values())
        )

    async def test_retries_empty_response_after_tool_chain(self):
        tool_call = types.Part(
            function_call=types.FunctionCall(
                name='send_message',
                args={
                    'agent_name': 'Defense Strategy Agent',
                    'message': '[number: CVE-2026-9001]',
                },
            )
        )
        tool_response = types.Part(
            function_response=types.FunctionResponse(
                name='send_message',
                response={'result': ['[result: Drop_Payload_Signature_v1.sh]']},
            )
        )
        manager = _manager_with_runs(
            [
                [
                    _model_event([tool_call]),
                    _model_event([tool_response]),
                    _model_event([]),
                ],
                [
                    _model_event(
                        [types.Part.from_text(text='finalized workflow')]
                    )
                ],
            ]
        )

        await manager.process_message(_user_message())

        self.assertEqual(len(manager._host_runner.calls), 2)
        conversation = manager._conversations[0]
        self.assertEqual(
            conversation.messages[-1].parts[0].root.text,
            'finalized workflow',
        )
        event_texts = [
            part.root.text
            for event in manager._events.values()
            for part in event.content.parts
            if part.root.kind == 'text'
        ]
        self.assertIn(
            '[result: Drop_Payload_Signature_v1.sh]',
            event_texts,
        )
        self.assertFalse(manager._pending_message_ids)

    async def test_rejects_textual_tool_call_and_retries(self):
        leaked = (
            'Tool Calls: [{"id":"call-1","type":"function","function":'
            '{"name":"send_message","arguments":{"agent_name":'
            '"Defense Strategy Agent","message":"[number: CVE-2026-9001]"}}}]'
        )
        manager = _manager_with_runs(
            [
                [_model_event([types.Part.from_text(text=leaked)])],
                [
                    _model_event(
                        [types.Part.from_text(text='final user answer')]
                    )
                ],
            ]
        )

        with self.assertLogs('host.validation', level='ERROR') as captured:
            await manager.process_message(_user_message())

        self.assertEqual(len(manager._host_runner.calls), 2)
        host_log = '\n'.join(captured.output)
        self.assertIn('[HOST VALIDATION ERROR]', host_log)
        self.assertIn('Stage: host_final_output', host_log)
        self.assertIn('Code: ToolCallIncomplete', host_log)
        self.assertIn('Action: rejected_and_retrying', host_log)
        self.assertIn(
            'exposed a tool call',
            manager._host_runner.calls[1].parts[0].text,
        )
        response = manager._conversations[0].messages[-1]
        self.assertEqual(response.parts[0].root.text, 'final user answer')
        self.assertNotIn(
            leaked,
            [
                part.root.text
                for message in manager._conversations[0].messages
                for part in message.parts
                if part.root.kind == 'text'
            ],
        )

    async def test_disabled_ui_passes_tool_call_through_without_retry(self):
        leaked = (
            'Tool Calls: [{"type":"function","function":'
            '{"name":"send_message","arguments":{"agent_name":"OP3"}}}]'
        )
        manager = _manager_with_runs(
            [[_model_event([types.Part.from_text(text=leaked)])]]
        )
        manager.validation_enabled = False

        await manager.process_message(_user_message())

        self.assertEqual(1, len(manager._host_runner.calls))
        response = manager._conversations[0].messages[-1]
        self.assertEqual(leaked, response.parts[0].root.text)
        self.assertFalse(manager._pending_message_ids)

    async def test_disabled_host_sends_and_returns_raw_message(self):
        leaked = (
            'Tool Calls: [{"type":"function","function":'
            '{"name":"lookup_attack_cve","arguments":{}}}]'
        )

        class FakeConnection:
            def __init__(self):
                self.messages = []

            async def send_message(self, message):
                self.messages.append(message)
                return Message(
                    role=Role.agent,
                    parts=[Part(root=TextPart(text=leaked))],
                    message_id='remote-response',
                    context_id=message.context_id,
                )

        connection = FakeConnection()
        host = object.__new__(HostAgent)
        host.validation_enabled = False
        host.remote_agent_connections = {
            'IP Intelligence Agent': connection
        }
        host._protocol_initialized_agents = set()
        tool_context = SimpleNamespace(
            state={'context_id': 'baseline-session'},
            actions=SimpleNamespace(),
        )

        result = await host.send_message(
            'IP Intelligence Agent',
            '203.0.113.10',
            tool_context,
        )

        self.assertEqual(['203.0.113.10'], [
            connection.messages[0].parts[0].root.text
        ])
        self.assertEqual([leaked], result)
        self.assertNotIn(
            '_mpst_initialized_agents',
            tool_context.state,
        )
        self.assertNotIn('_mpst_session_id', tool_context.state)

    async def test_returns_visible_error_after_retry_limit(self):
        manager = _manager_with_runs(
            [
                [_model_event([])],
                [_model_event([])],
                [_model_event([])],
            ]
        )

        await manager.process_message(_user_message())

        self.assertEqual(len(manager._host_runner.calls), 3)
        response = manager._conversations[0].messages[-1]
        self.assertTrue(response.parts)
        self.assertIn('自动重试', response.parts[0].root.text)
        self.assertFalse(manager._pending_message_ids)


if __name__ == '__main__':
    unittest.main()
