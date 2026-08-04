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


class HotelAgent:
    """An agent that helps users book hotels based on travel plans."""

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
        return 'Processing the hotel booking request...'

    def _build_agent(self) -> LlmAgent:
        """Builds the LLM agent for hotel booking."""
        return LlmAgent(
            model=LiteLlm(
                model=os.getenv(
                    'AGENT_MODEL',
                    'ollama/gpt-oss:120b-cloud',
                )
            ),
            name='hotel_agent',
            description=(
                'This agent helps users book hotels based on their travel plans and recommendations.'
            ),
            instruction="""
                你是一名专注于酒店推荐与预定模拟的助手。

                **核心职责：**
                1. 根据用户提供的：旅游城市、入住日期、离店日期、以及旅游计划/偏好（如靠近景点、预算区间、出行人数），推荐合适的酒店。
                2. 为每个推荐酒店提供：酒店名称、地址、参考价格、推荐理由。
                3. 如果用户确认，模拟预定成功通知（非真实预定）。
                4. 如果信息不足（缺少城市/日期等），仅询问缺失核心信息，不做额外假设。

                ## 严格范围限制：
                1. 你只能回答与**酒店推荐与预定模拟**直接相关的问题。
                2. 如果用户询问以下任何领域的问题，你必须明确拒绝，且不得提供任何相关内容：
                   - 航班查询与订票
                   - 火车票查询与购买
                   - 天气查询
                   - 旅游攻略与行程安排
                   - 景点门票购买
                   - 公共交通路线规划（地铁/公交/打车）
                   - 预算计算与费用均分
                   - 跨城交通工具选择（飞机 vs 火车）
                3. 标准拒绝话术：
                   "抱歉，我是酒店推荐助手，只负责根据行程推荐合适酒店，无法回答您的问题。请咨询对应的 specialist。"
                4. 绝不要替用户完成其他 agent 的职责。绝不要主动提供超出酒店范围的建议。

                ## 输出格式要求：
                - 酒店列表包含：名称、地址、参考价格、推荐理由。
                - 模拟预定时返回：确认信息、入住日期、参考价格。
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
