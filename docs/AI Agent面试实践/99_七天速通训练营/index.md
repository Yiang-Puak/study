# AI Agent 面试七天速通训练营

> 目标：不再从长文档里迷路，而是用 7 天把核心知识、项目表达和面试口述跑一遍。

<div class="hero-panel" markdown>

<span class="hero-eyebrow">7-Day Interview Sprint</span>

<h1 class="hero-title">每天 45 分钟，把 Agent 知识变成可面试输出</h1>

<p class="hero-subtitle">学习顺序固定为：知识卡片 → 项目举证 → 口述训练 → 追问复盘。重点不是看完所有内容，而是能讲清楚、能举项目、能回答追问。</p>

<div class="hero-actions" markdown>

[打开知识卡片](知识卡片速查.md){ .md-button .md-button--primary }
[开始 Day 1](01_Day1_Agent全景.md){ .md-button }
[高频追问题库](高频追问题库.md){ .md-button }

</div>

</div>

---

## 一、每天固定学习法

<div class="strategy-strip" markdown>

<div class="strategy-item" markdown>
<strong>10 分钟：看知识卡片</strong>
只看定义、30 秒回答、项目举证，不陷入长文档。
</div>

<div class="strategy-item" markdown>
<strong>15 分钟：项目举证</strong>
把知识点绑定到 RAG、Tool、Workflow、Eval 等通用项目证据。
</div>

<div class="strategy-item" markdown>
<strong>20 分钟：口述 + 追问</strong>
先自己说，再看标准答案，再练追问，最后压缩成 30 秒版本。
</div>

</div>

---

## 二、7 天路线图

| 天数 | 主题 | 今日目标 | 入口 |
| :--- | :--- | :--- | :--- |
| Day 1 | Agent 全景 | 能用五层架构解释 Agent 系统 | [开始](01_Day1_Agent全景.md) |
| Day 2 | RAG 与检索 | 能讲清 Chunk、Embedding、混合检索、Rerank | [开始](02_Day2_RAG与检索.md) |
| Day 3 | Tool 与 MCP | 能讲清工具调用闭环和 MCP 价值 | [开始](03_Day3_Tool与MCP.md) |
| Day 4 | LangGraph 与记忆 | 能讲清 State、Node、Edge、多轮上下文 | [开始](04_Day4_LangGraph与记忆.md) |
| Day 5 | Eval 与安全 | 能讲清评测、Trace、SQL 安全和 HITL | [开始](05_Day5_Eval与安全.md) |
| Day 6 | 项目链路复盘 | 能把一个 Agent 项目拆成模块、风险和指标 | [查看项目复盘入口](../../项目实战与复盘/index.md) |
| Day 7 | 模拟面试冲刺 | 完成 15 道高频题口述 | [开始](07_Day7_模拟面试冲刺.md) |

---

## 三、P0 必会清单

| 知识点 | 你必须能说出什么 | 项目举证 |
| :--- | :--- | :--- |
| Agent 五层架构 | 模型、上下文、工具、编排、治理 | 知识库或工具型 Agent 链路 |
| RAG | 索引、检索、增强、生成 | 带引用的知识库问答 |
| Tool Calling | 模型选工具，应用执行，结果回填 | SQL 执行器 |
| LangGraph | State、Node、Edge、条件边 | 工具失败重试与人工确认 |
| Eval Harness | 固定 Case、指标、自动报告 | 20 条评测集 |
| SQL 安全 | Prompt 不是安全边界，执行层兜底 | SELECT 白名单、只读连接 |
| 可观测性 | metadata、trace、latency、token | 前端执行详情 |

---

## 四、每天输出物

每天结束时，你要留下 3 个输出：

1. **一句话定义**：这个知识点是什么；
2. **30 秒口述**：面试时怎么讲；
3. **项目举证**：我在哪个项目里用过。

示例：

```text
知识点：RAG
一句话定义：在生成答案前先检索外部证据，再把证据组织进上下文。
30 秒口述：RAG 的质量不只看模型回答，还要拆开检查切块、召回、精排、引用和生成忠实度。
项目举证：知识库 Agent 会先召回文档片段，再让回答携带引用与证据来源。
```

---

## 五、建议使用方式

- **第一遍**：每天只看训练营，不跳到长文档；
- **第二遍**：遇到不会的，再点回对应专题深入；
- **第三遍**：只刷 `高频追问题库.md` 和项目复盘入口；
- **面试前一天**：只看 `知识卡片速查.md`。
