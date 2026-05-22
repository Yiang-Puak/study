# Day 5 | Eval 与安全：让 Agent 可验证、可治理

## 今日目标

- 能讲清 Eval Harness 为什么必要；
- 能解释 Pass@1、Tool Accuracy、Self-Correction Rate；
- 能说明 Prompt 不是安全边界。

---

## 10 分钟知识卡片

### 1. Eval Harness

Eval Harness 是固定评测集 + 指标统计 + 自动报告，用来判断 Agent 优化是否真的有效。

### 2. Agent 常见指标

| 指标 | 含义 |
| :--- | :--- |
| Pass@1 | 第一次生成并执行成功比例 |
| Retrieval Recall | 正确证据是否被召回 |
| Tool Accuracy | 工具与参数是否选择正确 |
| Self-Correction Rate | 重试后最终成功比例 |
| Avg Latency | 平均端到端耗时 |

### 3. 安全原则

> Prompt 是行为建议，不是安全边界。

真正的安全边界必须在执行层：白名单、权限、只读连接、审计、HITL。

---

## 项目举证

工具型 Agent：

- 权限分级；
- 参数校验；
- 高风险动作人审；
- 失败回执结构化；
- 审计真实执行动作；
- 生成 Eval Markdown / JSON 报告。

---

## 面试训练

??? question "Q1：为什么 Agent 需要 Eval Harness？"
    因为 LLM 输出不稳定，不能只靠手动 Demo 判断效果。Eval Harness 用固定 Case 集和指标做回归，能证明 Prompt、RAG、工具和自愈机制的改动是否真的提升了系统质量。

??? question "Q2：工具执行成功就代表任务正确吗？"
    不代表。工具执行成功只说明调用路径跑通，任务意图、参数、上下文和最终解释仍可能错。所以要同时看工具命中率、参数正确率、任务完成率和失败分类。

??? question "Q3：怎么防止模型调用危险工具？"
    不能只靠 Prompt。执行前要做工具白名单、参数校验、权限分级和审计，高风险动作还应加入人工审批。

??? question "Q4：可观测性要记录什么？"
    记录 intent、retrieved_context、selected_tool、tool_args、tool_result、耗时、Token、retry_count 和 execution_trace，用于定位错误发生在哪个节点。

---

## 今日输出

```text
Eval Harness 一句话定义：
3 个你能解释的指标：
工具安全的执行层防护：
为什么 Prompt 不是安全边界：
```
