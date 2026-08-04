import json
import logging

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    DataPart,
    Message,
    Part,
    Role,
    Task,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_agent_parts_message,
    new_agent_text_message,
    new_task,
)
from a2a.utils.errors import ServerError
from agent import Op1Agent

# 导入 MPST 验证扩展
from mpst_ext import MPSTValidatingExecutor


logger = logging.getLogger(__name__)


class Op1AgentExecutor(MPSTValidatingExecutor):
    """支持 MPST 验证的 IP 情报 AgentExecutor。

    继承自 MPSTValidatingExecutor，
    支持接收 MPST 局部协议并进行运行时验证。
    """

    def __init__(self):
        MPSTValidatingExecutor.__init__(self, delegate=None, role_name="OP1")
        self.agent = Op1Agent()
        self._delegate = self
        self.role_name = 'OP1'
        logger.info('Op1AgentExecutor (IP Intelligence lookup) initialized with MPST validation support')


