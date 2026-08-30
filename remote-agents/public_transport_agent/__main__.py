import logging
import os

import click

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent import PublicTransportAgent
from agent_executor import PublicTransportAgentExecutor
from dotenv import load_dotenv
from timestamp_ext import TimestampExtension


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=10505)
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
            id='transport',
            name='City Public Transport Planner',
            description='根据旅游攻略中的景点位置，规划目的地市内的公共出行路线（地铁/公交/打车）并估算费用。只能处理市内交通规划，不涉及航班、火车票、酒店等其他领域。',
            tags=['transport', 'subway', 'bus', 'taxi', 'city', 'route'],
            examples=[
                '今天要去故宫、天坛和南锣鼓巷，怎么安排市内交通最方便？',
                '从上海人民广场到外滩坐地铁几号线？大概多少钱？'
            ]
        )
        # Agent Card for Public Transport
        agent_card = AgentCard(
            name='Public Transport Agent',
            description='专门规划旅游目的地市内的公共交通路线（地铁/公交/打车）。范围仅限市内交通规划，其他问题会拒绝。',
            url=f'http://{host}:{port}/',  # Assuming separate ports for remote agents
            version='1.0.0',
            default_input_modes=PublicTransportAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=PublicTransportAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[warehouse_skill],
        )
        agent_executor = PublicTransportAgentExecutor()
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
