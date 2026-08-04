# Remote Agent 1 — IP Intelligence Agent (`op1`)

链路中的 **第 1 段**：IP 情报智能体。

> 输入 Key：攻击源 IP
> 输出 Value：该 IP 所属的「恶意黑客组织 / 僵尸网络标签」

收到 host 发来的攻击源 IP 后，本智能体通过内置 `mapping` 表查到对应的威胁组织标签
（例如 `Advanced-Threat-Group-X`），并以固定格式 `[result: <label>]` 返回。
该 label 即作为下一站（武器库资产智能体 `op2`）的输入 key。

底层实现与原框架完全一致：仅依据传入的 key 在数据库中做一次 value 查询；
`mapping` 表为 `(key TEXT, value TEXT)`，`query_database` 与领域查询工具仍保留。

## 可追踪示例链路（贯穿三段）

| 攻击源 IP      | op1 输出标签             | op2 输出 CVE    | op3 输出脚本                   |
|----------------|--------------------------|-----------------|--------------------------------|
| 203.0.113.10   | Advanced-Threat-Group-X  | CVE-2026-9999   | Block_Rule_Protocol_v3.sh      |
| 198.51.100.20  | Advanced-Threat-Group-A  | CVE-2026-9001   | Drop_Payload_Signature_v1.sh   |
| 192.0.2.30     | Advanced-Threat-Group-B  | CVE-2026-9123   | Isolate_Host_Rule_v2.sh        |
| 203.0.113.40   | Advanced-Threat-Group-C  | CVE-2026-8888   | Quarantine_File_Rule_v5.sh      |
| 198.51.100.50  | Advanced-Threat-Group-D  | CVE-2026-9500   | Block_C2_Beacon_v4.sh          |

例如 host 以 `203.0.113.10` 作为 key 调用 op1，得到 `[result: Advanced-Threat-Group-X]`。

## 使用方式

```bash
uv run .
```

默认监听端口 `10399`。

## 字段说明

- 工具：`lookup_threat_group(ip_address)` —— IP → 威胁组织标签
- 库表：`op1_data.db` 中的 `mapping(key, value)`
