# 00 | AI 底层框架全景图

> 这一章用于回答最容易被问到的总览题：一个完整 AI Agent 系统到底由哪些层组成？

---

## 本章定位

很多同学学习 Agent 时会直接从 ReAct、RAG 或 LangChain 开始，但面试官更希望听到你能从底层到工程全链路解释：

```text
LLM & Token → Context Window → Prompt / RAG → Tool / MCP → Agent → Agent Skill → Eval / Safety
```

这章就是用来建立这张“总地图”。

---

## 学习目标

- 能画出 AI Agent 底层框架全景图
- 能解释 LLM、Token、Context、Prompt、RAG、Tool、MCP、Agent Skill 的关系
- 能区分 Prompt Engineering 和 Context Engineering
- 能把零散知识组织成面试中的系统化回答

---

## 章节目录

| 页面 | 解决的问题 |
|------|------------|
| [AI 系统分层总览](01_AI系统分层总览.md) | Agent 系统从底层到应用如何分层 |
| [LLM 与 Token 底层原理](02_LLM与Token底层原理.md) | Token、上下文窗口、成本和推理参数如何影响 Agent |
| [Context Window 记忆加工容器](03_ContextWindow记忆加工容器.md) | 模型当前能看见什么，记忆/RAG/Prompt 如何装入上下文 |

---

## 面试高频问题

1. AI Agent 和普通 LLM 应用的本质区别是什么？
2. 一个 Agent 系统由哪些层组成？
3. Token 为什么会成为 Agent 的成本和性能瓶颈？
4. Context Window、Memory、RAG 的关系是什么？
5. Tool、Function Call、MCP 的关系是什么？
