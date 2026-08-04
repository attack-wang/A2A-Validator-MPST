import logging
import os

import click

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent import GuideAgent
from agent_executor import GuideAgentExecutor
from dotenv import load_dotenv
from timestamp_ext import TimestampExtension


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


@click.command()
@click.option('--host', default='localhost')
@click.option('--port', default=10707)
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
            id='guide_agent',
            name='Travel Itinerary Planner',
            description='根据用户提供的目的地、时间和偏好，制定旅游景点的游玩计划与行程安排。只能处理景点游玩攻略相关任务，不涉及其他领域。',
            tags=['travel', 'itinerary', 'guide', 'plan', 'schedule'],
            examples=[
                '帮我制定一份北京3天2晚的景点游玩攻略',
                '上海迪士尼一日游怎么安排最合理？'
            ]
        )
        # Agent Card for Guide
        agent_card = AgentCard(
            name='Guide Agent',
            description='专门制定旅游景点的每日游玩计划与行程安排，包括景点推荐、游玩顺序、时间安排、餐饮建议等。不涉及其他问题会拒绝。',
            url=f'http://{host}:{port}/',  # Assuming separate ports for remote agents
            version='1.0.0',
            default_input_modes=GuideAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=GuideAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[warehouse_skill],
        )
        agent_executor = GuideAgentExecutor()
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
