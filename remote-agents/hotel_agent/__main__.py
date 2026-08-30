import logging
import os

import click

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent import HotelAgent
from agent_executor import HotelAgentExecutor
from dotenv import load_dotenv
from timestamp_ext import TimestampExtension


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=10606)
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
            id='book_hotel',
            name='Hotel Recommendation & Booking',
            description='根据旅游城市和行程安排推荐合适酒店，并支持预定。只能处理酒店相关任务，不涉及航班、火车票、天气、攻略等其他领域。',
            tags=['hotel', 'accommodation', 'booking', 'travel'],
            examples=[
                '去北京旅游3天，住在哪个区方便？帮我推荐几家中档酒店',
                '帮我预定上海外滩附近的酒店，预算500左右一晚'
            ]
        )
        # Agent Card for Hotel
        agent_card = AgentCard(
            name='Hotel Agent',
            description='专门根据旅游计划推荐合适酒店，给出酒店信息与参考价格，并可支持预定。范围仅限酒店推荐与预定，其他问题会拒绝。',
            url=f'http://{host}:{port}/',  # Assuming separate ports for remote agents
            version='1.0.0',
            default_input_modes=HotelAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=HotelAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[warehouse_skill],
        )
        agent_executor = HotelAgentExecutor()
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
