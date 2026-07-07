# Agent 基础高频八股

## 题单速刷

| 题目 | 先答什么 |
| :--- | :--- |
| 什么是 Agent | 多步决策与行动系统 |
| Agent 和 Chatbot 区别 | 回答文本与完成任务 |
| Agent 和 RAG 区别 | 执行闭环与知识检索 |
| Agentic Loop 是什么 | Think、Act、Observe |
| ReAct 和 Function Call 区别 | 策略框架与结构化调用 |
| 单 Agent 和 Multi-Agent 怎么选 | 先稳单 Agent，再拆天然分工 |

## 1. 什么是 Agent

**一句话答案：**Agent 是能围绕目标观察状态、选择行动、接收反馈并多步推进任务的系统。

## 2. Agent 与相近概念

| 概念 | 边界 |
| :--- | :--- |
| Chatbot | 主要生成回答 |
| RAG | 主要补外部证据 |
| Workflow | 系统显式控制步骤 |
| Agent | 模型在边界内决定下一步 |
| Multi-Agent | 多个角色协作完成任务 |

## 3. Agentic Loop 怎么答

```text
Think：判断下一步
Act：调用能力
Observe：读取结果
Stop：完成、失败收口或人工介入
```

## 4. 常见误区

| 误区 | 修正 |
| :--- | :--- |
| 接了 Tool 就是 Agent | 还要有观察、决策和反馈闭环 |
| 自主性越大越好 | 可靠系统要有边界和治理 |
| Multi-Agent 是默认升级 | 先看拆分收益是否大于协作成本 |

## 回到专题

- [Agent 基础专题入口](index.md)
- [Agent 基础真题追问](06_Agent基础真题与工程追问.md)

## 回补知识点

- [Agent 基础学习与答题页](01_核心概念与面试答题模板.md)
- [Agent 基础专题入口](index.md)
- [相关专题题页](06_Agent基础真题与工程追问.md)
