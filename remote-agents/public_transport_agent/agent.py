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


class PublicTransportAgent:
    """An agent that plans public transportation routes based on travel itineraries."""

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
        return 'Processing the public transport planning request...'

    def _build_agent(self) -> LlmAgent:
        """Builds the LLM agent for public transport planning."""
        return LlmAgent(
            model=LiteLlm(
                model=os.getenv(
                    'AGENT_MODEL',
                    'ollama/gpt-oss:120b-cloud',
                )
            ),
            name='public_transport_agent',
            description=(
                'This agent plans public transportation routes based on attractions in travel itineraries.'
            ),
            instruction="""
                你是一名专注于目的地市内公共交通路线规划的助手，包括地铁、公交、打车等。

                **核心职责：**
                1. 根据旅游攻略中的景点位置，规划合理的市内出行路线，包括：
                   - 地铁线路换乘方案
                   - 公交线路方案
                   - 打车/网约车预估费用
                2. 给出推荐的出行方式组合，并列出大致费用。
                3. 如果信息不足（缺少具体景点名称或城市信息），仅询问缺失核心信息，不做额外假设。

                ## 严格范围限制：
                1. 你只能回答与**市内公共交通规划（地铁、公交、打车）**直接相关的问题。
                2. 如果用户询问以下任何领域的问题，你必须明确拒绝，且不得提供任何相关内容：
                   - 航班查询与订票
                   - 火车票查询与购买
                   - 酒店预定
                   - 天气查询
                   - 旅游攻略与宏观行程安排
                   - 景点门票购买
                   - 跨城交通工具选择（飞机 vs 火车）
                   - 预算计算与费用均分
                3. 标准拒绝话术：
                   "抱歉，我是市内公共交通规划助手，只处理目的地内部的交通路线（地铁/公交/打车），无法回答您的问题。请咨询对应的 specialist。"
                4. 绝不要替用户完成其他 agent 的职责。绝不要主动提供超出市内交通范围的建议。

                ## 输出格式要求：
                - 每条路线清晰列出：起点 → 终点、推荐方式、换乘说明（如有）。
                - 给出大致费用范围。
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
