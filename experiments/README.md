# 自动化实验与指标说明

两个执行器均直接调用Mesop UI使用的Host接口，自动启动和停止服务、注册远程
智能体、创建独立会话、发送固定提示词、等待任务结束并导出通信轨迹。验证器开启
和关闭两组使用相同代码、模型、输入与超时配置，只改变验证开关。

每个结果目录都包含：

- `resolved_prompts.json`：本次运行实际使用的提示词；
- `config.snapshot.json`：展开继承关系后的配置和运行环境；
- `summary.csv`：逐项任务指标；
- `aggregate.csv`：两组指标均值；
- `paired_comparison.csv`：相同提示词和重复编号的配对记录；
- `communications.csv`：按时间排序的应用层消息；
- `a2a_trace.csv`：真正跨越Host通信边界的A2A载荷；
- `<模式>/<任务>/`：单项任务的消息、事件、任务、工具调用及进程日志。

## 1. 工具调用异常案例

配置文件为 `security_chain_experiment.json`。5个固定IP各重复10次，验证开启和
关闭各得到50项任务记录。

```powershell
# 只解析配置，不启动服务
uv run --frozen --python 3.13 python scripts\security_experiment_runner.py --dry-run

# 每个IP执行一次
uv run --frozen --python 3.13 python scripts\security_experiment_runner.py --repetitions 1

# 论文规模：每个IP执行10次
uv run --frozen --python 3.13 python scripts\security_experiment_runner.py
```

该案例额外生成：

- `validation_events.csv`：验证错误、纠错重试、恢复成功和重试耗尽事件；
- `error_counts.csv`：按模式、服务、阶段和错误码汇总的发生次数；
- `error_aggregate.csv`：两组错误、恢复和最终阻断次数；
- `<模式>/<任务>/validation_events.json`：可以追溯到单项任务的事件记录。

`validation_error_count`记录验证器观察到的错误事件；
`recovery_retry_count`记录错误提示反馈给模型后发生的重新生成；
`recovery_success_count`记录重新生成后通过验证的次数；
`recovery_exhausted_count`记录达到重试上限的次数；
`final_block_count`记录最终未被发送的异常输出。被发送前识别的非法消息属于
“违规尝试”，不会计入已经跨越通信边界的实际业务通信。

为保证日志计数完整，应让执行器启动服务。`--reuse-services`无法读取外部进程
启动前的日志，只适合交互调试。

## 2. 旅行规划案例

旅行案例包含天气查询、攻略生成、交通选择、高铁或航班、酒店、门票、市内路线
和预算计算8个必要业务阶段。高铁与航班是互斥分支，因此一项完整任务实际调用
8个远程智能体。

### 2.1 在线运行

`travel_live.json`把出发日期解析为运行日之后第3天，行程持续4天：

```powershell
uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_live.json --repetitions 1
```

该模式调用实时Open-Meteo接口，用于检查当前环境和执行流程。

### 2.2 论文数据回放

`travel_paper_replay.json`继承100次正式实验配置，并使用
`fixtures/weather_beijing_2026-08-10_13.json`中保存的原实验天气响应：

```powershell
uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_paper_replay.json
```

天气回放固定了外部天气输入，但Host和远程智能体仍由大语言模型驱动，因此重新
执行得到的文本和个别任务结果可能发生变化。

### 2.3 主要指标

- **任务完成率**：在规定时间内结束并返回非错误最终回复的任务比例；
- **通信效率**：非重复远程业务调用数与实际远程业务调用总数之比；
- **实际重复调用数**：同一业务阶段超过首次调用的累计次数；
- **智能体覆盖数**：一项任务实际覆盖的8个必要业务阶段数量；
- **输出质量得分**：AI评价器对交通、住宿、门票、天气适配、每日路线和预算
  六项内容分别给出0或1分，合计为0～6分。

执行器在 `summary.csv` 中保留的 `output_completeness_score_0_6` 是关键词规则
形成的自动预检值，只用于发现明显缺项；论文输出质量以
`ai_output_scores.csv`中的 `ai_output_quality_score_0_6` 为准。

过程指标只根据真正出现在 `a2a_trace.csv` 中的业务消息计算。模型已经生成、但
被验证器在发送前阻断的 `send_message` 调用记录在
`blocked_send_message_calls`中，不计入实际通信次数。

## 3. AI输出质量评价

评价配置、提示词和程序分别位于：

- `ai_judge_config.json`；
- `ai_output_judge_prompt.md`；
- `scripts/evaluate_outputs.py`。

先检查第一项任务的完整评价提示词：

```powershell
uv run --frozen --python 3.13 python scripts\evaluate_outputs.py `
  experiments\results\<旅行实验目录> --dry-run
```

执行评价：

```powershell
uv run --frozen --python 3.13 python scripts\evaluate_outputs.py `
  experiments\results\<旅行实验目录>
```

评价器只读取Host最终回复，不读取验证模式、过程指标或论文结论，避免将组别信息
泄露给评价模型。每项判断均保存直接证据、缺失原因和模型原始JSON回复。

## 4. 中断恢复

长时间实验可从已有结果目录继续：

```powershell
uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_paper_replay.json `
  --resume-dir experiments\results\travel-paper-replay-YYYYMMDD-HHMMSS
```

执行器读取已有 `run.json`，跳过已经完成的模式、提示词和重复编号，只运行缺失项。
