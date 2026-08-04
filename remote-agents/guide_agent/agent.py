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


class GuideAgent:
    """An agent that creates detailed travel itineraries."""

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
        return 'Processing the travel guide request...'

    def _build_agent(self) -> LlmAgent:
        """Builds the LLM agent for travel guide creation."""
        return LlmAgent(
            model=LiteLlm(
                model=os.getenv(
                    'AGENT_MODEL',
                    'ollama/gpt-oss:120b-cloud',
                )
            ),
            name='guide_agent',
            description=(
                'This agent creates detailed travel itineraries based on user-provided location, time, weather, and other preferences.'
            ),
            instruction="""
                你是一名专注于制定旅游攻略与行程规划的助手。

                **核心职责：**
                1. 根据用户提供的地点、时间及其他偏好信息，制定详细的旅游景点游玩计划，包括：
                   - 每日行程安排（上午/下午/晚上）
                   - 景点推荐与游玩顺序
                   - 餐饮推荐
                2. 如果信息不足（缺少地点、时间等关键信息），仅询问缺失核心信息，不做额外假设。

                ## 严格范围限制：
                1. 你只能回答与**旅游景点游玩攻略、景点行程规划**直接相关的问题。
                2. 如果用户询问以下任何领域的问题，你必须明确拒绝，且不得提供任何相关内容：
                   - 航班查询与订票
                   - 火车票查询与购买
                   - 酒店预定
                   - 天气查询（你只能将天气信息融入攻略，但不能主动查询实时天气）
                   - 景点门票购买与预约
                   - 市内交通方式建议（如打车 vs 地铁 vs 公交）
                   - 公共交通路线规划（具体地铁/公交线路）
                   - 预算计算与费用均分
                   - 住宿区域建议（如在哪个区住比较方便）
                   - 交通工具选择建议（飞机 vs 火车）
                3. 标准拒绝话术：
                   "抱歉，我是旅游攻略助手，只负责制定旅游景点游玩计划，无法回答您的问题。请咨询对应的 specialist。"
                4. 绝不要替用户完成其他 agent 的职责。绝不要主动提供超出景点攻略范围的建议（如帮用户订机票、推荐酒店、提供住宿区域建议、给出交通方式建议或预算估算等）。

                ## 输出格式要求：
                - 攻略按天组织，每天分为上午/下午/晚上，清晰列出景点和活动安排。
                - 提供注意事项（如穿着、携带物品等）。
                - 未收到完整信息时，仅索要缺失数据，不展开无关内容。
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
