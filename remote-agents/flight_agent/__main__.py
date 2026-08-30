import logging
import os

import click

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent import FlightAgent
from agent_executor import FlightAgentExecutor
from dotenv import load_dotenv
from timestamp_ext import TimestampExtension


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=10808)
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
            id='flight_ticket',
            name='Flight Query & Booking',
            description='根据日期、出发地和目的地查询航班信息，并支持机票预订。只能处理航班相关任务，不涉及火车票、酒店、天气等其他领域。',
            tags=['flight', 'airplane', 'ticket', 'booking', 'travel'],
            examples=[
                '2024-10-01 从北京到上海的航班有哪些？',
                '帮我预订明天早上从北京到深圳的机票'
            ]
        )
        # Agent Card for Flight
        agent_card = AgentCard(
            name='Flight Agent',
            description='专门查询航班信息和预订机票。根据日期、出发地、目的地提供航班列表。范围仅限航班查询与订票，其他问题会拒绝。',
            url=f'http://{host}:{port}/',  # Assuming separate ports for remote agents
            version='1.0.0',
            default_input_modes=FlightAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=FlightAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[warehouse_skill],
        )
        agent_executor = FlightAgentExecutor()
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
