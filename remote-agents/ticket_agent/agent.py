import json
import os
import random
from typing import Optional

from collections.abc import AsyncIterable
from typing import Any

from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import logging

# 增加这一行来定义 logger
logger = logging.getLogger(__name__)


class TicketAgent:
    """An agent that helps users purchase or reserve attraction tickets."""

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']

    def __init__(self):
        self._agent = self._build_agent()
        self._user_id = 'remote_agent'
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    def get_processing_message(self) -> str:
        return 'Processing the ticket purchase request...'

    def _build_agent(self) -> LlmAgent:
        """Builds the LLM agent for ticket purchasing."""
        return LlmAgent(
            model=LiteLlm(
                model=os.getenv(
                    'AGENT_MODEL',
                    'ollama/qwen3.5:cloud',
                )
            ),
            name='ticket_agent',
            description=(
                'This agent helps users purchase or reserve attraction tickets based on travel itineraries.'
            ),
            instruction="""
                你是一名专注于旅游景点门票购买与预约模拟的助手。

                **核心职责：**
                1. 根据用户提供的：城市、景点名称、游玩日期、人数信息，查询景点门票信息（模拟数据），并模拟完成购买/预约流程。
                2. 为每个景点提供：门票价格（成人/儿童/优惠）、开放时间、是否需要提前预约。
                3. 模拟购买成功后返回：确认信息（模拟）、景点、日期、票数、总价。
                4. 如果信息不足（缺少城市/景点/日期），仅询问缺失核心信息，不做额外假设。

                ## 严格范围限制：
                1. 你只能回答与**景点门票购买与预约模拟**直接相关的问题。
                2. 如果用户询问以下任何领域的问题，你必须明确拒绝，且不得提供任何相关内容：
                   - 航班查询与订票
                   - 火车票查询与购买
                   - 酒店预定
                   - 天气查询
                   - 旅游攻略与行程安排（你只管门票，不管路线怎么安排）
                   - 公共交通路线规划（地铁/公交/打车）
                   - 预算计算与费用均分
                   - 跨城交通工具选择（飞机 vs 火车）
                3. 标准拒绝话术：
                   "抱歉，我是景点门票助手，只负责景点门票购买/预约，无法回答您的问题。请咨询对应的 specialist。"
                4. 绝不要替用户完成其他 agent 的职责。绝不要主动提供超出门票范围的建议。

                ## 输出格式要求：
                - 门票信息包含：景点名称、日期、票价（成人/儿童）、是否需要预约。
                - 购买成功后返回：确认信息、日期、人数、总费用。
                - 信息不足时仅索要缺失数据，不做额外推断。
            """,
            tools=[

            ],
        )

    async def stream(self, query, session_id) -> AsyncIterable[dict[str, Any]]:
        session = await self._runner.session_service.get_session(
            app_name=self._agent.name,
            user_id=self._user_id,
            session_id=session_id,
        )
        content = types.Content(
            role='user', parts=[types.Part.from_text(text=query)]
        )
        if session is None:
            session = await self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                state={},
                session_id=session_id,
            )
        async for event in self._runner.run_async(
            user_id=self._user_id, session_id=session.id, new_message=content
        ):
            if event.is_final_response():
                response = ''
                if (
                    event.content
                    and event.content.parts
                    and event.content.parts[0].text
                ):
                    response = '\n'.join(
                        [p.text for p in event.content.parts if p.text]
                    )
                elif (
                    event.content
                    and event.content.parts
                    and any(
                        [
                            True
                            for p in event.content.parts
                            if p.function_response
                        ]
                    )
                ):
                    response = next(
                        p.function_response.model_dump()
                        for p in event.content.parts
                    )
                yield {
                    'is_task_complete': True,
                    'content': response,
                }
            else:
                yield {
                    'is_task_complete': False,
                    'updates': self.get_processing_message(),
                }
