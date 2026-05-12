# Context 压缩与总结实践（Compaction）

> 解决长会话上下文窗口溢出的核心方案

---

## 一、为什么需要 Compaction

当 Agent 运行多轮后，上下文会出现：
- **Token 爆炸**：工具输出、观察、思考层层累积
- **信号稀释**：关键指令被淹没在大量历史消息中
- **成本飙升**：API 按 token 计费，冗余上下文 = 浪费钱

**Compaction = 接近窗口限制时，总结历史并丢弃冗余，重启新上下文**

---

## 二、三种压缩策略

### 策略 1：Tool Result Clearing（工具结果清理）

**适用场景**：工具已执行完成，结果已使用

**原理**：清空历史消息中的工具调用和结果，保留决策和观察

```python
# compaction_tool_clearing.py
"""
轻量级 Compaction：清理已完成的工具输出
保留：用户指令、模型决策、关键观察
丢弃：具体的工具调用 JSON、冗余的工具返回结果
"""

def compact_tool_results(messages, keep_last_n=3):
    """
    清理消息历史中的工具输出，只保留最近 N 轮的完整信息
    """
    compacted = []
    
    for i, msg in enumerate(messages):
        # 保留系统消息
        if msg.get("role") == "system":
            compacted.append(msg)
            continue
            
        # 保留用户消息
        if msg.get("role") == "user":
            compacted.append(msg)
            continue
            
        # 对于 assistant 消息，判断是否是最近 N 轮
        rounds_from_end = len(messages) - i
        if rounds_from_end <= keep_last_n:
            # 最近 N 轮保留完整信息
            compacted.append(msg)
        else:
            # 更早的消息，只保留决策摘要
            if msg.get("tool_calls"):
                # 保留工具调用决策，但清空具体参数
                compacted.append({
                    "role": "assistant",
                    "content": f"[已执行工具: {len(msg['tool_calls'])} 个]"
                })
            else:
                # 保留内容摘要（实际实现中可以用模型总结）
                content = msg.get("content", "")
                if len(content) > 100:
                    compacted.append({
                        "role": "assistant", 
                        "content": f"[历史总结: {content[:100]}...]"
                    })
                else:
                    compacted.append(msg)
    
    return compacted


# ============ 演示 ============
if __name__ == "__main__":
    # 模拟一个运行了 10 轮的消息历史
    messages = [
        {"role": "system", "content": "你是一个文件管理助手"},
        {"role": "user", "content": "帮我整理桌面文件"},
        {"role": "assistant", "content": "我来帮你整理桌面文件。首先让我查看当前桌面结构。", 
         "tool_calls": [{"id": "call_1", "function": {"name": "list_dir", "arguments": '{"path": "~/Desktop"}'}}]},
        {"role": "tool", "content": "文件1.txt, 文件2.pdf, 图片1.jpg, 图片2.png, 文档.docx"},
        {"role": "assistant", "content": "我看到桌面有 5 个文件。建议按类型分类：文档、图片、其他。",
         "tool_calls": [{"id": "call_2", "function": {"name": "create_folders", "arguments": '{"folders": ["文档", "图片", "其他"]}'}}]},
        {"role": "tool", "content": "文件夹创建成功: 文档/, 图片/, 其他/"},
        {"role": "assistant", "content": "文件夹已创建。现在开始移动文件。",
         "tool_calls": [{"id": "call_3", "function": {"name": "move_files", "arguments": '{"mapping": {"*.txt": "文档", "*.docx": "文档", "*.jpg": "图片", "*.png": "图片"}}'}}]},
        {"role": "tool", "content": "文件移动完成"},
        {"role": "assistant", "content": "整理完成！桌面文件已分类存放。"},
        {"role": "user", "content": "现在帮我检查下载文件夹"},
        {"role": "assistant", "content": "让我查看下载文件夹。",
         "tool_calls": [{"id": "call_4", "function": {"name": "list_dir", "arguments": '{"path": "~/Downloads"}'}}]},
        {"role": "tool", "content": "[大量文件列表... 超过 2000 tokens]"},
    ]
    
    print("=== 压缩前 ===")
    print(f"消息数: {len(messages)}")
    
    compacted = compact_tool_results(messages, keep_last_n=2)
    
    print(f"\n=== 压缩后 (保留最近 2 轮) ===")
    print(f"消息数: {len(compacted)}")
    for msg in compacted:
        role = msg.get("role")
        content = msg.get("content", "")[:50]
        print(f"  [{role}] {content}...")
```

**面试要点**：
- 这是最轻量的 Compaction，安全性高（不会丢失关键决策）
- Claude Developer Platform 已上线此功能
- 适合：工具调用频繁、结果已消费的场景

---

### 策略 2：Sliding Window（滑动窗口）

**适用场景**：对话流式进行，早期信息相关性随时间降低

**原理**：只保留最近 K 轮对话，丢弃更早的历史

```python
# compaction_sliding_window.py
"""
滑动窗口 Compaction：保留最近 N 轮，丢弃更早历史
适合：闲聊型、流式进行的对话
注意：不适合需要长期依赖的任务（如代码迁移、复杂项目）
"""

def sliding_window(messages, max_rounds=5, preserve_system=True):
    """
    滑动窗口压缩
    - max_rounds: 保留的最近对话轮数
    - preserve_system: 是否始终保留系统消息
    """
    # 分离系统消息
    system_msgs = [m for m in messages if m.get("role") == "system"] if preserve_system else []
    
    # 非系统消息按轮分组
    non_system = [m for m in messages if m.get("role") != "system"]
    
    # 保留最近 max_rounds 轮（每轮通常包含 user + assistant + tool）
    # 简单实现：按消息数量截断
    kept = non_system[-max_rounds * 3:]  # 假设每轮平均 3 条消息
    
    return system_msgs + kept


def sliding_window_with_summary(messages, max_rounds=5):
    """
    增强版：丢弃的历史用一句话总结替代
    """
    system_msgs = [m for m in messages if m.get("role") == "system"]
    non_system = [m for m in messages if m.get("role") != "system"]
    
    if len(non_system) <= max_rounds * 3:
        return messages
    
    # 更早的历史生成摘要
    older = non_system[:-max_rounds * 3]
    recent = non_system[-max_rounds * 3:]
    
    # 实际生产中，这里应该用 LLM 总结
    # 简化版：用用户消息拼接作为摘要
    user_msgs = [m.get("content", "") for m in older if m.get("role") == "user"]
    summary = "[历史对话摘要: " + "; ".join(user_msgs[:3]) + "...]"
    
    summary_msg = {"role": "assistant", "content": summary}
    
    return system_msgs + [summary_msg] + recent


# ============ 演示 ============
if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "你是编程助手"},
        {"role": "user", "content": "写个快速排序"},
        {"role": "assistant", "content": "快速排序代码..."},
        {"role": "user", "content": "改成降序"},
        {"role": "assistant", "content": "降序版本..."},
        {"role": "user", "content": "加注释"},
        {"role": "assistant", "content": "带注释版本..."},
        {"role": "user", "content": "测试一下"},
        {"role": "assistant", "content": "测试代码..."},
        {"role": "user", "content": "优化性能"},  # 当前轮
        {"role": "assistant", "content": "优化版本..."},
    ]
    
    print("=== 原始消息 ===")
    print(f"消息数: {len(messages)}")
    
    compacted = sliding_window_with_summary(messages, max_rounds=2)
    print(f"\n=== 滑动窗口后 (保留最近 2 轮 + 摘要) ===")
    print(f"消息数: {len(compacted)}")
    for msg in compacted:
        print(f"  [{msg['role']}] {msg['content'][:40]}...")
```

**面试要点**：
- 简单但粗暴，可能丢失关键上下文
- 改进版：丢弃部分用 LLM 生成摘要替代
- 适合：闲聊、简单问答；不适合：复杂项目、代码迁移

---

### 策略 3：LLM-based Compaction（模型驱动的压缩）

**适用场景**：长时任务（代码迁移、研究项目、多步骤工作流）

**原理**：让 LLM 自己总结对话历史，生成高保真摘要

```python
# compaction_llm_based.py
"""
LLM-based Compaction：让模型自己总结历史
核心：高保真摘要 = 保留关键决策 + 未完成任务 + 架构选择
丢弃：冗余工具输出、已完成步骤的详细过程

这是生产级 Agent（如 Claude Code）使用的方案
"""

COMPACTION_PROMPT = """你正在维护一个 AI Agent 的上下文窗口。当前对话即将超出长度限制，请对历史对话进行压缩总结。

## 压缩规则
1. **必须保留**：
   - 用户的原始目标和需求
   - 已做出的关键架构决策
   - 未完成的任务和待办事项
   - 已发现的 bug 或问题
   - 最近访问/修改的文件列表

2. **可以丢弃**：
   - 已完成的工具调用详细输出
   - 中间探索过程的失败尝试
   - 已确认正确的代码实现细节

3. **输出格式**：
   用简洁的Markdown格式输出总结，不要有多余解释。

## 历史对话
{conversation_history}

## 请输出压缩后的摘要
"""


def compact_with_llm(messages, llm_client, model="gpt-4o-mini"):
    """
    使用 LLM 对消息历史进行智能压缩
    生产环境中，这里调用实际的 LLM API
    """
    # 将消息历史拼接成文本
    history_text = "\n".join([
        f"[{m.get('role', 'unknown')}] {m.get('content', '')[:200]}"
        for m in messages
    ])
    
    # 构建压缩提示
    prompt = COMPACTION_PROMPT.format(conversation_history=history_text)
    
    # 实际生产代码：调用 LLM
    # summary = llm_client.chat.completions.create(
    #     model=model,
    #     messages=[{"role": "user", "content": prompt}],
    #     max_tokens=2000
    # ).choices[0].message.content
    
    # 模拟输出（实际使用时替换为真实 LLM 调用）
    summary = """## 任务摘要
- **目标**：重构项目中的数据处理模块
- **关键决策**：
  - 使用 Pandas 替代原生 Python 处理 CSV
  - 采用批处理方式处理大文件（chunk_size=10000）
- **未完成任务**：
  - [ ] 异常值检测逻辑待完善
  - [ ] 性能基准测试待运行
- **已知问题**：
  - 内存占用过高，需要流式处理优化
- **最近文件**：data_processor.py, config.yaml, test_data.csv
"""
    
    # 保留系统消息 + 压缩摘要 + 最近 2 轮完整对话
    system_msgs = [m for m in messages if m.get("role") == "system"]
    recent = [m for m in messages if m.get("role") != "system"][-4:]
    
    compacted = system_msgs + [
        {"role": "assistant", "content": f"[上下文压缩摘要]\n{summary}"}
    ] + recent
    
    return compacted


# ============ 演示 ============
if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "你是代码重构助手，帮助优化数据处理模块"},
        {"role": "user", "content": "帮我重构 data_processor.py，当前处理 1GB CSV 会内存溢出"},
        {"role": "assistant", "content": "我来分析当前实现...",
         "tool_calls": [{"function": {"name": "read_file", "arguments": '{"path": "data_processor.py"}'}}]},
        {"role": "tool", "content": "[文件内容... 使用 pd.read_csv() 一次性加载整个文件...]"},
        {"role": "assistant", "content": "问题确认：当前使用 pd.read_csv() 一次性加载，建议改为 chunk 处理。",
         "tool_calls": [{"function": {"name": "modify_file", "arguments": '{"path": "data_processor.py", "changes": "..."}'}}]},
        {"role": "tool", "content": "[修改后的代码... chunk_size=10000...]"},
        {"role": "assistant", "content": "已修改。现在测试一下性能...",
         "tool_calls": [{"function": {"name": "run_test", "arguments": '{"test": "test_large_csv"}'}}]},
        {"role": "tool", "content": "[测试输出... 内存占用降低 80%，但异常值检测未通过...]"},
        {"role": "user", "content": "异常值检测怎么处理？"},  # 当前轮
        {"role": "assistant", "content": "让我查看异常值检测逻辑..."},
    ]
    
    print("=== 压缩前 ===")
    print(f"消息数: {len(messages)}")
    total_chars = sum(len(str(m)) for m in messages)
    print(f"总字符数: {total_chars}")
    
    # 模拟 LLM 压缩
    compacted = compact_with_llm(messages, llm_client=None)
    
    print(f"\n=== LLM 压缩后 ===")
    print(f"消息数: {len(compacted)}")
    new_chars = sum(len(str(m)) for m in compacted)
    print(f"总字符数: {new_chars}")
    print(f"压缩率: {(1 - new_chars/total_chars)*100:.1f}%")
    
    print("\n压缩摘要内容:")
    for msg in compacted:
        if "摘要" in str(msg.get("content", "")):
            print(msg["content"])
```

**面试要点**：
- 这是生产级方案（Claude Code、Devin 都在用）
- 核心：提示词要指导模型保留什么、丢弃什么
- 压缩质量取决于总结 prompt 的设计
- 挑战：过度压缩会丢失 subtle but critical 的信息

---

## 三、Compaction 策略选择指南

| 场景 | 推荐策略 | 原因 |
|------|---------|------|
| 工具调用频繁，结果已消费 | Tool Result Clearing | 安全性高，几乎零风险 |
| 闲聊、简单问答 | Sliding Window + Summary | 简单有效，实现成本低 |
| 代码迁移、复杂项目 | LLM-based Compaction | 保留关键决策，保证连贯性 |
| 超长文档处理（>100K tokens） | 分层 Compaction | 多级摘要，按需展开 |

---

## 四、面试答题模板

**Q：如何处理 Agent 长会话中的上下文窗口溢出？**

**A**：
> 我采用分层 Compaction 策略。首先做轻量级的 Tool Result Clearing，清理已完成的工具输出；当接近窗口限制时，触发 LLM-based Compaction，让模型总结关键决策、未完成任务和架构选择，同时保留最近 2-3 轮完整对话保证连贯性。在 Claude Code 的实践中，这种方案能支持数小时的连续代码迁移任务。

**Q：Compaction 会不会丢失重要信息？**

**A**：
> 这是核心挑战。我的做法是：在压缩 prompt 中明确要求保留"关键决策、未完成任务、已知问题、最近文件"，并建议先做最大化召回的总结，再迭代消除冗余。Claude Plays Pokémon 的案例证明，只要总结得当，Agent 能在数千步后依然保持策略连贯性。
```
