# ChatDev：MPST 与内容契约实验归档

此目录集中保存 ChatDev 对比实验、确定性内容契约实现，以及全局类型引用契约的新实现。原项目及历史实验没有被移动或覆盖。实验生成模型为 `glm-5.3-flash:cloud`，独立产物评审使用 `gpt-oss:120b-cloud`；本次整理没有重新调用生成或评审模型。

## 实验结果

| 方案 | 轮数 | 最终产物验收通过 | 最终通过率 | 平均运行耗时 |
|---|---:|---:|---:|---:|
| ChatDev 基线 | 10 | 88/300 | 29.33% | 300.09 秒 |
| ChatDev + MPST | 10 | 91/300 | 30.33% | 326.98 秒 |
| ChatDev + MPST + 内容契约 | 12 | 200/360 | 55.56% | 156.93 秒 |

每轮重复同一组 30 题，合计 960 次运行；不是 960 个不同题目。按照本次汇报口径，仅比较最终产物结果，原始记录仍保留运行诊断用于追溯。

“通过率”是自动产物验收代理指标，包含编译、项目完整性及独立模型评审，不是标准答案测试集正确率。耗时不包含独立产物评审，包含超时和提前停止。契约版本还改变了交付提示和修复逻辑，运行日期也不同，因此不能将所有正确率和速度差异单独归因于契约验证。

契约 R1、R3 各有一条原评审接口异常，补评只填补原来的缺失值；两份原始结果及两份补评均保存。完整分轮数据见 [reports/results.md](reports/results.md)，逐题表见 [reports/records.csv](reports/records.csv)。

## 目录

```text
source/chatdev-mpst/       基线/仅 MPST 适配器与原实验脚本
source/pure-contract/      做过真实 12 轮实验的冻结确定性契约版本
source/inline-contract/    GT 中 @contract 引用的新投影版本
data/tasks.json           同一组 30 道题目
data/records.json         960 条统一索引，指向逐题证据
data/runs/                逐题原结果、评审、契约审计、生成产物
data/manifests/           契约批次配置、源码哈希及评审说明
data/provenance.json      导出文件的原始哈希与发布哈希
reports/                  可重新计算的结果和耗时说明
scripts/                  离线核对、测试与新实验启动工具
presentations/            简版结果汇报与编码契约讲解 PPT
```

完整 console/application 日志放在同仓库 [GitHub Releases](https://github.com/attack-wang/A2A-Validator-MPST/releases) 的 `chatdev-experiment-traces-960.zip`，避免把大型日志存入 Git 历史。附件哈希见 [data/archive-manifest.json](data/archive-manifest.json)。发布副本将个人本地绝对路径改成仓库相对路径，同时记录导出前后 SHA-256；本地原文件保持原样。

## 三种代码版本的关系

- `chatdev-mpst`：基线与仅 MPST 使用同一 ChatDev 源码，通过环境开关决定是否校验通信顺序。上游来自 ChatDev 1.0 分支，原实验记录记载提交 `31fd994416a251ecdeb1f0a73c329271743bfb56`。适配器是整理时的本地快照，基线批次没有逐轮冻结完整源码，因此不声称可恢复每个历史批次的精确代码版本。
- `pure-contract`：从受保护的独立实验目录复制，97 个实验源码/配置文件逐一匹配原冻结哈希。以上 200/360 对应这个版本；没有 JEV/TEV 模型裁决。
- `inline-contract`：全局类型直接引用注册表中的契约名，投影后的发送/接收转换携带 `contract_ref`、`payload_schema` 和通信编号，状态提交前执行契约，失败则不推进状态。此版本只做过离线验证，**尚未运行真实 30 题**，不能把 200/360 当作它的实验结果。

新版本示例：

```text
CodeReviewer -> Coordinator :
    reviewResult(ReviewReport) @contract("chatdev.review.v1").
```

Coordinator 协议仍是阶段结果的协调抽象，并非 ChatDev 全部原生角色对话拓扑。schema 名由实际领域检查函数解释，没有引入通用 JSON Schema 执行引擎。更多实现说明见 [docs/contracts.md](docs/contracts.md)。

## 离线复核

只计算统计需要 Python 标准库：

```powershell
python scripts/summarize.py --verify-hashes
```

离线契约测试使用 Python 3.11：

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-offline.txt
.venv/Scripts/python -c "import tiktoken; tiktoken.encoding_for_model('gpt-4o'); tiktoken.encoding_for_model('gpt-4')"
.venv/Scripts/python scripts/run_offline_tests.py --variant pure-contract
.venv/Scripts/python scripts/run_offline_tests.py --variant inline-contract
.venv/Scripts/python source/inline-contract/export_projection.py
```

Linux/macOS 将 `.venv/Scripts/python` 替换成 `.venv/bin/python`。离线测试阻止 socket 连接，生成模型由固定输出代替，结果写到忽略目录 `output/`。生成代码作为历史研究数据保存；复核汇总不会执行这些代码。

安装步骤中的 tokenizer 预下载不是模型调用，用于避免离线测试尝试下载词表。完整测试包含真实 Tk 事件循环，Linux/macOS 需要可用的桌面显示或虚拟显示；仓库 CI 使用 Windows。

整理后已用全新依赖环境验证：冻结契约 81 项、新投影版本 97 项，全部通过且没有网络连接尝试。仓库 CI 自动复核逐题数据与两套离线测试。

## 新实验

先在 shell 中配置 `.env.example` 列出的连接参数；文件不会自动加载。运行 `scripts/run_experiment.py --help` 查看使用方式。新运行必须使用全新的 batch 名，结果写到各源码版本自己的忽略目录，不能覆盖归档的 `data/runs/`。这一操作会真实调用生成模型；独立评审另行执行原版 `benchmarks/programdev/evaluate.py`。

例如，从归档根目录启动一题，然后独立评审：

```powershell
.venv/Scripts/python scripts/run_experiment.py --condition mpst_contract --index 0 --batch-name fresh_contract_r1
.venv/Scripts/python source/pure-contract/benchmarks/programdev/evaluate.py --framework chatdev --run-tag fresh_contract_r1 --judge-model gpt-oss:120b-cloud
```

条件可选 `baseline`、`mpst`、`mpst_contract`、`inline_contract`。发布版启动工具使用当前 Python，方便跨机器运行；原历史启动脚本仍作为来源证据保留。历史结果不是由这个新启动工具重新产生的。

## 来源与许可

第三方 ChatDev/CAMEL 的版权头及 [Apache-2.0 LICENSE](source/pure-contract/integrations/ChatDev1.0/LICENSE) 保留。投影器作者说明见 [AUTHORS.txt](source/pure-contract/protocol-projection/AUTHORS.txt)。这是原仓库的研究附录，不对第三方代码或模型生成的软件产物另行重新许可。许可证和来源说明见 [docs/provenance.md](docs/provenance.md)。
