import logging
import os

import click

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent import TransportSelectAgent
from agent_executor import TransportSelectAgentExecutor
from dotenv import load_dotenv
from timestamp_ext import TimestampExtension


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


@click.command()
@click.option('--host', default='localhost')
@click.option('--port', default=10404)
def main(host, port):
    try:
        hello_ext = TimestampExtension()
        capabilities = AgentCapabilities(
            streaming=True,
            extensions=[
                hello_ext.agent_extension(),
            ],
        )
        # Agent Skill for Warehouse
        warehouse_skill = AgentSkill(
            id='transport_select',
            name='Inter-city Transport Selector',
            description='根据用户提供的日期、出发地、目的地及天气，推荐跨城出行选择飞机还是火车。只能处理飞机/火车的选择决策，不涉及具体航班/车次查询、酒店、天气等其他领域。',
            tags=['transport', 'flight', 'train', 'select', 'recommend'],
            examples=[
                '7月1日想从武汉去北京旅游，天气怎么样，坐飞机还是火车好？',
                '带老人从上海到西安，推荐飞机还是高铁？'
            ]
        )
        # Agent Card for Transport Select
        agent_card = AgentCard(
            name='Transport Select Agent',
            description='专门推荐跨城出行选择飞机还是火车。范围仅限飞机/火车的选择建议，其他问题会拒绝。',
            url=f'http://{host}:{port}/',  # Assuming separate ports for remote agents
            version='1.0.0',
            default_input_modes=TransportSelectAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=TransportSelectAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[warehouse_skill],
        )
        agent_executor = TransportSelectAgentExecutor()
        # Use the decorator version of the extension for highest ease of use.
        agent_executor = hello_ext.wrap_executor(agent_executor)
        request_handler = DefaultRequestHandler(
            agent_executor=agent_executor,
            task_store=InMemoryTaskStore(),
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )
        import uvicorn

        uvicorn.run(server.build(), host=host, port=port)
    except MissingAPIKeyError as e:
        logger.error(f'Error: {e}')
        exit(1)
    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        exit(1)


if __name__ == '__main__':
    main()
