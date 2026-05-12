# 09 | Tool 与 MCP 工程实践

> Tool 让 LLM 从“会说”变成“会做”，MCP 则把工具、资源和提示词连接标准化。

---

## 本章学习目标

- 能区分 Tool、Function Call、MCP
- 能设计可靠的 Tool Schema
- 能解释 MCP Host / Client / Server 架构
- 能说明 MCP 的 Tools / Resources / Prompts 三类能力
- 能回答工具调用安全、权限、超时、重试和幂等性问题

---

## 章节目录

| 页面 | 重点 |
|------|------|
| [Tool 设计原则与容错](01_Tool设计原则与容错.md) | Tool Schema、参数校验、幂等、重试、熔断 |
| [MCP 协议核心概念](02_MCP协议核心概念.md) | Host、Client、Server、Tools、Resources、Prompts、Transport |

---

## Tool / Function Call / MCP 的关系

| 概念 | 作用 | 类比 |
|------|------|------|
| Tool | 具体能力，如查天气、读文件、查数据库 | 一个可执行按钮 |
| Function Call | LLM 请求调用工具的格式协议 | 调用按钮时填写的表单 |
| MCP | 管理和暴露工具/资源/提示词的标准协议 | 插座和接口标准 |

---

## 面试高频题

1. Function Call 的 JSON Schema 怎么设计？
2. 工具描述为什么会影响模型是否正确调用工具？
3. 工具调用失败怎么处理？
4. MCP 和普通 Function Calling 有什么区别？
5. MCP Server 暴露 Tools、Resources、Prompts 分别有什么用？
6. 本地 MCP Server 有哪些安全风险？
