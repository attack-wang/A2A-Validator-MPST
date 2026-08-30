# Weather Agent

旅行规划案例的天气查询智能体，默认端口为`10303`。智能体通过Open-Meteo
获取天气数据，并支持论文天气响应回放。

```powershell
uv run --frozen --python 3.13 .
```

模型由`AGENT_MODEL`设置。`WEATHER_DATA_MODE`支持`live`和`replay`；回放时
还需设置`WEATHER_FIXTURE_FILE`。完整实验请从仓库根目录运行自动执行器。
