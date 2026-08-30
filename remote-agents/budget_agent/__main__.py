import logging
import os

import click

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent import BudgetAgent
from agent_executor import BudgetAgentExecutor
from dotenv import load_dotenv
from timestamp_ext import TimestampExtension


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=10909)
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
            id='budget-agent',
            name='Budget Calculator',
            description='根据旅行项目总金额和参与人数，计算每个人的预算份额。只能处理预算计算相关任务，不涉及航班、酒店、天气等其他领域。',
            tags=['budget', 'cost', 'expense', 'split', 'calculation'],
            examples=[
                '5个人去旅游，交通费5000，住宿费3000，门票2000，每人多少钱？',
                '团队10人，总花费15000，帮我算下每人均摊多少？'
            ]
        )
        # Agent Card for Budget
        agent_card = AgentCard(
            name='Budget Agent',
            description='专门计算旅游团队费用均分。根据输入的项目金额和人数计算人均预算。范围仅限预算计算，其他问题会拒绝。',
            url=f'http://{host}:{port}/',  # Assuming separate ports for remote agents
            version='1.0.0',
            default_input_modes=BudgetAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=BudgetAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[warehouse_skill],
        )
        agent_executor = BudgetAgentExecutor()
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
