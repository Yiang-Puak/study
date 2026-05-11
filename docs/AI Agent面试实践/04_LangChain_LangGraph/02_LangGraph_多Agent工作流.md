# 02_LangGraph_多Agent工作流

> 来源: AI Agent面试实践/04_LangChain_LangGraph/02_LangGraph_多Agent工作流.py

`python
"""
【面试加分项】LangGraph 多 Agent 工作流编排 —— 代码实践

学习目标：
1. 理解 LangGraph 的 State / Nodes / Edges 核心概念
2. 掌握条件分支和循环的实现方式
3. 能手撕一个 LangGraph 多 Agent 协作示例

运行前准备：
pip install langgraph langchain langchain-community openai
"""

import os
from typing import TypedDict, Annotated, Literal
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


# ============================================================================
# 第一步：定义 State（状态）
# ============================================================================
# State 是 LangGraph 的核心概念——它就像一个"公共白板"，
# 所有 Agent（节点）都可以读取和修改白板上的信息。
#
# 面试要点：为什么不用普通变量传递数据？
# —— 普通变量只能在单个函数内使用，State 可以让不同节点共享数据。
#    就像快递站的货架，每个快递员（节点）都可以放东西和取东西。

class AgentState(TypedDict):
    """工作流状态定义

    TypedDict 是 Python 的类型提示工具。
    面试追问：为什么用 TypedDict 而不是普通 dict？
    —— TypedDict 有类型提示，IDE 可自动补全，且 LangGraph 会做 schema 校验
       就像给字典加了一份"说明书"，告诉你里面应该有什么字段。
    """
    messages: list          # 对话历史：记录每个 Agent 说了什么
    topic: str              # 当前任务主题：比如"AI Agent 的未来发展趋势"
    research_result: str     # 研究结果：研究员 Agent 产出的内容
    report: str              # 生成的报告：写手 Agent 产出的内容
    review_score: int        # 审核评分：审核员 Agent 打的分数（0-100）
    next_step: str           # 路由决策：用于控制流程走向


# ============================================================================
# 第二步：定义 Nodes（节点 = Agent）
# ============================================================================
# 在 LangGraph 中，"节点"就是一个普通的 Python 函数。
# 每个节点接收当前的 State（状态），做一些事情，然后返回更新后的 State。
#
# 类比：工厂流水线上的工人
#   - 每个工人（节点）拿到前一道工序的产品（State）
#   - 完成自己的工序（处理逻辑）
#   - 把产品传给下一道工序（返回新的 State）

# 初始化大模型——这是所有 Agent 共享的"大脑"
model = ChatTongyi(model="qwen3-max")


def research_node(state: AgentState) -> AgentState:
    """研究员 Agent：根据主题搜索信息"""
    topic = state["topic"]

    # 模拟研究过程（实际项目中调用搜索 API / 数据库）
    prompt = f"请对'{topic}'进行简要研究，列出3个核心要点。只输出要点。"
    response = model.invoke([HumanMessage(content=prompt)])

    state["research_result"] = response.content
    state["messages"] = state.get("messages", []) + [
        AIMessage(content=f"[研究员] 研究完成：{response.content}")
    ]
    return state


def write_node(state: AgentState) -> AgentState:
    """写手 Agent：根据研究结果撰写报告"""
    research = state["research_result"]
    topic = state["topic"]

    prompt = f"基于以下研究内容，撰写一份关于'{topic}'的简要报告（100字以内）：\n{research}"
    response = model.invoke([HumanMessage(content=prompt)])

    state["report"] = response.content
    state["messages"] = state.get("messages", []) + [
        AIMessage(content=f"[写手] 报告完成：{response.content}")
    ]
    return state


def review_node(state: AgentState) -> AgentState:
    """审核员 Agent：检查报告质量并决定下一步"""
    report = state["report"]
    topic = state["topic"]

    prompt = f"请对以下关于'{topic}'的报告打分（0-100），并说明是否通过审核：\n{report}\n\n只输出 JSON：{{'score': 分数, 'passed': true/false}}"
    response = model.invoke([HumanMessage(content=prompt)])

    # 解析评分（简化版，生产环境需健壮解析）
    content = response.content
    score = 85  # 默认值
    if "score" in content:
        try:
            import json
            result = json.loads(content[content.find("{"):content.rfind("}")+1])
            score = result.get("score", 85)
        except:
            pass

    state["review_score"] = score
    state["messages"] = state.get("messages", []) + [
        AIMessage(content=f"[审核员] 评分：{score}")
    ]
    return state


def revise_node(state: AgentState) -> AgentState:
    """修改 Agent：根据审核意见修改报告"""
    report = state["report"]
    score = state["review_score"]

    prompt = f"报告当前评分{score}分（满分100），请优化改进。原报告：\n{report}"
    response = model.invoke([HumanMessage(content=prompt)])

    state["report"] = response.content
    state["messages"] = state.get("messages", []) + [
        AIMessage(content=f"[修改] 报告已优化：{response.content}")
    ]
    return state


# ============================================================================
# 第三步：定义 Edges（边 = 流转规则）
# ============================================================================
# "边"决定了工作流的走向——从哪个节点出发，到哪个节点结束。
#
# 类比：工厂的传送带
#   - 普通边（add_edge）：固定路线，A 完成后必到 B
#   - 条件边（add_conditional_edges）：岔路口，根据条件决定走哪条路
#
# 面试要点：
# - 普通边：固定流转（research → write）
# - 条件边：根据 State 动态决定下一步（router 函数返回节点名称）

def router(state: AgentState) -> Literal["revise", "finish"]:
    """
    路由函数：根据审核评分决定下一步
    面试要点：router 返回的是下一个节点的名称
    """
    score = state.get("review_score", 0)
    if score < 80:
        print(f"[路由] 评分 {score} < 80，进入修改节点")
        return "revise"
    else:
        print(f"[路由] 评分 {score} >= 80，流程结束")
        return "finish"


# ============================================================================
# 第四步：构建 Graph（把节点和边组装起来）
# ============================================================================

def build_workflow():
    """
    构建多 Agent 协作工作流

    这一步就像"组装流水线"：
    1. 先搭一个空架子（StateGraph）
    2. 把各个工位（节点）装上去
    3. 把传送带（边）连接起来
    4. 最后通电启动（compile）
    """

    # 第一步：创建一个空的工作流图
    # StateGraph 是 LangGraph 的核心类，负责管理状态和节点流转
    workflow = StateGraph(AgentState)

    # 第二步：添加节点
    # 每个节点有一个名字（字符串）和一个处理函数
    # 名字用于在边中引用，函数定义了节点要做什么
    workflow.add_node("research", research_node)   # 研究节点
    workflow.add_node("write", write_node)          # 撰写节点
    workflow.add_node("review", review_node)        # 审核节点
    workflow.add_node("revise", revise_node)        # 修改节点

    # 第三步：添加边（连接节点，定义流转规则）

    # set_entry_point：设置入口节点，工作流从这里开始执行
    workflow.set_entry_point("research")

    # add_edge：普通边，固定流转
    # "research" 完成后一定走到 "write"
    workflow.add_edge("research", "write")

    # "write" 完成后一定走到 "review"
    workflow.add_edge("write", "review")

    # add_conditional_edges：条件边，根据 router 函数的返回值决定走向
    # router 返回 "revise" -> 走到 revise 节点
    # router 返回 "finish" -> 走到 END（工作流结束）
    workflow.add_conditional_edges(
        "review",           # 从 review 节点出发
        router,             # 用 router 函数决定下一步去哪
        {
            "revise": "revise",   # router 返回 "revise" -> 去 revise 节点
            "finish": END         # router 返回 "finish" -> 结束工作流
        }
    )

    # 关键！这里形成了"循环"：
    # revise（修改）完成后回到 review（重新审核）
    # 如果审核不通过，会再次进入 revise，形成循环
    # 直到审核通过（score >= 80），router 返回 "finish"，循环才结束
    workflow.add_edge("revise", "review")

    # 第四步：编译工作流
    # compile() 把上面的定义转换成可执行的对象
    # checkpointer 会自动保存每个节点的状态快照，支持断点续传和重试
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)

    return app


# ========================
# 第五步：运行测试
# ========================

if __name__ == "__main__":
    print("=" * 50)
    print("LangGraph 多 Agent 工作流演示")
    print("=" * 50)

    app = build_workflow()

    # 初始状态
    initial_state = {
        "messages": [],
        "topic": "人工智能 Agent 的未来发展趋势",
        "research_result": "",
        "report": "",
        "review_score": 0,
        "next_step": ""
    }

    # 运行工作流
    # 面试要点：stream 可以看到每个节点的执行过程
    print("\n🚀 启动工作流...\n")
    for event in app.stream(initial_state, config={"configurable": {"thread_id": "demo-1"}}):
        for node_name, node_state in event.items():
            print(f"📍 节点 [{node_name}] 执行完成")
            if "report" in node_state and node_state["report"]:
                print(f"   当前报告：{node_state['report'][:60]}...")
            if "review_score" in node_state and node_state["review_score"]:
                print(f"   当前评分：{node_state['review_score']}")
            print()

    print("=" * 50)
    print("✅ 工作流执行完毕")
    print("=" * 50)

"""
【面试追问准备】

Q: LangGraph 和之前手写的 Multi-Agent Orchestrator 有什么区别？
A: 手写版是硬编码的 Pipeline（研究→撰写→审核→修改），LangGraph 用声明式图定义：
   - 节点和边解耦，易于扩展
   - 支持循环（审核不通过 → 修改 → 重新审核）
   - 支持条件分支（根据评分决定走向）
   - 内置 checkpoint，支持断点续传

Q: checkpointer 有什么用？
A: checkpoint 会自动保存每个节点的 State 快照：
   - 节点执行失败后可以从上一个 checkpoint 重试
   - 支持 Human-in-the-loop（在节点间暂停等待人工确认）
   - 可以查看完整执行轨迹，便于调试

Q: 怎么实现 Human-in-the-loop？
A: LangGraph 支持 interrupt：
   - 在关键节点（如审核）设置 interrupt_before=True
   - 工作流暂停，等待人类输入（approve/reject）
   - 人类确认后，从 checkpoint 继续执行

Q: LangGraph 支持并行执行吗？
A: 支持！用 `add_edge` 让多个节点从同一个节点出发，
   或者用 `RunnableParallel` 在单个节点内并行执行子任务。

Q: LangGraph 的 State 怎么保证线程安全？
A: 每个 thread_id 有独立的 State 副本，互不影响；
   多线程共享数据需要通过外部存储（Redis/数据库）。
"""

`
