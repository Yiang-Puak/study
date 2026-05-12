# Context 工程核心概念与面试考点

> 基于 Anthropic 官方工程博客与生产实践整理

---

## 一、什么是 Context Engineering

**Context Engineering（上下文工程）** 是 Prompt Engineering 的自然演进。

| 对比维度 | Prompt Engineering | Context Engineering |
|---------|-------------------|---------------------|
| **关注点** | 怎么写提示词 | 怎么管理上下文窗口里的信息 |
| **时间范围** | 单次推理 | 多轮循环 + 长时任务 |
| **核心挑战** | 指令清晰度 | 信息筛选、压缩、持久化 |
| **技术栈** | 模板、Few-shot | Compaction、Memory、RAG |

**一句话定义**：Context Engineering 是"在有限的上下文窗口内，为模型提供最高信号密度信息"的艺术与科学。

---

## 二、为什么必须做 Context Engineering

### 1. Context Rot（上下文衰减）

Anthropic 研究表明：随着上下文 token 增加，模型准确回忆信息的能力**持续下降**。

- 128K 窗口 ≠ 128K 有效信息
- 信息越多，注意力越分散
- 关键指令容易被噪声淹没

### 2. 注意力预算有限

LLM 的注意力机制是 O(n²) 复杂度：

```
1000 tokens → 1,000,000 对关系
10000 tokens → 100,000,000 对关系
```

每增加一个 token，都在消耗模型的"注意力预算"。

### 3. 多轮循环的累积污染

Agent 循环中每轮产生的新数据：
- 工具调用结果
- 观察（Observation）
- 思考（Thought）
- 环境反馈

如果不管理，上下文会迅速膨胀且质量下降。

---

## 三、Context Engineering 的三大核心技术

### 1. Compaction（压缩）

**原理**：接近窗口限制时，总结历史并丢弃冗余。

**实现方式**：
- 让模型自己总结对话历史
- 保留关键决策、未完成任务、架构选择
- 丢弃已完成的工具调用细节

**Claude Code 实践**：
- 把消息历史传给模型做总结压缩
- 保留最近访问的 5 个文件
- 用户获得连续性，不担心窗口限制

### 2. Structured Note-taking（结构化笔记）

**原理**：Agent 定期写笔记到上下文外，后续读取。

**实现方式**：
- `NOTES.md`：项目级笔记
- `todo.json`：任务追踪
- `memory/` 目录：分类持久化记忆

**Claude Plays Pokémon 验证**：
- 数千步游戏中维护精确统计
- 训练路线、解锁成就、战斗策略
- 上下文重置后读取笔记继续

### 3. Context Retrieval（动态检索）

**原理**：只把当前相关的信息拉入上下文。

**实现方式**：
- RAG：按语义检索相关文档
- Agentic Search：让模型决定检索什么
- 分层记忆：工作记忆 + 长期记忆

---

## 四、面试高频考点

### 考点 1：Context Engineering vs Prompt Engineering

**标准回答**：
> Prompt Engineering 关注单次推理中怎么写提示词；Context Engineering 关注多轮交互中怎么管理上下文窗口的信息密度和时效性。随着 Agent 从单次调用走向长时间运行，Context Engineering 成为决定系统上限的关键。

### 考点 2：如何解决长会话中的上下文丢失？

**三层方案**：
1. **轻量层**：Tool Result Clearing（清理已完成的工具输出）
2. **中度层**：Sliding Window（滑动窗口保留最近 N 轮）
3. **重度层**：Compaction（全量总结 + 重启上下文）

### 考点 3：工具结果太多怎么办？

**策略**：
- 工具返回结构化、精简的数据
- 已调用的工具结果可清空
- 按需检索，不要全量塞入

### 考点 4：多 Agent 系统中的上下文隔离

**Harness 模式**：
- 每个 Subagent 有自己的上下文窗口
- Dispatch Map 传递精简状态，而非全量历史
- "模型做决策，代码只执行" + "模型做筛选，只给最相关信息"

---

## 五、与现有知识体系的关系

```
Agent 基础架构（ReAct / MultiAgent）
    ↓
记忆系统（短期/长期记忆）
    ↓
RAG 检索增强（外部知识）
    ↓
LangChain / LangGraph（编排框架）
    ↓
Harness 工程（Subagent 隔离 + Dispatch Map）
    ↓
Context 工程（上下文压缩 + 持久化 + 动态检索） ← 新增
    ↓
Prompt 工程（指令优化）
```

**Context Engineering 是 Harness 哲学的延伸**：
- Harness：把 LLM 当智能编排器，代码只执行
- Context Engineering：把 LLM 当信息筛选器，只给最相关的上下文

---

## 六、推荐阅读

- [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Manus: Context Engineering Lessons](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [PromptingGuide: Context Engineering Deep Dive](https://www.promptingguide.ai/agents/context-engineering-deep-dive)
`
