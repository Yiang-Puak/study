# Day 4 | LangGraph 与记忆：让 Agent 有状态地工作

## 今日目标

- 能讲清 State、Node、Edge；
- 能说明为什么需要条件边；
- 能解释多轮上下文如何支持追问。

---

## 10 分钟知识卡片

### 1. LangGraph 三元组

| 概念 | 含义 |
| :--- | :--- |
| State | 全局共享状态，保存 messages、工具参数、错误、结果等 |
| Node | 一个处理步骤，如 RAG、工具选择、工具执行 |
| Edge | 节点之间的流转关系 |

### 2. 条件边

条件边根据当前 State 决定下一步，例如：

```text
intent == tool_task → tool_execute
intent == chitchat → END
tool failed and retry_count < 3 → tool_select
```

### 3. 多轮记忆

多轮记忆通过 `conversation_id` 取历史消息，让系统理解“那上个月呢？”这种追问。

---

## 项目举证

带工具失败恢复的工作流：

```text
retrieve_context → tool_select → tool_execute → summarize_result
                              ↑          ↓ failed
                              └──────────┘ retry
```

---

## 面试训练

??? question "Q1：LangChain 和 LangGraph 有什么区别？"
    LangChain 更适合线性 Chain 和组件组合；LangGraph 更适合有状态、条件分支、循环重试、多 Agent 协作的复杂工作流。

??? question "Q2：LangGraph 的 State 有什么用？"
    State 保存工作流中的共享数据，例如用户消息、召回上下文、工具参数、执行结果、错误信息、重试次数和耗时。它让节点之间的数据传递显式、可调试、可观测。

??? question "Q3：多轮追问怎么实现？"
    用 `conversation_id` 找到历史对话，把最近 N 轮注入 `AgentState.messages`，再在 Prompt 中提供给模型。这样第二轮追问可以结合上一轮任务继续执行。

??? question "Q4：怎么防止 Agent 死循环？"
    设置最大重试次数、最大迭代步数和错误处理节点。超过次数后返回明确错误或转人工处理。

---

## 今日输出

```text
LangGraph 三元组：
为什么工具型工作流需要条件边：
多轮记忆实现方式：
一个可能的追问场景：
```
