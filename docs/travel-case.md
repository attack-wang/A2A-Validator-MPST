# 旅行规划案例运行说明

旅行规划案例沿用 `PythonProject8` 的 9 个远程 Agent，并使用
`host-platform/backend/python/hosts/multiagent/protocols/Travel.gt`
约束 Host 与各 Agent 的调用顺序。实验组和对照组使用完全相同的代码、
模型、Agent、端口和提示词，只切换 `VALIDATION_ENABLED`。

## Agent 与端口

| 角色 | 目录 | AgentCard 名称 | 默认端口 |
|---|---|---|---:|
| Weatheragent | `weather_agent` | Weather Agent | 10303 |
| Guideagent | `guide_agent` | Guide Agent | 10707 |
| Transportselectagent | `transport_select_agent` | Transport Select Agent | 10404 |
| Trainagent | `train_agent` | Train Agent | 10101 |
| Flightagent | `flight_agent` | Flight Agent | 10808 |
| Hotelagent | `hotel_agent` | Hotel Agent | 10606 |
| Ticketagent | `ticket_agent` | Ticket Agent | 10202 |
| Publictransportagent | `public_transport_agent` | Public Transport Agent | 10505 |
| Budgetagent | `budget_agent` | Budget Agent | 10909 |

`Travel.gt` 在 Trainagent 与 Flightagent 之间包含互斥选择。一次合法任务
只会调用其中一个，因此正常的远程 Agent 覆盖数是 8/9；同时调用两个
大交通 Agent 反而属于分支违规。

Weather Agent 与 OP3 的默认端口都是 10303。旅行规划案例与 OP1—OP3
案例不要同时启动；切换案例前先停止上一案例的进程。

## 实验模式

在 Host/UI 和 9 个远程 Agent 的每一个终端中设置相同的值，然后再启动
进程。

实验组：

```powershell
$env:VALIDATION_ENABLED="true"
$env:MPST_DEFAULT_GT_FILE="Travel.gt"
$env:MPST_DEFAULT_PROTOCOL_NAME="Travel"
```

对照组：

```powershell
$env:VALIDATION_ENABLED="false"
$env:MPST_DEFAULT_GT_FILE="Travel.gt"
$env:MPST_DEFAULT_PROTOCOL_NAME="Travel"
```

关闭验证后，Host 不进行协议投影、初始化、消息验证或终态检查，也不会
增加协议标签；业务请求直接发送给相同的远程 Agent。每次切换开关后应
重启 Host 和全部远程 Agent，并新建会话，避免复用上一轮状态。

## 启动与注册

每个远程 Agent 在单独终端中按同一方式启动，只替换目录名：

```powershell
cd D:\Projects\mpst-a2a-validator\remote-agents\weather_agent
uv run --python 3.13 .
```

9 个 Agent 全部启动后，再启动 Host/UI：

```powershell
cd D:\Projects\mpst-a2a-validator\host-platform\frontend\ui
uv run --python 3.13 main.py
```

在 UI 的 Agents 页面注册以下地址：

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

## 配对实验提示词

有验证与无验证两组应逐字使用相同提示词。日期应选择天气接口可查询的
时间范围。推荐使用下列版本，并在每一对实验中只替换方括号内的固定
实验参数：

```text
我计划从[出发日期]至[返程日期]从南京前往北京旅游，共两位成人，
总预算一万元，请制定一份详细的旅游计划。最终行程的室内/户外安排
需要与天气信息一致；跨城交通选择需要考虑天气，天气不适合飞行时
优先选择高铁；景点门票应与旅游攻略中的景点一致；酒店选择需要同时
考虑行程和预算；每日市内路线需要给出交通方式、换乘路线和价格；
最后汇总全部开销并计算人均预算。必须实际调用相关远程 Agent 并等待
真实结果，不得模拟返回值。
```

两组至少记录：实际调用的 Agent 数、协议/逻辑冲突数、信息完整度、
Host 发起的业务通信次数、任务是否完成。开启验证时还应保存 Host 与
远程 Agent 的验证日志，以说明违规在哪一状态被发现及是否阻止了错误
状态推进。
