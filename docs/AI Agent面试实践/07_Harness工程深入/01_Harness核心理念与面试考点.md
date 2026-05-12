# 08 | Harness 工程深入 —— 从 learn-claude-code 提炼的面试知识点

> 来源：[learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) 项目提炼
> 这是面试中极具区分度的进阶内容，能让你从"调 API 的"升级为"造载具的"

---

## 一、核心概念：Agent vs Harness（⭐⭐⭐⭐⭐）

### 1. 一句话定义

**Agent = 模型（智能）+ Harness（载具）**

- **Agent（智能）**：感知、推理、行动的能力。来自模型训练，不是代码写出来的。
- **Harness（载具）**：让模型能在特定领域工作的环境。包括工具、知识、上下文管理、权限控制。

### 2. 类比理解

| 组件 | 类比 | 作用 |
|------|------|------|
| **模型** | 驾驶员 | 决定往哪开、怎么开 |
| **Harness** | 汽车 | 提供方向盘、油门、刹车、导航 |
| **工具** | 手脚 | 文件读写、Shell、API、浏览器 |
| **知识** | 地图 | 产品文档、API 规范、风格指南 |
| **上下文** | 记忆 | 当前看到什么、之前做了什么 |
| **权限** | 保险/交规 | 什么能做、什么不能做 |

### 3. 为什么这个概念重要？（面试加分！）

大多数面试者只停留在"调 API"的层面——用 LangChain/LangGraph 搭个工作流就觉得自己在做 Agent。

但真正理解 Harness 的人知道：
- **提示词水管工**（Prompt Plumber）：用 if-else、节点图、硬编码路由把 LLM 调用串起来 → 脆弱、不可扩展
- **Harness 工程师**：为模型构建一个可感知、可行动、可持久化的环境 → 模型自己决定做什么

**面试金句**："我不是在开发智能，我是在构建智能栖居的世界。"

---

## 二、Harness 的五大组件

```
Harness = Tools + Knowledge + Observation + Action Interfaces + Permissions

    Tools:          文件读写、Shell、网络、数据库、浏览器
    Knowledge:      产品文档、领域资料、API 规范、风格指南
    Observation:    git diff、错误日志、浏览器状态、传感器数据
    Action:         CLI 命令、API 调用、UI 交互
    Permissions:    沙箱隔离、审批流程、信任边界
```

### 1. Tools（工具）
- 每个工具都是 Agent 在环境中可以采取的一个行动
- 设计原则：**原子化、可组合、描述清晰**
- 新增工具只需加一个 handler，循环不用改（Dispatch Map 模式）

### 2. Knowledge（知识）
- 不是一次性塞入 system prompt，而是**按需加载**
- Skill 文件（.md）通过 tool_result 注入，Agent 用到什么加载什么
- 避免上下文膨胀：前置塞入 100 页文档，Agent 根本看不过来

### 3. Observation（观察）
- Agent 需要看到环境的状态才能做决策
- 代码 Agent：文件内容、目录结构、错误日志、git diff
- 农业 Agent：土壤湿度、气温、光照传感器数据

### 4. Action Interfaces（行动接口）
- Agent 的决策如何转化为实际执行
- 编程：写入文件、执行命令、调用 API
- 机器人：电机控制、机械臂运动

### 5. Permissions（权限）
- 沙箱化文件访问（safe_path 检查路径逃逸）
- 危险操作拦截（rm -rf /、sudo 等命令黑名单）
- 审批流程：破坏性操作需要人工确认

---

## 三、从 learn-claude-code 提炼的 12 个 Harness 机制

| 课程 | 机制 | 格言 | 面试考点 |
|------|------|------|----------|
| s01 | **Agent Loop** | One loop & Bash is all you need | 核心循环：LLM → tool_use → execute → loop |
| s02 | **Tool Dispatch** | 加一个工具，只加一个 handler | Dispatch Map 模式：name → handler，循环不变 |
| s03 | **TodoWrite** | 没有计划的 agent 走哪算哪 | 先列步骤再动手，完成率翻倍 |
| s04 | **Subagent** | 大任务拆小，每个小任务干净的上下文 | 独立 messages[]，不污染主对话，只返回 summary |
| s05 | **Skill Loading** | 用到什么知识，临时加载什么知识 | 不塞 system prompt，通过 tool_result 按需注入 |
| s06 | **Context Compact** | 上下文总会满，要有办法腾地方 | 三层压缩：micro（静默替换）→ auto（超阈值摘要）→ manual（工具触发） |
| s07 | **Task System** | 大目标要拆成小任务，排好序，记在磁盘上 | 文件持久化的任务图，依赖关系管理 |
| s08 | **Background Tasks** | 慢操作丢后台，agent 继续想下一步 | 守护线程 + 通知队列，异步不阻塞 |
| s09 | **Agent Teams** | 任务太大一个人干不完，要能分给队友 | 持久化队友 + JSONL 异步邮箱 |
| s10 | **Team Protocols** | 队友之间要有统一的沟通规矩 | Request-Response 模式驱动协商 |
| s11 | **Autonomous Agents** | 队友自己看看板，有活就认领 | 自组织：空闲轮询 + 自动认领 |
| s12 | **Worktree Isolation** | 各干各的目录，互不干扰 | 任务管目标，worktree 管目录，按 ID 绑定 |

---

## 四、核心机制详解（面试高频）

### 1. Agent Loop 的极简实现（s01）

```python
def agent_loop(messages):
    while True:
        response = llm(messages, tools)   # 1. 调用 LLM
        messages.append(assistant_msg)     # 2. 记录回复
        if not tool_use:                   # 3. 没有工具调用 -> 结束
            return
        results = execute_tools(response)  # 4. 执行工具
        messages.append(tool_results)      # 5. 结果回传，循环继续
```

**面试要点**：
- 循环的终止条件不是"固定轮数"，而是"模型决定停止"
- 代码只是执行模型的要求，不做决策
- 这是所有 Agent 的最小内核，其他机制都是在这个循环上叠加

---

### 2. Dispatch Map 模式（s02）

```python
TOOL_HANDLERS = {
    "bash":       lambda **kw: run_bash(kw["command"]),
    "read_file":  lambda **kw: run_read(kw["path"]),
    "write_file": lambda **kw: run_write(kw["path"], kw["content"]),
    "edit_file":  lambda **kw: run_edit(kw["path"], kw["old_text"], kw["new_text"]),
}

# 新增工具？只加一行！循环完全不用改
handler = TOOL_HANDLERS.get(tool_name)
output = handler(**args) if handler else f"Unknown tool: {tool_name}"
```

**面试要点**：
- 解耦工具定义和循环逻辑
- 新增工具零侵入，符合开闭原则
- 面试常问："怎么让 Agent 支持动态加载工具？" → 用 Dispatch Map + 注册表

---

### 3. Subagent 上下文隔离（s04）

```
Parent agent                     Subagent
+------------------+             +------------------+
| messages=[...]   |             | messages=[]      |  <-- fresh
|                  |  dispatch   |                  |
| tool: task       | ----------> | while tool_use:  |
|   prompt="..."   |            |   call tools     |
|                  |  summary    |                  |
|   result = "..." | <--------- | return last text |
+------------------+             +------------------+
```

**面试要点**：
- 子 Agent 有独立的 messages[]，不污染父 Agent 的上下文
- 子 Agent 共享文件系统（能看到相同的文件），但对话历史隔离
- 只返回 summary 给父 Agent，中间过程全部丢弃
- **类比**：项目经理（父）派一个实习生（子）去调研，实习生做完只交一份报告，调研过程中的草稿不交给经理

---

### 4. 三层 Context Compact（s06）⭐⭐⭐⭐

```
Every turn:
+------------------+
| Tool call result |
+------------------+
        |
        v
[Layer 1: micro_compact]        (silent, every turn)
  Replace old tool_result content with "[Previous: used {tool_name}]"
        |
        v
[Check: tokens > 50000?]
   |               |
   no              yes
   |               |
   v               v
continue    [Layer 2: auto_compact]
              Save full transcript to disk
              Ask LLM to summarize conversation
              Replace all messages with [summary]
                    |
                    v
            [Layer 3: compact tool]
              Model calls compact -> immediate summarization
```

| 层级 | 触发条件 | 策略 | 保留什么 |
|------|----------|------|----------|
| **micro_compact** | 每轮循环静默执行 | 旧 tool_result 替换为占位符 | 最近 3 个完整结果，read_file 输出保留 |
| **auto_compact** | Token 数 > 阈值 | 保存完整记录到磁盘，LLM 生成摘要 | 摘要 + 系统提示 |
| **manual_compact** | 模型主动调用 compact 工具 | 立即执行 auto_compact | 同上 |

**面试要点**：
- 为什么三层？单层无法兼顾"实时性"和"压缩力度"
- micro：轻量、无感知、每轮都做
- auto：兜底策略，防止上下文溢出
- manual：Agent 自己判断"该清理了"，最智能
- 对比 LangChain Memory：这是更工程化的实现，考虑 Token 成本和压缩粒度

---

### 5. Task System 持久化（s07）

- 任务不是存在内存里的变量，而是**持久化到磁盘**的文件
- 格式：JSON/JSONL，包含任务 ID、状态、依赖、优先级
- 好处：Agent 重启后任务不丢失；多 Agent 可以通过文件共享任务状态

```
task_graph.json:
{
  "tasks": [
    {"id": "t1", "status": "done", "deps": []},
    {"id": "t2", "status": "in_progress", "deps": ["t1"]},
    {"id": "t3", "status": "pending", "deps": ["t2"]}
  ]
}
```

**面试要点**：
- 为什么不用内存存储？进程崩溃/重启后丢失
- 依赖图怎么实现？拓扑排序，先完成依赖任务才能开始当前任务
- 和 LangGraph 的区别：LangGraph 用内存 StateGraph，这里用文件持久化

---

## 五、面试真题 + 标准答案

### 【真题 1】什么是 Harness 工程？和"提示词水管工"有什么区别？（⭐⭐⭐⭐⭐）

**答题模板**：
1. **核心定义**：Harness 是为 Agent 模型提供可感知、可行动环境的工程。模型是驾驶员，Harness 是载具。
2. **Harness 五大组件**：工具（Tools）、知识（Knowledge）、观察（Observation）、行动接口（Action）、权限（Permissions）。
3. **提示词水管工（Prompt Plumber）**：用 if-else、节点图、硬编码路由把 LLM 调用串在一起，试图通过工程手段编码出智能。结果：脆弱、不可扩展、不具备泛化能力。
4. **Harness 工程师**：不为模型做决策，只为模型构建环境。模型自己决定用什么工具、怎么组合。代码只是执行模型的要求。
5. **面试金句**："Agency 是训练出来的，不是编出来的。Harness 让 agency 落地。"

---

### 【真题 2】Agent Loop 的核心结构是什么？为什么循环的终止条件是模型决定停止？（⭐⭐⭐⭐）

**答题模板**：
1. **核心结构**：`while True: call LLM → check stop_reason → if tool_use: execute → append results → loop`
2. **终止条件**：`stop_reason != "tool_use"` 时循环结束。这意味着模型主动决定"我不需要再调用工具了，可以直接回答"。
3. **为什么这样设计**：因为模型的智能体现在"知道什么时候该停止"。如果代码固定循环 N 次，要么浪费 Token（提前完成还继续），要么完不成任务（需要更多轮次）。
4. **安全兜底**：同时设置 `max_iterations` 上限，防止模型陷入死循环。
5. **类比**：像医生问诊——病人描述症状（用户输入），医生决定做检查（调用工具）还是直接开药（停止循环）。问诊次数由医生（模型）决定，不是固定 3 次。

---

### 【真题 3】Subagent 的设计解决了什么问题？（⭐⭐⭐⭐）

**答题模板**：
1. **问题背景**：大任务需要多步骤完成，如果所有步骤都在同一个对话中进行，上下文会被中间过程的噪音污染，模型后期"看不清重点"。
2. **Subagent 方案**：把大任务拆成小任务，每个小任务派一个子 Agent 执行。子 Agent 有独立的 messages[]，只返回 summary 给父 Agent。
3. **核心优势**：
   - 上下文隔离：子 Agent 的中间过程不污染父 Agent
   - 关注点分离：父 Agent 负责规划，子 Agent 负责执行
   - 失败隔离：子 Agent 失败不影响父 Agent 的上下文
4. **实现细节**：子 Agent 共享文件系统（通过磁盘协作），但对话历史隔离。返回的只有最终 summary。
5. **类比**：项目经理（父）把调研任务外包给咨询公司（子），咨询公司内部讨论几百封邮件（中间过程），最后只提交一份 2 页的报告（summary）。

---

### 【真题 4】Context Compact 的三层策略各是什么？为什么需要三层？（⭐⭐⭐⭐）

**答题模板**：
1. **问题背景**：Agent 的上下文窗口有限（如 128K Token），长会话必然溢出。需要策略性"遗忘"不重要信息，保留关键信息。
2. **三层策略**：
   - **micro_compact（微观压缩）**：每轮静默执行，将旧的非 read_file tool_result 替换为占位符 `[Previous: used {tool_name}]`。无感知、低成本。
   - **auto_compact（自动压缩）**：当 Token 数超过阈值时触发，保存完整记录到磁盘，让 LLM 生成摘要，然后用摘要替换整个对话历史。
   - **manual_compact（手动压缩）**：Agent 自己判断"该清理了"，主动调用 compact 工具。最智能，因为模型知道哪些信息重要。
3. **为什么需要三层**：单层策略无法兼顾所有场景。micro 轻量但力度弱；auto 兜底但时机被动；manual 精准但需要模型配合。三层组合实现"无限会话"。
4. **和 LangChain Memory 的区别**：LangChain 提供 ConversationBufferMemory、ConversationSummaryMemory 等预制组件，但 Compact 是更细粒度的工程化实现，考虑了 Token 成本和业务场景。

---

### 【真题 5】Dispatch Map 模式是什么？有什么好处？（⭐⭐⭐⭐）

**答题模板**：
1. **核心定义**：用一个字典（Map）把工具名映射到处理函数：`{tool_name: handler_function}`。
2. **执行逻辑**：`handler = TOOL_HANDLERS.get(tool_name); output = handler(**args)`
3. **好处**：
   - **解耦**：工具定义和循环逻辑分离
   - **扩展性**：新增工具只需在 Map 中加一行，循环代码完全不用改（开闭原则）
   - **动态性**：运行时可以从外部加载工具注册表，实现插件化
4. **对比 if-else 链**：if-else 每加一个工具就要改循环代码，违背开闭原则；Dispatch Map 新增工具零侵入。
5. **生产扩展**：可以用装饰器自动注册（`@tool` 装饰器把函数加入全局 Map），实现工具的自发现。

---

### 【真题 6】Skill Loading 为什么要"按需加载"而不是"前置塞入"？（⭐⭐⭐）

**答题模板**：
1. **前置塞入的问题**：把产品文档、API 规范、风格指南全部塞进 system prompt → 上下文膨胀 → 模型注意力分散 → 成本高（Token 多）。
2. **按需加载方案**：system prompt 只告诉 Agent"有哪些 Skill 可用"，Agent 通过工具调用主动拉取需要的 Skill 文件内容。
3. **实现方式**：Skill 是 .md 文件，通过 `read_file` 工具读取，结果通过 tool_result 注入对话。
4. **类比**：去图书馆查资料，不是把整栋楼的书搬回家再看，而是去书架找需要的书，看完放回去。

---

## 六、面试冲刺检查清单

- [ ] 能说出 Harness 的五大组件
- [ ] 能区分"提示词水管工"和"Harness 工程师"
- [ ] 能画出 Agent Loop 的流程图
- [ ] 能解释 Dispatch Map 模式的优势
- [ ] 能说出 Subagent 隔离的三层 Context Compact 策略
- [ ] 能解释为什么 Skill 要"按需加载"而非"前置塞入"
- [ ] 能说出 Task System 持久化的好处
- [ ] 能描述 Agent Teams 的异步邮箱机制

---

## 七、推荐阅读

- [learn-claude-code 中文文档](https://github.com/shareAI-lab/learn-claude-code/tree/main/docs/zh) —— 12 个课程的详细文档
- [Kode-cli](https://github.com/shareAI-lab/Kode-cli) —— 基于这些原理实现的开源 Coding Agent
- [claw0](https://github.com/shareAI-lab/claw0) —— 姊妹仓库：从临时工具到常驻助手的 Harness 机制

---

*本节完毕！Harness 工程是 Agent 面试中最具区分度的知识点，掌握它，你的认知会超越 90% 的面试者。*
```
