# 数据字段与复核方法

`records.json` 一条记录对应一次运行，`run_id` 是唯一键。`task_index` 为 0–29；每个 condition/round 恰好各包含 30 个不同题号。`round` 是该条件内轮号，不能暗示三种条件在同一时间配对运行。

| 字段 | 含义 |
|---|---|
| condition | baseline、mpst、mpst_contract |
| artifact_pass | 实际独立评估中的最终布尔结果 |
| elapsed_seconds | 原 run_result 的运行耗时，不含独立评审 |
| evaluation_source | 实际使用的评审证据，相对于研究归档根目录 |
| run_result_source | 原运行记录，文本路径已归一化 |
| supplemental_evaluation | 是否用补评填补原评估的缺失值，仅 2 条 |
| published_python_files | 归档的 Python 源文件数，不代表评审通过 |

`runs/` 按 condition/round/task 存放文件：`run_result.json`、`evaluation.json`、可选补评、契约审计及 `artifact/` 文本产物。归档保留原运行状态和失败诊断，但主表仅使用最终评估结果。

`manifests/` 是确定性契约批次的配置及核对记录。`provenance.json` 中每项含来源标识、原始与发布 SHA-256；文本路径改写后两种哈希可能不同。

从上层目录执行 `python scripts/summarize.py --verify-hashes` 会校验逐题结果、补评条件、每轮题号覆盖、总数和所有导出文件的发布哈希，并重算 JSON、CSV、Markdown 汇总。
