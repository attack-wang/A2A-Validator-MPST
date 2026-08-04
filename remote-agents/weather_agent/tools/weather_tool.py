"""天气查询工具：通过 Open-Meteo API 获取真实天气数据。"""

import asyncio
import logging
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger(__name__)

# Open-Meteo Geocoding API：根据地名获取经纬度
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
# Open-Meteo Weather Forecast API
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


async def _get_json_with_retry(
    url: str,
    params: Dict[str, Any],
    *,
    attempts: int = 3,
) -> Dict[str, Any]:
    """Retry temporary network/5xx failures without hiding permanent errors."""
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            last_error = exc
            retryable = isinstance(exc, httpx.RequestError) or (
                isinstance(exc, httpx.HTTPStatusError)
                and exc.response.status_code >= 500
            )
            if not retryable or attempt + 1 >= attempts:
                raise
            delay = 1.0 * (2**attempt)
            logger.warning(
                "[weather_tool] 临时请求失败，%.0f秒后重试（%s/%s）: %s",
                delay,
                attempt + 1,
                attempts,
                exc,
            )
            await asyncio.sleep(delay)
    raise RuntimeError(f"天气请求失败: {last_error}")


async def query_weather(city: str, date: Optional[str] = None) -> str:
    """查询指定城市的天气信息。

    Args:
        city: 城市名称，支持中文。例如："北京"、"上海"。
        date: 日期，格式 "YYYY-MM-DD"。如果为 None，查询当天天气。

    Returns:
        格式化的天气信息文本。如果查询失败返回错误提示。
    """
    logger.info(f"[weather_tool] 查询天气: city={city}, date={date}")

    # 1. 获取城市经纬度
    try:
        geo_data = await _get_json_with_retry(
            GEOCODING_URL,
            {
                "name": city,
                "count": 1,
                "language": "zh",
                "format": "json",
            },
        )
    except Exception as exc:
        logger.error(f"[weather_tool] 地理编码请求失败: {exc}")
        return f"抱歉，查询城市「{city}」的天气信息时出现网络错误，请稍后重试。"

    results = geo_data.get("results")
    if not results:
        return f"未找到城市「{city}」的位置信息，请检查城市名称是否正确。"

    lat = results[0]["latitude"]
    lon = results[0]["longitude"]
    country = results[0].get("country", "")
    admin1 = results[0].get("admin1", "")
    full_name = f"{city} ({admin1}, {country})" if admin1 else f"{city} ({country})"

    # 2. 调用天气 API
    params: Dict[str, Any] = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "weather_code",
            "precipitation_probability_max",
            "wind_speed_10m_max",
        ],
        "timezone": "auto",
    }

    if date:
        params["start_date"] = date
        params["end_date"] = date
    else:
        # 默认查询当天及未来 5 天
        params["forecast_days"] = 6

    try:
        weather_data = await _get_json_with_retry(WEATHER_URL, params)
    except Exception as exc:
        logger.error(f"[weather_tool] 天气请求失败: {exc}")
        return f"抱歉，查询「{full_name}」的天气数据时出现网络错误，请稍后重试。"

    daily = weather_data.get("daily")
    if not daily:
        return f"未能获取到「{full_name}」的天气预报数据，API 返回为空。"

    # 3. 格式化输出
    dates = daily.get("time", [])
    max_temps = daily.get("temperature_2m_max", [])
    min_temps = daily.get("temperature_2m_min", [])
    codes = daily.get("weather_code", [])
    rain_probs = daily.get("precipitation_probability_max", [])
    wind_speeds = daily.get("wind_speed_10m_max", [])

    lines = [f"【{full_name} 天气预报】", ""]

    for i in range(len(dates)):
        date_str = dates[i]
        max_t = max_temps[i]
        min_t = min_temps[i]
        code = codes[i]
        rain = rain_probs[i]
        wind = wind_speeds[i]

        desc = _weather_code_to_desc(code)
        lines.append(
            f"📅 {date_str}  {desc}\n"
            f"   🌡 温度: {min_t}°C ~ {max_t}°C\n"
            f"   🌧 降水概率: {rain}%\n"
            f"   💨 最大风速: {wind} km/h\n"
        )

    return "\n".join(lines)


# WMO Weather interpretation codes (Open-Meteo weather_code)
def _weather_code_to_desc(code: int) -> str:
    """将 WMO weather code 转换为中文描述。"""
    mapping = {
        0: "☀ 晴天",
        1: "🌤  mainly clear",
        2: "⛅ 部分多云",
        3: "☁ 阴天",
        45: "🌫 雾",
        48: "🌫 雾凇",
        51: "🌧 毛毛雨（轻度）",
        53: "🌧 毛毛雨（中度）",
        55: "🌧 毛毛雨（密集）",
        56: "🌨 冻雨（轻度）",
        57: "🌨 冻雨（密集）",
        61: "🌧 小雨",
        63: "🌧 中雨",
        65: "🌧 大雨",
        66: "🌨 冻雨（轻度）",
        67: "🌨 冻雨（密集）",
        71: "❄ 小雪",
        73: "❄ 中雪",
        75: "❄ 大雪",
        77: "🌨 雪粒",
        80: "🌦 阵雨（轻度）",
        81: "🌦 阵雨（中度）",
        82: "🌦 阵雨（猛烈）",
        85: "🌨 阵雪（轻度）",
        86: "🌨 阵雪（猛烈）",
        95: "⛈ 雷雨（轻度/中度）",
        96: "⛈ 雷阵雨伴冰雹（轻度）",
        99: "⛈ 雷阵雨伴冰雹（猛烈）",
    }
    return mapping.get(code, f"未知天气 (code={code})")
