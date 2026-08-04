# Remote Agent 3 — Defense Strategy Agent (`op3`)

链路中的 **第 3 段（终点）**：防御策略智能体。

> 输入 Key：漏洞编号（CVE ID）
> 输出 Value：防火墙 / 安全拦截系统应自动下发的「安全补丁 / 策略规则脚本」

收到 host 传来的 CVE 编号后，本智能体通过内置 `mapping` 表查到对应的防御规则脚本
（例如 `Block_Rule_Protocol_v3.sh`），并以固定格式 `[result: <script>]` 返回。
该脚本即链路的最终交付结果，由 host 回传给用户。

底层实现与原框架完全一致：仅依据传入的 key 在数据库中做一次 value 查询；
`mapping` 表为 `(key TEXT, value TEXT)`，`query_database` 与领域查询工具仍保留。

## 可追踪示例链路（贯穿三段）

| 输入 CVE      | 本段（终点）输出脚本           |
|---------------|--------------------------------|
| CVE-2026-9999 | Block_Rule_Protocol_v3.sh      |
| CVE-2026-9001 | Drop_Payload_Signature_v1.sh   |
| CVE-2026-9123 | Isolate_Host_Rule_v2.sh        |
| CVE-2026-8888 | Quarantine_File_Rule_v5.sh      |
| CVE-2026-9500 | Block_C2_Beacon_v4.sh          |

## 使用方式

```bash
uv run .
```

默认监听端口 `10303`。

## 字段说明

- 工具：`lookup_defense_strategy(cve_id)` —— CVE → 防御脚本
- 库表：`op3_data.db` 中的 `mapping(key, value)`
