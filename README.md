# MPST-A2A Validator

面向 A2A 多智能体通信的多方会话类型（MPST）协议投影与运行时验证框架。

框架从全局协议生成各角色的局部协议，并在 Host 与 Remote Agent 通信过程中验证消息顺序、通信方向、标签、数据类型、会话状态以及未执行的工具调用，防止协议违规消息推进会话状态。

## 项目结构

- `host-platform/frontend/ui/`：Mesop UI 与前端 API 服务。
- `host-platform/backend/`：Host Agent、A2A 连接、协议初始化及 Host 侧验证。
- `protocol-projection/`：全局类型解析以及 subset/classical projection 引擎。
- `mpst-runtime/`：共享验证器、会话状态、消息检查器和验证执行器。
- `remote-agents/op1/`：IP Intelligence Agent。
- `remote-agents/op2/`：Weapon Library Asset Agent。
- `remote-agents/op3/`：Defense Strategy Agent。
- `docs/`：框架设计说明。
- `tests/`：运行时验证测试。

## 默认端口

- UI / Host：`12000`
- OP1：`10399`
- OP2：`10302`
- OP3：`10303`

## 启动

在四个终端中分别执行：

先在每个终端中设置相同的验证模式。实验组使用：

```powershell
$env:VALIDATION_ENABLED="true"
```

对照组使用：

```powershell
$env:VALIDATION_ENABLED="false"
```

`true`为默认值。切换模式后必须重启Host和三个Remote Agent，
并创建新会话，避免复用已有协议状态。

```powershell
cd D:\Projects\mpst-a2a-validator\remote-agents\op1
uv run --python 3.13 .
```

```powershell
cd D:\Projects\mpst-a2a-validator\remote-agents\op2
uv run --python 3.13 .
```

```powershell
cd D:\Projects\mpst-a2a-validator\remote-agents\op3
uv run --python 3.13 .
```

```powershell
cd D:\Projects\mpst-a2a-validator\host-platform\frontend\ui
uv run --python 3.13 main.py
```

### 验证模式差异

- `VALIDATION_ENABLED=true`：初始化协议，验证Host和Remote Agent消息，
  拦截格式错误、空消息及未完成的Tool Call，并在合法时推进会话状态。
- `VALIDATION_ENABLED=false`：跳过协议初始化和所有验证干预，消息原样发送，
  不拦截、不重试，也不维护协议状态，用作同代码基线实验。

四个进程启动时都会输出`[VALIDATION MODE]`日志。一次实验中四个进程的
`enabled`值必须完全一致。

## 验证

```powershell
cd D:\Projects\mpst-a2a-validator
uv run --python 3.13 python -m unittest tests.test_mpst_runtime -v
```

需要重建三级威胁分析映射数据时执行：

```powershell
uv run --python 3.13 python remote-agents\rebuild_mappings.py
```

## 旅行规划案例

第二个案例已接入 Weather、Guide、Transport Select、Train、Flight、
Hotel、Ticket、Public Transport 和 Budget 共 9 个远程 Agent。它们与
OP1—OP3 共用同一套 `VALIDATION_ENABLED=true/false` 开关和验证运行时。

完整端口、启动、注册和配对实验提示词见
`docs/travel-case.md`。

### 自动执行与通信记录

旅行规划的配对实验可以由脚本自动启动两组服务、注册 Agent、创建独立
会话、发送提示词、等待完成并导出应用层通信记录：

```powershell
uv run --python 3.13 python scripts\experiment_runner.py --config experiments\travel_experiment.json
```

建议先用 `--repetitions 1` 完成一次小规模检查。输出位于
`experiments/results/`，具体文件及评分口径见 `experiments/README.md`。
