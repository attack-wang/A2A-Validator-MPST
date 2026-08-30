import logging
import os
import click
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from dotenv import load_dotenv

# 导入操作1相关的类
from agent import Op1Agent
from agent_executor import Op1AgentExecutor

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=10399)  # 操作1 Agent 默认使用 10399 端口
def main(host, port):
    try:
        capabilities = AgentCapabilities(
            streaming=True,
            extensions=[],
        )

        # 定义通用业务能力：IP 情报查询节点
        op1_skill = AgentSkill(
            id='ip_intelligence',
            name='IP Intelligence Service',
            description='接受一个攻击源 IP，返回该 IP 所属的恶意黑客组织/僵尸网络标签。'
                        '返回值可作为不透明 key 传递给下游武器库资产智能体。',
            tags=['ip', 'threat-intel', 'lookup', 'opaque-key'],
            examples=['203.0.113.10', 'check 198.51.100.20']
        )

        # 定义通用 Agent 名片
        agent_card = AgentCard(
            name='IP Intelligence Agent',
            description='IP 情报节点：接受攻击源 IP 并返回其所属的恶意黑客组织/僵尸网络标签。'
                        '将结果视为不透明 key。',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            default_input_modes=Op1Agent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=Op1Agent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[op1_skill],
        )

        agent_executor = Op1AgentExecutor()

        request_handler = DefaultRequestHandler(
            agent_executor=agent_executor,
            task_store=InMemoryTaskStore(),
        )

        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        logger.info(f"Starting IP Intelligence Agent on {host}:{port}")
        uvicorn.run(server.build(), host=host, port=port)

    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        exit(1)


if __name__ == '__main__':
    main()
