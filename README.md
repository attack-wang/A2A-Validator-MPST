# MPST-A2A Validator

面向 A2A 多智能体通信的多方会话类型（MPST）协议投影与运行时验证框架。
框架从全局协议生成各角色的局部协议，并在 Host 与 Remote Agent 的通信边界
验证消息顺序、通信方向、通信对象、标签、数据类型、会话状态及未完成的工具调用。

本仓库提供论文两个案例的自动执行入口：

1. OP1→OP2→OP3 工具调用异常案例；
2. 九个远程智能体参与的旅行规划流程案例。

## 1. 环境要求

以下流程已在 Windows PowerShell、Python 3.13 和 `uv` 下验证。

- Git；
- Python 3.13（可以由 `uv` 自动安装）；
- [uv](https://docs.astral.sh/uv/)；
- [Ollama](https://ollama.com/download)；
- 可访问 Ollama Cloud 和 Open-Meteo 的网络环境。

克隆仓库并进入根目录：

```powershell
git clone https://github.com/attack-wang/A2A-Validator-MPST.git
cd A2A-Validator-MPST
uv python install 3.13
```

实验配置固定使用 `glm-5.2:cloud`、`qwen3.5:cloud` 和
`kimi-k2.6:cloud`。首次运行前登录 Ollama，并确认本地服务可以调用模型：

```powershell
ollama signin
ollama serve
```

在另一个终端中执行模型冒烟测试：

```powershell
ollama run glm-5.2:cloud "仅回复 OK"
ollama run qwen3.5:cloud "仅回复 OK"
ollama run kimi-k2.6:cloud "仅回复 OK"
```

## 2. 项目结构

- `host-platform/`：Host Agent、Mesop UI、A2A连接及Host侧验证；
- `remote-agents/`：两个案例使用的远程智能体；
- `protocol-projection/`：全局类型解析及投影工具；
- `mpst-runtime/`：协议自动机、消息检查器和验证执行器；
- `scripts/experiment_runner.py`：旅行规划自动实验执行器；
- `scripts/security_experiment_runner.py`：工具调用异常自动实验执行器；
- `scripts/evaluate_outputs.py`：旅行规划最终输出的AI评价器；
- `experiments/`：固定实验配置、评价提示词和天气回放数据；
- `tests/`：运行时、实验执行器和评价器测试；
- `reproduction/`：论文结果的最小复现数据包。

## 3. 安装检查与测试

项目及各子项目均提交了 `uv.lock`。建议保留锁文件并使用 `--frozen`，避免
实验期间依赖版本发生变化。

```powershell
uv run --frozen --python 3.13 python -m unittest discover -s tests -v
```

需要重新生成OP1、OP2和OP3的固定映射数据库时执行：

```powershell
uv run --frozen --python 3.13 python remote-agents\rebuild_mappings.py
```

## 4. 验证模式

自动实验执行器会分别设置以下两种模式，并在切换模式时重启全部服务、创建
新会话：

- `VALIDATION_ENABLED=true`：启用协议初始化和运行时验证；
- `VALIDATION_ENABLED=false`：不初始化或维护协议状态，作为同代码基线。

错误反馈重试由以下变量控制：

- `MPST_ERROR_FEEDBACK_ENABLED=true`：把可修正错误转换为模型反馈；
- `MPST_ERROR_FEEDBACK_MAX_RETRIES=2`：每次输出最多纠正两次；
- 将重试次数设为`0`：保留检测和阻断，关闭重新生成。

## 5. 案例一：工具调用异常

该案例以一个固定IP查询作为执行链的唯一初始输入。主控智能体随后依次调用
IP情报、武器库资产和防御策略智能体，并自动将上一阶段的真实结果作为下一阶段
输入。正式实验将这条完整执行链在验证器开启和关闭模式下分别重复50次。

先检查配置和实际提示词，不启动服务或调用模型：

```powershell
uv run --frozen --python 3.13 python scripts\security_experiment_runner.py --dry-run
```

运行一次完整执行链的小规模检查。命令会在验证器开启和关闭模式下各生成1项
任务记录，共2项：

```powershell
uv run --frozen --python 3.13 python scripts\security_experiment_runner.py --repetitions 1
```

运行论文规模实验：

```powershell
uv run --frozen --python 3.13 python scripts\security_experiment_runner.py
```

主要结果包括 `summary.csv`、`error_counts.csv`、`error_aggregate.csv`、
`validation_events.csv` 和每次任务的原始日志。指标定义见
[experiments/README.md](experiments/README.md)。

## 6. 案例二：旅行规划

### 6.1 实时天气实验（推荐）

`travel_live.json`是读者复现实验时的默认配置。脚本根据运行日期自动生成从
第3天开始的连续4天行程，并由Weather Agent调用Open-Meteo接口获取实时天气。
先预检动态日期和配置，不启动服务或调用模型：

```powershell
uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_live.json --dry-run
```

随后运行一次小规模检查。验证器开启和关闭模式各执行1次：

```powershell
uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_live.json --repetitions 1
```

正式配置在两种模式下各执行100次，共200项任务：

```powershell
uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_live.json
```

实时天气、模型输出和外部服务状态会随运行时间变化。读者可以据此复现智能体
组成、A2A通信过程、协议约束、实验流程和指标计算方法，但具体文本及统计数值
可能与论文实验存在差异。

### 6.2 历史天气数据回放（可选）

`travel_paper_replay.json` 固定使用论文实验期间保存的北京天气工具响应，避免
历史日期无法由实时预报接口查询。该配置只用于需要固定外部天气输入时的补充
验证；Host仍通过A2A调用Weather Agent，Weather Agent仅将在线接口替换为本地
天气数据文件。

```powershell
uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_paper_replay.json --dry-run

uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_paper_replay.json --repetitions 1

uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_paper_replay.json
```

实时实验运行中断后可从原目录继续：

```powershell
uv run --frozen --python 3.13 python scripts\experiment_runner.py `
  --config experiments\travel_live.json `
  --resume-dir experiments\results\travel-live-YYYYMMDD-HHMMSS
```

## 7. AI输出质量评价

实验执行完成后，先生成一条评价提示词预览，不调用评价模型：

```powershell
uv run --frozen --python 3.13 python scripts\evaluate_outputs.py `
  experiments\results\travel-live-YYYYMMDD-HHMMSS --dry-run
```

确认后对全部最终回复执行六项内容评价：

```powershell
uv run --frozen --python 3.13 python scripts\evaluate_outputs.py `
  experiments\results\travel-live-YYYYMMDD-HHMMSS
```

评价器使用固定模型、温度、种子、提示词和JSON字段，输出：

- `ai_judgments.json`：原始回复与逐项证据；
- `ai_output_scores.csv`：每项任务的六项0/1评价及0～6分总分；
- `ai_score_aggregate.csv`：验证开启与关闭两组的汇总结果；
- `ai_judge_manifest.json`：评价模型、提示词和运行环境记录。

## 8. 结果与复现边界

每次运行都会保存解析后的提示词、配置快照、Git提交号、Python/uv版本、
操作系统、通信记录和进程日志。天气回放能够固定外部天气输入；大语言模型仍具有
运行时随机性，因此独立运行应主要复现执行流程、指标计算方法和总体趋势，不要求
每次生成文本与论文原始文本逐字一致。论文原始输出的最小数据包位于
`reproduction/paper-results/`，可以直接重新执行AI评价和表格汇总。

运行输出默认保存在 `experiments/results/`，该目录不会提交密钥或临时日志。
