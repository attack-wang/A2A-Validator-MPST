# 内容契约如何发挥作用

MPST 先检查当前状态下谁能给谁发送哪种标签的消息。内容契约进一步检查该消息交付的载荷。两者都通过才提交阶段结果；候选拒绝时保留此前已接受的状态、代码和历史，向生成角色返回诊断，在上限内重试。

## 编码契约

完整配置在 [冻结契约注册表](../source/pure-contract/chatdev-contracts.json)；实现主要在 [chatdev_contracts.py](../source/pure-contract/content_lab/chatdev_contracts.py)、[source_files.py](../source/pure-contract/content_lab/source_files.py) 和 [content_guard.py](../source/pure-contract/integrations/ChatDev1.0/chatdev/content_guard.py)。

编码交付必须包含明确的平面 `.py` 文件名、闭合代码围栏、非空且不重复的文件。解析器将候选变更与已有接受源码合并，检查全部 Python 文件的 AST/编译、初次编码的 `main.py` 入口及明显占位实现。编译验证在内存中进行，不等价于完成全部功能。

注册表默认 `max_attempts=3`，包括首次生成和最多两次候选重试。达到上限后抛出内容契约异常。主机启动及最终退出等检查并不是全部自动套用候选重试。

## 真实实验中的三个例子

1. R10 CandyCrush：Coding 前两次输出被判定为截断，第三次候选才接受，最终独立产物评估通过。见 [完整审计](../data/runs/mpst_contract/r10/24_CandyCrush/content-contract-audit.json) 和 [评估](../data/runs/mpst_contract/r10/24_CandyCrush/evaluation.json)。这是拒绝候选后重新生成的例子；不能单凭这一条证明关闭契约就一定失败。
2. R12 Minesweeper：测试总结引用的启动记录 ID 少了一位字符，`summary_evidence` 拒绝；随后一次候选截断，第三次接受，最终产物通过。见 [完整审计](../data/runs/mpst_contract/r12/12_Minesweeper/content-contract-audit.json)。契约验证真实证据一致性，避免凭空报告执行成功。
3. R11 ConnectFour：`<INFO> Finished.` 的句点没有被旧归一化逻辑去掉，导致 `missing_source_files` 拒绝，随后重新提交代码，最终产物通过。见 [完整审计](../data/runs/mpst_contract/r11/16_ConnectFour/content-contract-audit.json)。这是规则边界造成误拒的例子，归档保留当时行为，没有追溯修改结果。

## 全局类型引用的新版本

[全局类型](../source/inline-contract/integrations/ChatDev1.0/protocol/mpst_content.gt) 引用 [注册表](../source/inline-contract/chatdev-contracts.json) 的 10 份契约（8 种阶段结果、主机 testReport、done）。前端解析注解，编译成旧投影器可读的内部符号，再把契约引用恢复到局部 FSM 转换。

运行时通过当前发送/接收转换取得契约；只有与该通信相关的角色获得相应绑定。在提交两端状态前执行领域检查，未知引用、schema 不匹配或已注解却没有执行器时直接报错；没有注解的旧协议保留原验证行为。同标签不同契约不能随意合并或选取首条规则。

这项实现只通过离线测试，没有新增真实题目实验。保留纯契约冻结版本是为了让历史证据与新实现边界清楚。
