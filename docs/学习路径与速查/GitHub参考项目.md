# GitHub 仓库与学习页面

> 这里放可以直接打开学习的 GitHub 仓库和官方学习页。优先看源码结构、examples、docs 和 issue 里真实的工程问题。

## Agent 编排

| 链接 | 类型 | 学什么 |
| :--- | :--- | :--- |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | GitHub | StateGraph、条件边、循环、持久化状态 |
| [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/) | Docs | concepts、tutorials、how-to guides |
| [langchain-ai/langchain-academy](https://github.com/langchain-ai/langchain-academy) | GitHub | LangGraph 系统课程和 notebook |
| [microsoft/autogen](https://github.com/microsoft/autogen) | GitHub | 多 Agent 对话、任务拆分、工具协作 |
| [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | GitHub | role-based Agent、task、crew、tool 抽象 |

## RAG / 检索增强

| 链接 | 类型 | 学什么 |
| :--- | :--- | :--- |
| [langchain-ai/rag-from-scratch](https://github.com/langchain-ai/rag-from-scratch) | GitHub | RAG 从索引、检索到生成的完整 notebook |
| [run-llama/llama_index](https://github.com/run-llama/llama_index) | GitHub | 文档 ingestion、index、retriever、agentic RAG |
| [qdrant/examples](https://github.com/qdrant/examples) | GitHub | 向量数据库、混合检索、过滤和实战样例 |
| [weaviate/recipes](https://github.com/weaviate/recipes) | GitHub | 向量检索、RAG、hybrid search 示例 |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | GitHub | RAG pipeline、retriever、reader、evaluation |

## Tool / MCP / 外部能力

| 链接 | 类型 | 学什么 |
| :--- | :--- | :--- |
| [modelcontextprotocol/specification](https://github.com/modelcontextprotocol/specification) | GitHub | MCP 协议、tool/resource/prompt 的边界 |
| [MCP 官方文档](https://modelcontextprotocol.io/) | Docs | MCP 概念、server、client、transport |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | GitHub | 官方和社区 MCP server 示例 |
| [openai/openai-cookbook](https://github.com/openai/openai-cookbook) | GitHub | function calling、structured output、RAG、eval 示例 |

## Eval / Trace / 可观测

| 链接 | 类型 | 学什么 |
| :--- | :--- | :--- |
| [langfuse/langfuse](https://github.com/langfuse/langfuse) | GitHub | LLM trace、prompt management、eval、observability |
| [LangSmith 文档](https://docs.smith.langchain.com/) | Docs | tracing、dataset、evaluation |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | GitHub | prompt eval、red team、回归测试 |

## Python / 后端工程

| 链接 | 类型 | 学什么 |
| :--- | :--- | :--- |
| [fastapi/fastapi](https://github.com/fastapi/fastapi) | GitHub | FastAPI 源码、examples、issue 里的真实 API 问题 |
| [FastAPI 官方文档](https://fastapi.tiangolo.com/) | Docs | Pydantic、依赖注入、异步、异常处理 |
| [encode/httpx](https://github.com/encode/httpx) | GitHub | Python HTTP client、异步请求、超时 |
| [pytest-dev/pytest](https://github.com/pytest-dev/pytest) | GitHub | fixture、mock、测试组织 |
| [tiangolo/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) | GitHub | FastAPI 项目结构、Docker、前后端集成 |

## 面试题与 AI Engineering

| 链接 | 类型 | 学什么 |
| :--- | :--- | :--- |
| [amitshekhariitbhu/ai-engineering-interview-questions](https://github.com/amitshekhariitbhu/ai-engineering-interview-questions) | GitHub | AI Engineering 面试题型和知识覆盖 |
| [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | GitHub | 系统设计、缓存、队列、可用性、扩展性 |
| [jwasham/coding-interview-university](https://github.com/jwasham/coding-interview-university) | GitHub | CS 基础、数据结构、算法学习路线 |
| [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python) | GitHub | Python 算法实现，适合手撕题对照 |

## 怎么用这些链接

```text
项目名：
它解决什么问题：
核心抽象：
关键链路：
我能复用到项目的点：
面试可说的一句话：
```

## 当前最值得学习的顺序

1. 先看 LangGraph：补 Agent 编排与状态流转。
2. 再看 RAG From Scratch：补 RAG 评测和检索优化。
3. 看 MCP 官方文档和 servers：补工具协议和外部系统接入。
4. 看 Langfuse / promptfoo：补 trace、eval、prompt 回归测试。
5. 看 FastAPI / pytest：补 Python 后端和测试能力。
