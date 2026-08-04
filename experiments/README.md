# 自动化实验

`scripts/experiment_runner.py` 直接调用网页使用的 Host 接口，自动完成：

1. 分别以 `VALIDATION_ENABLED=true` 和 `false` 启动 Host 与远程 Agent；
2. 注册远程 Agent；
3. 每次实验创建全新会话，发送配对提示词并等待任务结束；
4. 保存会话消息、Host 内部工具调用、远程返回、任务状态和各进程日志；
5. 生成逐次结果、两组配对结果、分组均值以及人工评分表。

## 旅行规划实验

先关闭之前手工启动的 Host 和旅行 Agent，然后在项目根目录运行：

```powershell
uv run --python 3.13 python scripts\experiment_runner.py --config experiments\travel_experiment.json
```

默认每组重复 10 次，即验证开启和关闭各运行 10 次。先做一次小规模检查时使用：

```powershell
uv run --python 3.13 python scripts\experiment_runner.py --config experiments\travel_experiment.json --repetitions 1
```

只检查本次实际会使用的提示词，不启动模型或 Agent：

```powershell
uv run --python 3.13 python scripts\experiment_runner.py --config experiments\travel_experiment.json --dry-run
```

如果服务已由人工启动，只能运行与其环境变量一致的单组实验：

```powershell
uv run --python 3.13 python scripts\experiment_runner.py --config experiments\travel_experiment.json --mode on --reuse-services
```

结果保存在 `experiments/results/<实验名-时间>/`。其中：

- `summary.csv`：每次实验的客观指标；
- `aggregate.csv`：两组指标均值；
- `paired_comparison.csv`：相同提示词和重复编号的配对差值；
- `manual_scoring.csv`：信息完整度、人工逻辑冲突数和备注；
- `scoring_guide.csv`：六个任务点各自的 0/1 分判定规则；
- `communications.csv`：按时间排列的应用层通信内容；
- `a2a_trace.csv`：Host 边界处实际发送和接收的 A2A 载荷，可替代人工抓包；
- `messages.json`、`events.json`、`tasks.json`：未经简化的原始记录；
- `process_logs/`：该次实验期间 Host 与各远程 Agent 新增的日志。

`automatic_task_point_evidence_0_6` 只表示程序找到了多少项支持证据，用于
帮助人工复核，不能直接代替语义判断。最终案例得分填写在
`manual_scoring.csv`：六个任务点各计 0 或 1 分，总分为 0–6 分。

`process_score_0_10` 是透明的流程评分：任务完成 2 分、必要 Agent 组覆盖
3 分、实际 A2A 调用严格符合协议顺序 3 分、无远程失败任务 1 分、最终
回答无工具调用外泄 1 分。该分数不代替论文中的人工信息完整度评分。

`exact_protocol_sequence`、`repeated_agent_task` 和
`redundant_business_calls` 均根据真正跨过 A2A 边界的调用计算；
`blocked_send_message_calls` 表示模型已生成、但未实际外发的
`send_message` 调用。这样，被验证器拒绝的并发调用不会被误计为实际通信。

## 最终输出质量的大规模实验

在 10+10 次预实验确认服务、提示词和评分规则正常后，使用独立配置运行正式实验：

```powershell
uv run --python 3.13 python scripts\experiment_runner.py --config experiments\travel_final_output_large.json
```

该配置保持 `send_message` 的并发执行方式不变，验证开启和关闭各运行 100 次，共
200 次。正式实验使用与预实验相同的固定提示词、Agent、模型和超时设置，结果写入
新的 `travel-final-output-large-<时间>` 目录，不会覆盖预实验数据。

大规模实验新增以下最终输出指标：

- `final_output_usable`：任务成功结束，且最终文本不是工具调用外泄或错误消息；
- `output_transport_complete`：包含指定日期的往返车次或航班；
- `output_hotel_complete`：包含酒店名称和三晚住宿信息；
- `output_ticket_complete`：包含三日景点及门票预订信息；
- `output_weather_adapted`：体现天气与室内、室外活动的对应关系；
- `output_daily_routes_complete`：包含每日交通方式、路线或换乘及费用；
- `output_budget_complete`：调用 Budget Agent，并给出分项、总价和人均预算；
- `output_completeness_score_0_6`：上述六项的合计得分。

如果运行途中因网络、模型服务或电脑重启而中断，可以从已有结果目录继续：

```powershell
uv run --python 3.13 python scripts\experiment_runner.py --config experiments\travel_final_output_large.json --resume-dir experiments\results\travel-final-output-large-YYYYMMDD-HHMMSS
```

恢复运行时，脚本会读取已有的 `run.json`，跳过已经完成的实验编号，只补做缺失项。
