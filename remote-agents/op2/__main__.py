import logging
import os
import click
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from dotenv import load_dotenv

# 导入操作2相关的类
from agent import Op2Agent
from agent_executor import Op2AgentExecutor

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=10302)  # 操作2 Agent 默认使用 10302 端口
def main(host, port):
    try:
        capabilities = AgentCapabilities(
            streaming=True,
            extensions=[],
        )

        # 定义通用业务能力：武器库资产查询节点
        op2_skill = AgentSkill(
            id='weapon_library',
            name='Weapon Library Asset Service',
            description='接受一个黑客组织/僵尸网络标签，返回该组织近期最常利用的漏洞编号(CVE ID)。'
                        '返回值可作为不透明 key 传递给下游防御策略智能体。',
            tags=['weapon-library', 'cve', 'lookup', 'opaque-key'],
            examples=['Advanced-Threat-Group-X', 'Advanced-Threat-Group-A']
        )

        # 定义通用 Agent 名片
        agent_card = AgentCard(
            name='Weapon Library Asset Agent',
            description='武器库资产节点：接受黑客组织标签并返回其最常利用的 CVE 编号。'
                        '将结果视为不透明 key。',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            default_input_modes=Op2Agent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=Op2Agent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[op2_skill],
        )

        agent_executor = Op2AgentExecutor()

        request_handler = DefaultRequestHandler(
            agent_executor=agent_executor,
            task_store=InMemoryTaskStore(),
        )

        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        logger.info(f"Starting Weapon Library Asset Agent on {host}:{port}")
        uvicorn.run(server.build(), host=host, port=port)

    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        exit(1)


if __name__ == '__main__':
    main()
