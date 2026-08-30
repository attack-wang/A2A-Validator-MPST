import logging
import os
import click
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from dotenv import load_dotenv

# 导入操作3相关的类
from agent import Op3Agent
from agent_executor import Op3AgentExecutor

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=10303)  # 操作3 Agent 默认使用 10303 端口
def main(host, port):
    try:
        capabilities = AgentCapabilities(
            streaming=True,
            extensions=[],
        )

        # 定义通用业务能力：防御策略查询节点
        op3_skill = AgentSkill(
            id='defense_strategy',
            name='Defense Strategy Service',
            description='接受一个漏洞编号(CVE ID)，返回防火墙/安全拦截系统应自动下发的安全补丁/策略规则脚本。'
                        '该返回值即最终交付给用户的结果。',
            tags=['defense', 'firewall-rule', 'cve', 'lookup'],
            examples=['CVE-2026-9999', 'CVE-2026-9001']
        )

        # 定义通用 Agent 名片
        agent_card = AgentCard(
            name='Defense Strategy Agent',
            description='防御策略节点：接受 CVE 编号并返回应自动下发的安全补丁/策略规则脚本。'
                        '该节点为链路终点，结果直接交付用户。',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            default_input_modes=Op3Agent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=Op3Agent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[op3_skill],
        )

        agent_executor = Op3AgentExecutor()

        request_handler = DefaultRequestHandler(
            agent_executor=agent_executor,
            task_store=InMemoryTaskStore(),
        )

        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        logger.info(f"Starting Defense Strategy Agent on {host}:{port}")
        uvicorn.run(server.build(), host=host, port=port)

    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        exit(1)


if __name__ == '__main__':
    main()
