# Python × Agent 工程能力

> AI Agent 岗位不是只问算法，也会问 Python 工程化。下面这些能力能直接支撑 RAG、Tool Calling、LangGraph 和 FastAPI 项目。

## 必会能力矩阵

| 能力 | Agent 项目里怎么用 | 面试答题关键词 |
| :--- | :--- | :--- |
| 虚拟环境与依赖 | 固定 MkDocs、LangChain、FastAPI 等版本 | `requirements.txt`、lock、可复现构建 |
| 异步编程 | 并发调用检索、LLM、工具和外部 API | `asyncio`、I/O bound、超时、取消 |
| 日志与 trace | 记录 node、latency、token、error、conversation_id | structured logging、request id、链路追踪 |
| 测试 | mock LLM、固定 case、API 测试 | pytest、fixture、回归测试 |
| 数据处理 | 清洗文档、构造 chunk、统计评测指标 | pandas、jsonl、schema 校验 |
| API 后端 | 暴露 chat、upload、eval、health 接口 | FastAPI、Pydantic、SSE |
| 安全边界 | 工具参数校验、SQL 只读、敏感信息过滤 | allowlist、sandbox、HITL |

## 面试高频追问

### 1. Agent 系统里为什么常用异步？

因为 Agent 一次请求可能同时等待向量检索、LLM、数据库、外部工具和日志写入。它们大多是 I/O bound，异步可以减少等待时间，提高吞吐。

答题时别只说“更快”，要补一句：

> 异步不能让单次 LLM 推理本身变快，但能减少多个 I/O 调用之间的空等，适合 RAG 检索、工具调用和并发评测。

### 2. 你怎么测试一个 LLM 应用？

先把 LLM 输出当成不稳定依赖隔离：

1. 单元测试：mock LLM，验证 prompt builder、parser、tool executor。
2. 回归测试：固定 case 集，统计准确率、召回率、字段命中率。
3. 端到端测试：跑真实模型，记录 trace、latency、token 和失败原因。

### 3. 为什么要固定依赖版本？

LLM 应用通常依赖 LangChain、LangGraph、向量库和前端插件，这些库升级后 API 和渲染可能变化。固定版本能保证本地、CI 和部署环境一致，减少“我这里能跑”的问题。

## 推荐练习

1. 给一个 FastAPI chat 接口加 `request_id`、耗时日志和错误码。
2. 用 `pytest` mock 一个 LLM response，测试 JSON parser。
3. 写一个异步函数并发请求 3 个 mock tool，比较串行和并发耗时。
4. 把项目依赖写入 `requirements.txt`，让 GitHub Actions 用同一份依赖构建。
