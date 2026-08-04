# Remote Agent 2 — Weapon Library Asset Agent (`op2`)

链路中的 **第 2 段**：武器库资产智能体。

> 输入 Key：黑客组织 / 僵尸网络标签
> 输出 Value：该组织近期最常利用的「漏洞编号（CVE ID）」

收到 host 传来的威胁组织标签后，本智能体通过内置 `mapping` 表查到对应的 CVE 编号
（例如 `CVE-2026-9999`），并以固定格式 `[result: <cve>]` 返回。
该 CVE 即作为下一站（防御策略智能体 `op3`）的输入 key。

底层实现与原框架完全一致：仅依据传入的 key 在数据库中做一次 value 查询；
`mapping` 表为 `(key TEXT, value TEXT)`，`query_database` 与领域查询工具仍保留。

## 可追踪示例链路（贯穿三段）

| 输入标签            | 本段输出 CVE   | 下一段（op3）输出脚本            |
|----------------------|-----------------|--------------------------------|
| Advanced-Threat-Group-X | CVE-2026-9999   | Block_Rule_Protocol_v3.sh      |
| Advanced-Threat-Group-A | CVE-2026-9001   | Drop_Payload_Signature_v1.sh   |
| Advanced-Threat-Group-B | CVE-2026-9123   | Isolate_Host_Rule_v2.sh        |
| Advanced-Threat-Group-C | CVE-2026-8888   | Quarantine_File_Rule_v5.sh      |
| Advanced-Threat-Group-D | CVE-2026-9500   | Block_C2_Beacon_v4.sh          |

## 使用方式

```bash
uv run .
```

默认监听端口 `10302`。

## 字段说明

- 工具：`lookup_attack_cve(group_label)` —— 组织标签 → CVE
- 库表：`op2_data.db` 中的 `mapping(key, value)`
