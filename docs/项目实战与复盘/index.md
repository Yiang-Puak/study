---
hide:
  - toc
---

# 项目与代码实践

> 这里保留代码链路和项目复盘，用来把知识点放回真实系统，不替代专题与题库。

## 代码实践

| 实践 | 入口 | 对应知识点 |
| :--- | :--- | :--- |
| RAG 完整链路 | [代码实践](../AI%20Agent面试实践/03_RAG检索增强/02_RAG完整链路_代码实践.md) | 检索、上下文、引用、拒答 |
| ReAct Agent | [代码实践](../AI%20Agent面试实践/01_Agent基础架构/02_ReAct_Agent_代码实践.md) | Agent Loop、工具观察 |
| Multi-Agent | [协作实践](../AI%20Agent面试实践/01_Agent基础架构/03_MultiAgent_协作实践.md) | 角色拆分、通信成本 |
| Harness | [代码实践](../AI%20Agent面试实践/07_Harness工程深入/02_Harness代码实践_Subagent与DispatchMap.md) | 长任务、子任务、分发 |

## 项目复盘模板

| 项目方向 | 复盘入口 | 面试重点 |
| :--- | :--- | :--- |
| 知识库 Agent | [复盘模板](01_知识库Agent复盘模板.md) | ingestion、检索、引用、权限、评测 |
| 工具型 Workflow Agent | [复盘模板](02_工具型WorkflowAgent复盘模板.md) | Tool Schema、状态流转、HITL、失败恢复 |

## 复盘时检查

1. 输入输出是否清楚。
2. 主链路、状态和工具边界是否能画出来。
3. 失败点、重试、安全和人工确认是否能解释。
4. 是否能把项目答案回到 [面试题库](../面试题库/index.md) 的追问里。
