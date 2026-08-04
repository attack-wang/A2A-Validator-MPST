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
from agent import Op2Agent

# 导入 MPST 验证扩展
from mpst_ext import MPSTValidatingExecutor


logger = logging.getLogger(__name__)


class Op2AgentExecutor(MPSTValidatingExecutor):
    """支持 MPST 验证的武器库资产 AgentExecutor。

    继承自 MPSTValidatingExecutor，
    支持接收 MPST 局部协议并进行运行时验证。
    """

    def __init__(self):
        MPSTValidatingExecutor.__init__(self, delegate=None, role_name="OP2")
        self.agent = Op2Agent()
        self._delegate = self
        self.role_name = 'OP2'
        logger.info('Op2AgentExecutor (Weapon Library lookup) initialized with MPST validation support')


