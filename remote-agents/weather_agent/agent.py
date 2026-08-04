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

from tools.weather_tool import query_weather

# 增加这一行来定义 logger
logger = logging.getLogger(__name__)


class WeatherAgent:
    """An agent that queries weather information for specific locations and dates."""

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']
    requires_tool_call = True

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
        return 'Processing the weather query request...'

    def _build_agent(self) -> LlmAgent:
        """Builds the LLM agent for weather queries."""
        return LlmAgent(
            model=LiteLlm(
                model=os.getenv(
                    'AGENT_MODEL',
                    'ollama/gpt-oss:120b-cloud',
                )
            ),
            name='weather_agent',
            description=(
                'This agent queries weather information for specific locations and dates.'
            ),
            instruction="""
                你是一名专注于真实天气信息查询的助手。

                **核心职责：**
                1. 根据用户提供的：城市名称（支持中文/英文）、日期（可选当天、未来几天），调用真实天气 API 获取实时天气数据。
                2. 返回的天气信息包括：温度范围、天气状况（晴/阴/雨/雪等）、最大风速、降水概率。数据来源为真实气象数据。
                3. 如果没有指定日期，默认查询当天及未来 5 天的天气预报。
                4. 信息不足时（缺少城市名称），仅主动询问缺失的核心信息。

                ## Tool 使用说明：
                你配备了 `query_weather` 工具。当用户询问天气、温度、降雨、风力等信息时，**必须**调用此工具获取真实数据，不得自行编造。
                
                ### 调用规范：
                - city（必填）：城市名称，如 "北京"、"上海"、"New York"。
                - date（可选）：日期，格式 "YYYY-MM-DD"。不传则默认查询当天及未来数天。
                
                ## 严格范围限制：
                1. 你只能回答与**天气信息查询**直接相关的问题。
                2. 如果用户询问以下任何领域的问题，你必须明确拒绝，且不得提供任何相关内容：
                   - 航班查询与订票
                   - 火车票查询与购买
                   - 酒店预定
                   - 旅游攻略与行程安排
                   - 景点门票购买
                   - 公共交通路线规划（地铁/公交/打车）
                   - 预算计算与费用均分
                   - 跨城交通工具选择（飞机 vs 火车）
                3. 标准拒绝话术：
                   "抱歉，我是天气查询助手，只处理天气查询相关的问题，无法回答您的问题。请咨询对应的 specialist。"
                4. 绝不要替用户完成其他 agent 的职责。绝不要主动提供超出天气范围的建议。

                ## 输出格式要求：
                - 返回 LLM 收到的工具原始结果即可，已包含格式化信息。
                - 信息不足时仅索要缺失数据，不做额外推断。
            """,
            tools=[
                query_weather,
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
        tool_call_observed = False
        tool_response_observed = False
        last_tool_name = ''
        async for event in self._runner.run_async(
            user_id=self._user_id, session_id=session.id, new_message=content
        ):
            parts = (
                event.content.parts
                if event.content and event.content.parts
                else []
            )
            final_event_has_tool_call = False
            for part in parts:
                function_call = getattr(part, 'function_call', None)
                if function_call:
                    tool_call_observed = True
                    final_event_has_tool_call = event.is_final_response()
                    last_tool_name = (
                        getattr(function_call, 'name', '')
                        or last_tool_name
                    )
                if getattr(part, 'function_response', None):
                    tool_response_observed = True

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
                        if p.function_response
                    )
                elif (
                    event.content
                    and event.content.parts
                    and any(p.function_call for p in event.content.parts)
                ):
                    function_call = next(
                        p.function_call
                        for p in event.content.parts
                        if p.function_call
                    )
                    response = (
                        "Error: Tool call not executed - "
                        f"{function_call.name}"
                    )
                yield {
                    'is_task_complete': True,
                    'content': response,
                    'tool_required': True,
                    'tool_call_observed': tool_call_observed,
                    'tool_response_observed': tool_response_observed,
                    'unexecuted_tool_call': final_event_has_tool_call,
                    'tool_name': last_tool_name,
                }
            else:
                yield {
                    'is_task_complete': False,
                    'updates': self.get_processing_message(),
                }
