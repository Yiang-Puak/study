# Workflow 与 LangGraph 高频八股

## 题单速刷

| 题目 | 先答什么 |
| :--- | :--- |
| Workflow 和 Agent 怎么选 | 流程确定用 Workflow，决策开放用 Agent |
| LangChain 和 LangGraph 怎么区分 | 组件与简单链路，状态图与复杂编排 |
| LangGraph 的 State 有什么用 | 显式共享工作流状态 |
| 条件边和循环边解决什么 | 路由、重试、反思和审批回路 |
| Multi-Agent 什么时候值得拆 | 角色、工具或上下文明显分工 |
| 多 Agent 为什么可能更差 | 通信、状态同步、成本和错误传播 |

## 1. Workflow 与 Agent 怎么选

**一句话答案：**当步骤稳定、规则明确、风险要强控制时用 Workflow；当下一步需要根据观察动态决定时引入 Agent。

| 场景 | 更稳的选择 |
| :--- | :--- |
| 固定表单审核 | Workflow |
| 工具检索后动态排障 | Agent |
| RAG 问答加引用 | Workflow 为主 |
| 编码任务多轮探索 | Agent 加受控工具 |

## 2. LangGraph 为什么适合 Agent 编排

**一句话答案：**因为它把状态、节点、边、条件路由和中断显式化，适合分支、循环和长任务恢复。

## 3. State、Node、Edge 怎么讲

```text
State：共享数据契约
Node：执行一步能力
Edge：决定下一步流向
Router：根据 State 选择分支
```

## 4. Multi-Agent 怎么答

**30 秒版：**

多 Agent 不是默认升级。先把单 Agent 和 Workflow 做稳，只有在角色天然分工、工具集合差异大、上下文需要隔离，或者可以并行处理独立子任务时再拆。拆完还要设计通信、共享状态、失败汇总和评测。

## 5. 常见误区

| 误区 | 修正 |
| :--- | :--- |
| 节点越多越工程化 | 节点要减少复杂度，不是制造复杂度 |
| 所有循环都交给模型 | 退出条件和预算要系统约束 |
| 多 Agent 自然更聪明 | 可能只是在放大协作成本 |
| Graph 就替代 Tool | Graph 管流程，Tool 管能力 |

## 回到专题

- [专题入口](index.md)
- [真题与工程追问](04_Workflow与LangGraph真题与工程追问.md)
