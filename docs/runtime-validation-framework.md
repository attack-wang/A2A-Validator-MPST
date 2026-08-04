# 第6章 基于本地类型的运行时验证框架

前文提出的泛化投影类型系统能够从全局通信协议自动生成各参与角色对应的局部类型（Local Type），并通过类型一致性判断智能体行为是否符合预定义协议。然而，在开放式多智能体系统中，智能体通常由不同开发框架、不同大语言模型以及不同工具链实现，其内部执行逻辑无法完全受静态类型系统约束。大语言模型固有的随机性、工具调用的不可预测性以及第三方服务的不确定性，都可能使智能体在运行时产生偏离协议的通信行为。因此，仅依靠编译阶段的协议检查难以保证运行过程中智能体交互行为始终满足协议要求。

针对这一问题，本章提出一种基于局部类型驱动的运行时验证框架（Local Type-driven Runtime Verification Framework）。该框架将第5章生成的局部类型转换为轻量级协议验证器（Protocol Validator），并部署于各智能体通信边界，对运行过程中的消息交互进行动态检查。当智能体发送或接收消息时，Validator 根据当前协议状态判断该通信行为是否合法，并在检测到协议违约时阻止非法消息传播，从而将协议一致性保证从“静态推导”延伸到“动态执行”。

本章结构如下：6.1 节介绍框架总体架构；6.2 节介绍基于局部类型的验证器生成机制；6.3 节定义运行时消息验证过程；6.4 节讨论协议违约检测；6.5 节给出框架性质分析。

## 6.1 框架总体架构

本文提出的运行时验证框架主要由三个阶段组成：协议建模、协议编译与运行时验证。三个阶段形成一条从形式化规约到在线检查的闭环，如图6-1所示。

### 6.1.1 协议建模阶段（Protocol Specification）

用户首先根据任务需求定义多智能体之间的全局通信协议：

$$
G \;=\; \text{Global Type}
$$

其中，全局类型描述所有参与角色之间可能发生的通信行为，包括消息方向、消息标签、数据类型以及控制流结构（顺序、选择、递归等）。全局类型是整个验证框架的单一事实来源（single source of truth），所有后续验证逻辑均由其派生，从而避免人工编写监控规则所引入的一致性风险。

### 6.1.2 协议编译阶段（Protocol Compilation）

通过第5章定义的泛化投影机制：

$$
G \;\xrightarrow{\;\text{Projection}\;}\; L_p
$$

将全局协议转换为每个角色 $p$ 对应的局部类型 $L_p$。随后，根据局部类型自动生成对应的 Validator。该编译过程在智能体部署前离线完成，其正确性由第5章的投影保真性定理保证。

### 6.1.3 运行时验证阶段（Runtime Verification）

在智能体运行过程中，Validator 位于 Agent 通信接口之前，对所有 A2A 消息进行拦截和验证。Validator 维护该角色在协议中的当前状态，并在每次发送或接收时判定该通信是否为当前状态所允许的合法转移。

整体架构如图6-1所示。

```
            ┌───────────────────────────┐
            │      Global Type  G        │
            └─────────────┬─────────────┘
                          │  Generalized Projection
            ┌─────────────┴─────────────┐
            │   L_A      L_B      L_C    │   (Local Types)
            └──────┬───────┬───────┬─────┘
                   │       │       │
          ┌────────┘       │       └────────┐
          ▼                ▼                ▼
     Validator_A      Validator_B      Validator_C
          │                │                │
          ▼                ▼                ▼
      Agent A          Agent B          Agent C
          │                │                │
          └────────────────┼────────────────┘
                           │
                    A2A Messages (拦截/验证)
```
<div align="center">图6-1　基于局部类型的运行时验证框架总体架构</div>

与传统基于规则匹配的监控机制不同，本文框架中的 Validator 并非人工定义，而是由形式化协议自动生成，因此能够保证验证逻辑与通信协议保持一致：当协议演化时，只需重新执行投影与生成，各 Validator 即可同步更新，无需手工维护分散的监控规则。

## 6.2 基于局部类型的验证器生成

### 6.2.1 Local Type 的状态化表示

为了支持运行时验证，本文首先将局部类型转换为有限状态转换系统（Finite State Transition System）。局部类型中的递归变量、顺序组合与选择分支均可被规范化为状态与转移，从而得到一个可逐步执行的协议自动机。

给定角色 $p$ 的局部类型 $L_p$，定义其对应状态机：

$$
M_p = (S,\; s_0,\; \delta)
$$

其中：

- $S$ 表示协议状态集合，每个状态对应局部类型中一个待执行的通信位置；
- $s_0 \in S$ 表示初始状态，对应局部类型的起始位置；
- $\delta$ 表示状态转移函数，由局部类型的语法结构归纳生成。

例如，对于输出型局部类型：

$$
p!q(\text{label}:T).L
$$

其对应状态转换：

$$
s_i \;\xrightarrow{\;\text{send}(q,\,\text{label},\,T)\;}\; s_j
$$

表示角色 $p$ 当前状态允许向角色 $q$ 发送携带类型 $T$、标签 $\text{label}$ 的消息，执行后进入后继状态 $s_j$。

同理，对于输入型局部类型：

$$
p?q(\text{label}:T).L
$$

对应：

$$
s_i \;\xrightarrow{\;\text{receive}(q,\,\text{label},\,T)\;}\; s_j
$$

表示角色 $p$ 当前状态允许接收来自角色 $q$ 的对应消息。

对于选择型局部类型 $L_1 \oplus L_2$，其在同一状态上产生多条出边，分别对应不同分支；对于递归型局部类型 $\mu\mathbf{t}.L$，其后继状态回指递归入口状态，从而以有限状态刻画无限执行。因此，每个 Agent 的 Local Type 均可转换为一个协议自动机。

在实现层面，本文采用“协议位置（Protocol Position）”作为状态的等价表示：每个位置记录当前期望的动作类型、消息标签、数据类型、对端角色以及后继位置。这种位置驱动的表示与状态机等价，但更贴近局部类型的语法结构，便于由投影结果直接编译生成。位置与状态的对应关系为 $s_i \leftrightarrow \text{pos}_i$，转移 $\delta$ 由 `next_position` 字段显式编码。

### 6.2.2 Validator 生成

基于上述状态机，每个 Agent 部署一个对应的 Validator。Validator 包含三个核心组件：

**（1）Protocol State（协议状态）**

记录当前 Agent 所在协议状态：

$$
s_i \in S
$$

该状态在每次成功验证后沿 $\delta$ 推进，并保留历史轨迹以支持调试与审计。

**（2）Transition Table（转移表）**

保存当前状态允许的通信行为 $\delta(s_i)$。转移表由局部类型编译得到，每个表项描述一个合法转移的四元组（动作、对端角色、标签、数据类型）。例如，对于旅行规划场景中 Host 角色的局部类型，其转移表片段如表6-1所示。

<div align="center">表6-1　Host 角色转移表示例</div>

| Current State | Action | Receiver/Peer | Label | Type |
|:---:|:---:|:---:|:---:|:---:|
| $s_0$ | Send | FlightAgent | request | JSON |
| $s_1$ | Receive | FlightAgent | response | JSON |
| $s_2$ | Send | HotelAgent | request | JSON |
| $s_3$ | Receive | HotelAgent | response | JSON |
| $s_4$ | Send | WeatherAgent | request | JSON |
| $s_5$ | Receive | WeatherAgent | response | JSON |

**（3）Message Checker（消息检查器）**

负责解析实际 A2A 消息，并检查如下四项一致性：

1. 发送角色是否匹配；
2. 接收角色是否匹配；
3. 消息标签是否匹配；
4. 数据类型是否匹配。

其中数据类型检查在本框架中被显式纳入：消息标签与数据类型构成二元组 $(\text{label},\,\tau)$，从而能够区分同名标签但承载不同数据结构的消息（详见 6.4.3 节）。

因此，一个 Validator 可以形式化表示为：

$$
V = (s,\; \delta,\; C)
$$

其中：

- $s$ 为当前状态；
- $\delta$ 为协议转移关系；
- $C$ 为消息检查函数，将一条实际消息映射为“匹配某一转移”或“不匹配任何转移”。

生成流程可归纳为：对 $L_p$ 进行语法遍历，为每个通信前缀创建一个位置（状态），依据前缀的动作类型填充转移表，并将后续类型链接为后继位置；遇到递归变量时，将后继指向递归入口位置。最终输出的是一个自包含的、可在智能体通信边界独立运行的 Validator。

## 6.3 运行时消息验证机制

在 A2A 通信过程中，所有消息均经过 Validator 检查。Validator 采取“先验证、后放行”的策略：只有通过验证的消息才会触发状态推进并被转发至智能体或对端，未通过验证的消息将被拦截并上报违约。

设当前 Agent 处于状态 $s_i$，收到消息：

$$
m = (p,\; q,\; l,\; \tau)
$$

其中：

- $p$：发送者；
- $q$：接收者；
- $l$：消息标签；
- $\tau$：数据类型。

Validator 执行如下验证过程。

**Step 1：消息解析（Message Parsing）**

首先解析 A2A 消息结构：

$$
m = (\text{sender},\; \text{receiver},\; \text{label},\; \text{type},\; \text{payload})
$$

提取通信元信息。对于带载荷的消息，进一步从 `payload` 中抽取标签与类型声明的实际取值，供类型检查使用。

**Step 2：协议匹配（Transition Matching）**

Validator 查询当前状态允许的转移集合 $\delta(s_i)$。若存在转移：

$$
s_i \;\xrightarrow{\;(p,\;l,\;\tau)\;}\; s_j
$$

即存在某个合法转移，其动作方向、对端角色、标签与数据类型均与消息 $m$ 一致，则通信合法；否则产生协议违约。

匹配判定由消息检查函数 $C$ 完成：

$$
C(m,\, s_i) =
\begin{cases}
s_j, & \exists\, s_j.\; s_i \xrightarrow{(p,l,\tau)} s_j \\
\bot, & \text{否则}
\end{cases}
$$

其中 $\bot$ 表示不匹配任何合法转移。

**Step 3：状态更新（State Update）**

验证成功后：

$$
s_i \;\longrightarrow\; s_j
$$

Validator 更新当前协议状态，并将该次转移记入历史轨迹；若后继为递归入口，则状态回指以支持循环协议。整个过程如图6-2所示。

```
   Incoming Message
          │
          ▼
   Message Parser ──► (sender, receiver, label, type, payload)
          │
          ▼
    Current State  ──► s_i
          │
          ▼
  Transition Matching ──► δ(s_i) 中是否存在 (p, l, τ) ?
          │
      ┌───┴───┐
      ▼       ▼
   Accept    Reject  ──► 记录违约、阻止消息
      │
      ▼
   State Update ──► s_i → s_j
```
<div align="center">图6-2　单次消息的运行时验证流程</div>

对于发送方向（send），Validator 在消息出栈前执行同样的匹配，从而在消息离开智能体之前即阻断非法发送；对于接收方向（receive），Validator 在消息入栈后、交付智能体处理前执行匹配。两个方向共用同一状态机与同一转移表，仅在动作方向上取反。

## 6.4 协议违约检测

由于 Validator 严格依据 Local Type 执行检查，因此能够检测多种智能体通信错误。本节给出四类典型违约及其检测原理。

### 6.4.1 角色遗漏（Missing Agent）

考虑旅行规划任务：

```
        Host
         │
   ┌─────┼─────┐
   ▼     ▼     ▼
 Flight  Hotel  Weather
```

协议要求 Host 依次向 Flight、Hotel、Weather 三个 Agent 发送请求并接收响应。如果 Host 未向 Weather Agent 发送请求，而直接生成最终结果，则其行为违反 Global Type。

通过投影，Host 的 Local Type 要求在对应阶段执行：

$$
\text{send}(\text{WeatherAgent},\; \text{request})
$$

当 Validator 推进至该状态时，若始终检测不到对应通信，则可判定协议未完成。具体而言，Validator 在会话结束时会检查当前状态是否到达协议允许的终止状态；若处于非终止状态且不再有合法转移发生，则上报“角色遗漏/协议未完成”违约。

### 6.4.2 消息顺序错误（Message Order Violation）

例如协议要求：

$$
\text{request} \;\rightarrow\; \text{response}
$$

但 Agent 在尚未发送 `request` 的情况下直接发送 `response`。由于当前状态 $s_i$ 的转移表 $\delta(s_i)$ 中不存在：

$$
\text{send}(\_,\; \text{response},\; \_)
$$

对应转移，因此 $C(m, s_i) = \bot$，Validator 拒绝该消息并保持状态不变，从而阻止顺序错乱的消息传播。

### 6.4.3 消息类型错误（Message Type Mismatch）

传统 MPST 仅关注消息标签 $\text{label}$，例如 `weather_result`。但本文扩展消息类型为二元组 $(\text{label},\,\tau)$，因此能够区分：

$$
\text{weather\_result} : \text{JSON}
\quad \text{与} \quad
\text{weather\_result} : \text{Text}
$$

当协议期望 `weather_result : JSON` 而实际消息载荷为纯文本时，类型检查函数判定数据类型不匹配，Validator 拒绝该消息。在实现中，该二元组以 `label__type` 的形式编码（如 `result__float`、`number__int`），并由内置类型校验器（int/float/number/str/bool 等）对载荷取值进行运行时检查，避免同标签不同数据结构导致的解析错误。

### 6.4.4 非法分支选择（Illegal Branch Selection）

对于发送方驱动的选择：

$$
p \rightarrow q_1 : l_1 \quad \text{或者} \quad p \rightarrow q_2 : l_2
$$

Local Type 在对应状态上产生两条出边，分别对应标签 $l_1$ 与 $l_2$。Validator 根据当前状态判断发送方是否具有该选择权限：若 Agent 选择了未定义的分支（例如向 $q_3$ 发送标签 $l_3$，或发送了不在当前转移表中的标签），则当前状态不存在对应转移，Validator 立即拒绝。对于接收方驱动的选择，Validator 同样依据当前状态中允许的分支集合对接收消息进行约束，确保分支选择在协议允许的范围之内。

## 6.5 框架性质分析

本节分析本文运行时验证框架的理论性质。

### 6.5.1 协议一致性保证

**定理 6.1（协议一致性）**　若全局类型 $G$ 可投影，并且所有 Agent 均按照对应 Local Type 执行，则运行过程中不会产生协议违约。

**证明**　由第5章的定义，所有 Agent 的行为满足：

$$
P_i : L_i
$$

而 Local Type 由投影得到：

$$
G \;\xrightarrow{\;\text{Projection}\;}\; L_i
$$

由投影保真性，$L_i$ 所允许的通信序列恰为 $G$ 中与角色 $i$ 相关的合法投影路径。因此，Agent 按 $L_i$ 执行的通信行为均属于 Global Type $G$ 所允许的通信路径。

Validator 仅检查 Local Type 允许的转移 $\delta(s_i)$，并且仅当实际消息匹配某一合法转移时才接受并推进状态。故所有被 Validator 接受的行为均属于 $L_i$ 允许的通信，进而属于 $G$ 允许的通信路径。因此运行过程中不会产生协议违约。证毕。

### 6.5.2 完备性

**定理 6.2（违约检测完备性）**　对于任意违反 Local Type 的通信行为 $m \notin \delta(s)$，Validator 均能够检测并拒绝。

由消息检查函数 $C$ 的定义，当且仅当存在合法转移 $s_i \xrightarrow{(p,l,\tau)} s_j$ 时 $C(m,s_i)=s_j$；否则 $C(m,s_i)=\bot$。因此，任何不属于当前状态允许转移集合 $\delta(s_i)$ 的通信行为均无法通过匹配，必然被判定为违约并拒绝。于是框架保证：

$$
\text{Illegal Communication} \;\longrightarrow\; \text{Detection}
$$

即所有违反局部类型的通信行为都能被检测。

### 6.5.3 时间复杂度

由于 Validator 仅维护当前状态 $s_i$ 以及该状态下的有限转移集合 $\delta(s_i)$，单次消息验证只需在当前状态的出边集合中进行匹配，与协议整体规模无关。设当前状态的出边数为常数上界 $k$（在实际协议中 $k$ 通常很小，多数状态为单一出边，选择型状态出边数等于分支数），则单次消息验证复杂度为：

$$
O(k) = O(1)
$$

相比于重新解析整个 Global Type $G$ 进行全量检查所需的 $O(|G|)$ 开销，运行时验证具有显著更低的单次检查代价。此外，Validator 的状态推进是增量式的，无需在每次通信后重新计算协议全局结构，因此在大规模、长会话的多智能体协作中仍能保持稳定的低开销。

## 小结

本章提出了一种基于局部类型的多智能体通信运行时验证框架。该框架利用第5章提出的泛化投影机制，将全局通信协议转换为 Agent 级局部协议，并进一步生成轻量级 Validator。在运行过程中，Validator 通过检查消息角色、标签以及数据类型，实现对 A2A 通信行为的动态验证，并能在角色遗漏、消息顺序错误、消息类型错误以及非法分支选择等场景下及时检测并阻止违约。在性质上，框架在协议可投影且智能体遵循局部类型的前提下保证协议一致性，对违反局部类型的通信行为具备检测完备性，且单次验证开销为常数级。相比现有智能体通信框架仅提供消息交换能力，本文方法能够进一步保证多智能体协作过程中的协议一致性和通信安全。
