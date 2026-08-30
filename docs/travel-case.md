# 旅行规划案例运行说明

旅行规划案例由仓库中的9个远程智能体组成，并使用
`host-platform/backend/python/hosts/multiagent/protocols/Travel.gt`
约束Host与各智能体的调用顺序。实验组和对照组使用相同模型、智能体、端口、
提示词和超时设置，只切换运行时验证开关。

## 智能体与端口

| 业务角色 | 目录 | AgentCard名称 | 端口 |
|---|---|---|---:|
| 天气查询 | `weather_agent` | Weather Agent | 10303 |
| 攻略生成 | `guide_agent` | Guide Agent | 10707 |
| 跨城交通选择 | `transport_select_agent` | Transport Select Agent | 10404 |
| 高铁查询 | `train_agent` | Train Agent | 10101 |
| 航班查询 | `flight_agent` | Flight Agent | 10808 |
| 酒店选择 | `hotel_agent` | Hotel Agent | 10606 |
| 景点门票 | `ticket_agent` | Ticket Agent | 10202 |
| 市内路线 | `public_transport_agent` | Public Transport Agent | 10505 |
| 预算计算 | `budget_agent` | Budget Agent | 10909 |

`Travel.gt`在Train Agent与Flight Agent之间设置互斥选择。一项合法且完整的
任务会覆盖8个必要阶段，只调用其中一个跨城交通分支。

Weather Agent与工具调用异常案例中的OP3均使用10303端口，两个案例不能同时
启动。自动实验执行器会检查端口；若发现已有服务，应先结束相应进程。

## 推荐的自动运行方式

从仓库根目录执行：

```powershell
# 在线天气与动态日期
uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_live.json --repetitions 1

# 论文天气输入回放
uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_paper_replay.json --repetitions 1
```

执行器会自动设置验证模式、启动全部服务、注册Agent、创建新会话并保存结果，
不需要在UI中逐个注册。

## 手工启动与注册

需要调试单个智能体时，可在不同终端中从仓库根目录启动。例如：

```powershell
cd remote-agents\weather_agent
$env:PYTHONUTF8="1"
$env:PYTHONIOENCODING="utf-8"
$env:VALIDATION_ENABLED="true"
$env:MPST_DEFAULT_GT_FILE="Travel.gt"
$env:MPST_DEFAULT_PROTOCOL_NAME="Travel"
uv run --frozen --python 3.13 .
```

其余智能体只需替换目录。全部远程智能体启动后运行Host：

```powershell
cd host-platform\frontend\ui
$env:VALIDATION_ENABLED="true"
$env:MPST_DEFAULT_GT_FILE="Travel.gt"
$env:MPST_DEFAULT_PROTOCOL_NAME="Travel"
uv run --frozen --python 3.13 main.py
```

在UI的Agents页面注册：

```text
http://localhost:10303
http://localhost:10707
http://localhost:10404
http://localhost:10101
http://localhost:10808
http://localhost:10606
http://localhost:10202
http://localhost:10505
http://localhost:10909
```

切换 `VALIDATION_ENABLED` 后必须重启Host和全部远程智能体，并创建新会话，
避免复用上一轮协议状态。

## 天气数据模式

- `WEATHER_DATA_MODE=live`：调用Open-Meteo实时预报接口；
- `WEATHER_DATA_MODE=replay`：读取 `WEATHER_FIXTURE_FILE` 指定的固定响应。

论文日期已经过去，应使用 `travel_paper_replay.json`；验证当前部署和外部接口时
使用 `travel_live.json`。
