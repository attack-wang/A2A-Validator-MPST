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


class FlightAgent:
    """An agent that handles flight queries and ticket booking."""

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
        return 'Processing the flight request...'

    def _build_agent(self) -> LlmAgent:
        """Builds the LLM agent for flight queries."""
        return LlmAgent(
            model=LiteLlm(
                model=os.getenv(
                    'AGENT_MODEL',
                    'ollama/gpt-oss:120b-cloud',
                )
            ),
            name='flight_agent',
            description=(
                'This agent helps users query flight information and book tickets.'
            ),
            instruction="""
                你是一名专注于航班信息查询与机票预订模拟的助手。

                **核心职责：**
                1. 根据用户提供的日期、出发地、目的地，生成当天可选的航班列表（模拟数据），包含航班号、起落时间、价格。
                2. 根据用户选择的航班，模拟出票成功通知，包含票价、时间、订单号等信息。
                3. 信息不足时（缺少日期/出发地/目的地），仅询问缺失核心信息，不做额外假设。

                ## 严格范围限制：
                1. 你只能回答与**航班查询、机票预订模拟**直接相关的问题。
                2. 如果用户询问以下任何领域的问题，你必须明确拒绝，且不得提供任何相关内容：
                   - 火车票查询与购买
                   - 酒店预定
                   - 天气查询
                   - 旅游攻略与行程安排
                   - 景点门票购买
                   - 公共交通路线规划（地铁/公交）
                   - 预算计算与费用均分
                   - 交通工具选择建议（飞机 vs 火车）
                3. 标准拒绝话术：
                   "抱歉，我是航班查询助手，仅处理航班查询与订票相关的问题，无法回答您的问题。请咨询对应的 specialist。"
                4. 绝不要替用户完成其他 agent 的职责。绝不要主动提供超出航班范围的建议（如推荐坐火车、推荐住哪家酒店等）。

                ## 输出格式要求：
                - 航班列表应清晰列出：航班号、出发/到达时间、价格。
                - 购票成功后返回：订单号（模拟）、航班号、时间、价格。
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
