# 论文结果最小复现数据包

`paper-results/travel-final-output-large-20260731-173233/`由论文旅行规划正式实验
结果导出，包含200项任务的逐项指标和Host最终回复。为控制仓库体积并避免发布
无关运行日志，数据包不包含中间模型事件和完整进程日志。

可以直接检查AI评价提示词：

```powershell
uv run --frozen --python 3.13 python scripts\evaluate_outputs.py `
  reproduction\paper-results\travel-final-output-large-20260731-173233 `
  --dry-run
```

执行全部AI评价：

```powershell
uv run --frozen --python 3.13 python scripts\evaluate_outputs.py `
  reproduction\paper-results\travel-final-output-large-20260731-173233
```

`final_outputs.jsonl`为便于独立审计而提供的扁平化最终回复集合；各模式目录中的
最小 `run.json` 和 `messages.json` 保持了与评价器相同的输入结构。

如需从新的完整实验目录生成相同结构：

```powershell
uv run --frozen --python 3.13 python scripts\export_reproduction_bundle.py `
  experiments\results\<源目录> reproduction\paper-results\<目标目录>
```
