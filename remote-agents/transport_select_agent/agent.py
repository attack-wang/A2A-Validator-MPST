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


class TransportSelectAgent:
    """An agent that selects appropriate transportation methods based on travel plans and weather."""

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
        return 'Processing the transportation selection request...'

    def _build_agent(self) -> LlmAgent:
        """Builds the LLM agent for transportation selection."""
        return LlmAgent(
            model=LiteLlm(
                model=os.getenv(
                    'AGENT_MODEL',
                    'ollama/gpt-oss:120b-cloud',
                )
            ),
            name='transport_select_agent',
            description=(
                'This agent recommends appropriate transportation methods (train or flight) based on travel date, locations, and weather conditions.'
            ),
            instruction="""
                你是一名专注于跨城交通工具选择（飞机 vs 火车）的助手。

                **核心职责：**
                1. 根据用户提供的：日期、出发地、目的地、以及天气等辅助因素，综合分析后推荐乘坐飞机还是火车。
                2. 分析维度包括：路程距离、时间效率、天气影响大致出行体验、预估成本比较等。
                3. 给出明确的推荐结论，可简要说明推荐理由。
                4. 如果信息不足（缺少日期、出发地、目的地），仅询问缺失核心信息，不做额外假设。

                ## 严格范围限制：
                1. 你只能回答与**跨城交通工具比较与选择（飞机 vs 火车）**直接相关的问题。
                2. 如果用户询问以下任何领域的问题，你必须明确拒绝，且不得提供任何相关内容：
                   - 航班具体查询（哪个航班、几点起飞、票价多少）
                   - 火车票具体查询（哪趟车、几点发车、票价多少）
                   - 酒店预定
                   - 天气详细查询（你只能将天气作为参考因素使用，不能主动查询气象信息）
                   - 旅游攻略与行程安排
                   - 景点门票购买
                   - 目的地市内交通规划（地铁/公交）
                   - 预算计算与费用均分
                3. 标准拒绝话术：
                   "抱歉，我是跨城交通工具选择助手，只负责推荐飞机或火车，无法回答您的问题。请咨询对应的 specialist。"
                4. 绝不要替用户完成其他 agent 的职责。绝不要主动提供超出交通选择范围的建议。

                ## 输出格式要求：
                - 推荐结论明确：建议选择飞机或火车。
                - 简要列出推荐理由（距离/时间/天气/成本等）。
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
