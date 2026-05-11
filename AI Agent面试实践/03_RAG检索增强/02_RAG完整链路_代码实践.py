"""
【面试加分项】基于 LangChain 构建完整 RAG 链路 —— 代码实践

学习目标：
1. 掌握 RAG 四阶段完整实现
2. 理解 Embedding + 向量检索 + Prompt 增强 + LLM 生成的串联
3. 能手撕一个最小可用 RAG 系统

运行前准备：
pip install langchain langchain-community openai chromadb
"""

import os
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


# ========================
# 第一步：索引阶段（Indexing）
# ========================
# 面试要点：
# - 文档怎么加载？—— LangChain 提供各种 Loader（PDF/CSV/网页等）
# - 怎么切分？—— 用 TextSplitter 控制 chunk_size 和 overlap
# - 用什么 Embedding？—— 中文场景推荐 text-embedding-v4 或 BGE

# ============================================================================
# 模拟文档数据
# ============================================================================
# 实际项目中，这些文档通常来自：
#   - PDF/Word/TXT 文件（用 LangChain 的 PyPDFLoader、TextLoader 加载）
#   - 数据库查询结果
#   - 网页爬虫抓取的内容
# 这里为了演示方便，直接用字符串列表

DOCUMENTS = [
    "人工智能（AI）是指由计算机系统模拟人类智能的技术，包括学习、推理、感知和语言理解等能力。",
    "机器学习是人工智能的一个子领域，通过数据训练模型，使系统能够自动改进性能。",
    "深度学习是机器学习的一种，使用多层神经网络处理复杂数据，广泛应用于图像识别和自然语言处理。",
    "大语言模型（LLM）是基于深度学习的模型，通过海量文本预训练获得强大的语言生成和理解能力。",
    "RAG（检索增强生成）是一种将外部知识检索与大语言模型生成相结合的技术，有效减少模型幻觉。",
    "Agent 智能体是一种能够感知环境、做出决策并执行行动的智能系统，通常由 LLM 作为核心大脑。",
    "向量数据库是一种专门存储和检索高维向量数据的数据库，常用于语义搜索和 RAG 系统。",
    "Embedding 是将文本、图像等数据映射到低维向量空间的过程，使得语义相似的文本在向量空间中距离更近。",
]


def build_index(documents: list, embedding_model):
    """
    构建向量索引
    面试要点：为什么用 add_texts 而不是 add_documents？
    —— add_texts 直接传入字符串列表，更简单；add_documents 传入 Document 对象，可携带 metadata
    """
    # 使用内存向量存储（面试场景简化版，生产环境用 Chroma/Milvus）
    vector_store = InMemoryVectorStore(embedding=embedding_model)

    # 添加文档（实际项目中，这里会先 split 再 add）
    vector_store.add_texts(documents)
    print(f"[索引完成] 已索引 {len(documents)} 个文档片段")

    return vector_store


# ========================
# 第二步：检索阶段（Retrieval）
# ========================
# 面试要点：
# - similarity_search 返回什么？—— List[Document]，每个包含 page_content 和 metadata
# - k 怎么选？—— 面试常问：k 太小可能漏答案，k 太大可能引入噪声；通常 3-10

def retrieve(query: str, vector_store, k: int = 3):
    """
    语义检索
    面试要点：这里只做了语义检索，生产环境应做混合检索（语义 + BM25）
    """
    results = vector_store.similarity_search(query, k=k)

    print(f"\n[检索阶段] Query: '{query}'")
    print(f"召回 {len(results)} 个相关片段：")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.page_content[:40]}...")

    # 将检索结果拼接为上下文字符串
    context = "\n".join([f"[{i+1}] {doc.page_content}" for i, doc in enumerate(results)])
    return context


# ========================
# 第三步：增强阶段（Augmentation）
# ========================
# 面试要点：
# - Prompt 怎么设计？—— 明确告诉模型"基于以下资料回答"
# - 如果检索结果为空怎么办？—— 可以提示"根据我的知识回答"或直接拒绝

RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业助手。请严格根据我提供的参考资料回答问题。
如果参考资料中没有相关信息，请明确说明"根据现有资料无法回答"。

参考资料：
{context}"""),
    ("human", "{question}")
])


# ========================
# 第四步：生成阶段（Generation）
# ========================
# 面试要点：
# - 为什么用 LCEL（| 管道）？—— 可组合、可复用、支持流式输出
# - RunnablePassthrough 的作用？—— 将输入透传并附加新字段


def build_rag_chain(model, vector_store):
    """
    构建完整 RAG Chain
    面试要点：这是 LCEL（LangChain Expression Language）语法，用 | 串联组件
    """

    # 定义检索器函数
    retriever = lambda q: retrieve(q, vector_store, k=3)

    # 构建 Chain：输入 → 检索 + 透传 → Prompt → LLM → 解析输出
    chain = (
        {
            "context": retriever,           # 对 question 做检索，得到 context
            "question": RunnablePassthrough() # question 原样透传
        }
        | RAG_PROMPT
        | model
        | StrOutputParser()
    )

    return chain


# ========================
# 第五步：运行测试
# ========================

if __name__ == "__main__":
    print("=" * 50)
    print("RAG 完整链路演示")
    print("=" * 50)

    # 初始化组件
    embedding = DashScopeEmbeddings(model="text-embedding-v4")
    model = ChatTongyi(model="qwen3-max")

    # 1. 索引
    vector_store = build_index(DOCUMENTS, embedding)

    # 2. 构建 RAG Chain
    rag_chain = build_rag_chain(model, vector_store)

    # 3. 测试查询
    test_queries = [
        "什么是 RAG？",
        "深度学习和机器学习有什么关系？",
        "Agent 和 LLM 的区别是什么？",
        "量子计算的原理是什么？",  # 知识库中没有，测试拒答能力
    ]

    for query in test_queries:
        print(f"\n{'=' * 50}")
        print(f"🙋 用户问题：{query}")
        print(f"{'=' * 50}")

        answer = rag_chain.invoke(query)
        print(f"🤖 模型回答：{answer}")

    # 4. 流式输出演示（面试加分项）
    print(f"\n{'=' * 50}")
    print("流式输出演示")
    print(f"{'=' * 50}")
    print("🙋 用户问题：什么是向量数据库？")
    print("🤖 模型回答：", end="", flush=True)
    for chunk in rag_chain.stream("什么是向量数据库？"):
        print(chunk, end="", flush=True)
    print()

"""
【面试追问准备】

Q: 混合检索怎么实现？
A: 需要同时维护向量索引和倒排索引（BM25）：
   1. 向量检索召回 top_k_vector
   2. BM25 检索召回 top_k_bm25
   3. 按 α*vector_score + (1-α)*bm25_score 重新排序
   4. 取最终 top_k
   LangChain 的 EnsembleRetriever 可以简化实现。

Q: 检索结果太多导致 Prompt 太长怎么办？
A: 1）减小 k 值；2）对检索结果做摘要压缩后再拼入 Prompt；
   3）用 Map-Reduce 模式（每个 chunk 单独生成，再合并）。

Q: 怎么处理知识库更新？
A: 1）增量索引：只重新索引变更的文档；
   2）版本控制：文档带版本号，检索时优先返回最新版本；
   3）缓存失效：知识库更新时主动清除相关缓存。

Q: 怎么评估 RAG 效果？
A: 检索阶段：Hit@K、MRR、NDCG；
   生成阶段：人工评分、Faithfulness（RAGAS 框架可自动评估）。

Q: 如果向量检索召回的结果都不相关怎么办？
A: 1）Embedding 微调；2）查询改写（Query Expansion）；
   3）混合检索补充 BM25；4）加入兜底策略（纯 LLM 回答 + 免责声明）。
"""
