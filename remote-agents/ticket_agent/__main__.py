import logging
import os

import click

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent import TicketAgent
from agent_executor import TicketAgentExecutor
from dotenv import load_dotenv
from timestamp_ext import TimestampExtension


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=10202)
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
            id='ticket_buying_agent',
            name='Attraction Ticket Purchase',
            description='根据旅游攻略中规划的景点，查询门票信息并支持购买/预约。只能处理景点门票相关任务，不涉及航班、酒店、天气等其他领域。',
            tags=['ticket', 'attraction', 'booking', 'scenic'],
            examples=[
                '故宫门票多少钱？需要提前多久预约？',
                '帮我买2张7月15日上海迪士尼的成人票'
            ]
        )
        # Agent Card for Ticket
        agent_card = AgentCard(
            name='Ticket Agent',
            description='专门查询景点门票信息并支持购买/预约。范围仅限景点门票，其他问题会拒绝。',
            url=f'http://{host}:{port}/',  # Assuming separate ports for remote agents
            version='1.0.0',
            default_input_modes=TicketAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=TicketAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[warehouse_skill],
        )
        agent_executor = TicketAgentExecutor()
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
