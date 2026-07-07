# Tool 与 MCP 高频八股

> Tool 负责把模型输出接到可执行能力，MCP 负责把这类能力按统一协议暴露给 AI 应用。

## 题单速刷

| 题目 | 一句话先答 |
| :--- | :--- |
| Tool Calling 是什么 | 模型提出结构化工具请求，应用侧校验并执行 |
| 模型为什么不能直接执行工具 | 模型生成意图，执行权和权限在运行时 |
| 好的 Tool Schema 长什么样 | 名称清楚、描述明确、参数受约束、输出稳定 |
| 工具失败怎么处理 | 校验、超时、重试、幂等、降级、人审 |
| MCP 解决什么问题 | 统一连接工具、资源和提示词 |
| MCP 与 Function Calling 区别 | 一个是调用格式，一个是连接协议 |
| 高风险工具怎么做安全 | 最小权限、隔离、审计、确认、回滚 |

## 1. Tool Calling 的闭环

```text
工具描述 -> 模型选择工具 -> 结构化参数
应用校验 -> 运行时执行 -> 结构化结果
模型继续推理 -> 返回答案或下一步动作
```

**记忆口诀：**模型提请求，运行时做执行。

## 2. 一个可靠 Tool 要讲清什么

1. 它做什么。
2. 什么时候该用。
3. 什么时候不该用。
4. 参数边界在哪里。
5. 失败后系统怎样收口。

## 3. 工具失败怎么答

**30 秒版：**

工具失败先分类。参数错误靠 schema 和校验拦住；外部依赖失败靠 timeout、retry、fallback；写操作必须考虑幂等和重复执行；高风险动作要加权限、审计和人工确认。最后还要把成功率、延迟和错误类型打进 Trace。

## 4. MCP 怎么答

**一句话答案：**MCP 是 AI 应用连接外部 Tools、Resources 和 Prompts 的标准协议。

**展开顺序：**

1. 先说 Host、Client、Server。
2. 再说 Tools、Resources、Prompts。
3. 再比较 Function Calling 与 MCP。
4. 最后补 transport、安全和复用价值。

## 5. 高频对比

| 对比 | 边界 |
| :--- | :--- |
| Tool vs API | API 是接口形式，Tool 是给模型可选择的能力包装 |
| Tool vs MCP | Tool 是能力，MCP 是能力接入协议 |
| Function Calling vs MCP | 前者关注一次调用结构，后者关注连接与暴露能力 |
| Resources vs Tools | Resources 偏读取上下文，Tools 偏执行动作 |

## 6. 回到专题

- [Tool 与 MCP 专题入口](index.md)
- [Tool 设计原则与容错](01_Tool设计原则与容错.md)
- [MCP 协议核心概念](02_MCP协议核心概念.md)
- [Tool 与 MCP 真题追问](04_Tool与MCP真题与工程追问.md)

## 回补知识点

- [Tool 设计原则与容错](01_Tool设计原则与容错.md)
- [Tool 与 MCP 专题入口](index.md)
- [相关专题题页](04_Tool与MCP真题与工程追问.md)
