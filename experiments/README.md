# 自动化实验与指标说明

两个执行器均直接调用Mesop UI使用的Host接口，自动启动和停止服务、注册远程
智能体、创建独立会话、发送固定提示词、等待任务结束并导出通信轨迹。验证器开启
和关闭两组使用相同代码、模型、输入与超时配置，只改变验证开关。

结果默认写入`experiments/results/<实验名称>-YYYYMMDD-HHMMSS/`。使用
`--dry-run`预检时只生成`resolved_prompts.json`和`reproducibility.json`；正式
运行生成`config.snapshot.json`、`summary.csv`、`aggregate.csv`、
`paired_comparison.csv`和`manifest.json`。正式运行的完整文件级说明见本文档
第5节。

## 1. 工具调用异常案例

配置文件为 `security_chain_experiment.json`。每轮实验只向主控智能体提交一次
固定IP查询；主控智能体依次调用三个远程智能体，并将上一阶段的真实结果自动
传递给下一阶段。正式配置将完整执行链重复50次，验证开启和关闭各得到50项
任务记录。

```powershell
# 只解析配置，不启动服务
uv run --frozen --python 3.13 python scripts\security_experiment_runner.py --dry-run

# 一条完整执行链在开启、关闭模式下各执行一次，共2项记录
uv run --frozen --python 3.13 python scripts\security_experiment_runner.py --repetitions 1

# 论文规模：完整执行链在开启、关闭模式下各执行50次
uv run --frozen --python 3.13 python scripts\security_experiment_runner.py
```

配置预检通常在数秒内完成。小规模命令运行2项任务，每项任务的等待上限为10分钟，
任务等待时间最多约20分钟；论文规模命令运行100项任务，任务等待上限合计约
16小时40分钟。两者还需要计算服务启动和停止时间，实际耗时取决于云端模型和网络。
单项任务的实际耗时见`run.json`和`summary.csv`中的`duration_seconds`。

该执行器的终端摘要不包含分数，只显示任务完成情况、智能体数、实际调用数、验证
错误数和运行时间。

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

### 2.1 实时天气实验（推荐）

`travel_live.json`是读者复现实验的默认配置。它把出发日期解析为运行日之后
第3天，行程持续4天，并由Weather Agent调用Open-Meteo获取实时天气。正式配置
在验证开启和关闭模式下各执行100次。小规模检查命令为：

```powershell
uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_live.json --repetitions 1
```

小规模命令运行2项任务，每项任务的等待上限为30分钟，任务等待时间最多约60分钟；
正式命令运行200项任务，任务等待上限合计为100小时。两者还需要计算服务启动和
停止时间。建议正式实验使用第4节的中断恢复功能。

在线数据、模型输出和外部服务状态会随运行时间变化，因此该模式复现实验流程、
协议验证和指标计算方法，不要求具体文本与论文数值完全一致。

### 2.2 历史天气数据回放（可选）

`travel_paper_replay.json`继承100次正式实验配置，并使用
`fixtures/weather_beijing_2026-08-10_13.json`中保存的原实验天气响应：

```powershell
uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_paper_replay.json
```

天气回放固定了外部天气输入，但不会绕过Weather Agent。Host仍通过A2A发送
天气查询，Weather Agent接收请求后读取本地天气数据并通过A2A返回结果。Host和
远程智能体仍由大语言模型驱动，因此重新执行得到的文本和个别任务结果可能发生
变化。

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

评价器默认对每次模型请求设置180秒超时，失败时最多尝试3次。总耗时随结果目录中
的任务数近似线性增加；可先添加`--limit 1`完成一次连接和格式检查。

评价器只读取Host最终回复，不读取验证模式、过程指标或论文结论，避免将组别信息
泄露给评价模型。每项判断均保存直接证据、缺失原因和模型原始JSON回复。

## 4. 中断恢复

长时间实验可从已有结果目录继续：

```powershell
uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_live.json `
  --resume-dir experiments\results\travel-live-YYYYMMDD-HHMMSS
```

执行器读取已有 `run.json`，跳过已经完成的模式、提示词和重复编号，只运行缺失项。

## 5. 全部输出文件

### 5.1 配置预检

- `resolved_prompts.json`：解析动态日期等模板字段后的实际提示词；
- `reproducibility.json`：Git提交、Python与uv版本、操作系统和生成时间。

### 5.2 正式实验顶层文件

- `config.snapshot.json`：展开配置继承并应用命令行参数后的完整配置、环境和开始时间；
- `summary.csv`：逐项任务的完成情况、通信、覆盖、运行时间等原始指标；
- `aggregate.csv`：按验证模式计算的指标总值和均值；
- `paired_comparison.csv`：相同提示词与重复编号的两组配对指标及差值，仅在配对完整
  时生成；
- `manifest.json`：实验名称、完成时间、任务数和结果目录。

### 5.3 模式级和单项任务文件

- `<模式>/_service_logs/<服务名>.log`：该模式下每个Host或Remote Agent从启动到停止
  的完整日志；
- `<模式>/<任务>/prompt.txt`：发送给主控智能体的初始提示词；
- `<模式>/<任务>/final_response.txt`：主控智能体的最终可见回复；
- `<模式>/<任务>/run.json`：任务标识、完成状态、实际运行秒数和全部计算指标；
- `<模式>/<任务>/messages.json`：Host会话接口返回的原始消息；
- `<模式>/<任务>/events.json`：该任务期间Host新增的原始事件；
- `<模式>/<任务>/tasks.json`：该任务期间Host新增的A2A任务；
- `<模式>/<任务>/tool_calls.json`：从事件中提取的工具调用；
- `<模式>/<任务>/communications.csv`：消息与事件合并后的时间序列；
- `<模式>/<任务>/a2a_trace.json`：实际跨越Host通信边界的A2A请求与响应载荷；
- `<模式>/<任务>/a2a_trace.csv`：A2A边界载荷的表格形式；
- `<模式>/<任务>/process_logs/<服务名>.log`：完整服务日志中属于该项任务的时间片。

### 5.4 工具调用异常案例附加文件

- `validation_events.csv`：全部任务的验证错误与反馈重试相关事件；
- `error_counts.csv`：按模式、服务、阶段和错误码统计的事件次数；
- `error_aggregate.csv`：按模式汇总的验证错误、重试、成功恢复、重试耗尽和最终阻断
  次数；
- `<模式>/<任务>/validation_events.json`：单项任务的完整验证事件；
- `<模式>/<任务>/validation_events.csv`：同一验证事件的表格形式。

### 5.5 AI输出质量评价文件

- `ai_judge_prompt.preview.txt`：`--dry-run`生成的首项任务评价提示词；
- `ai_judgments.json`：逐项判断、证据、原因和模型原始回复；
- `ai_output_scores.csv`：逐任务六项0/1判断和0～6分输出质量得分；
- `ai_score_aggregate.csv`：按验证模式汇总的六项满足率和平均得分；
- `ai_judge_manifest.json`：评价配置、提示词路径、任务数和运行环境。
