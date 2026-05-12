# AI 面试学习知识库

> 基于 MkDocs Material 构建的个人面试知识库，聚焦 **AI Agent、Python、Git、Vibe Coding 流程和综合面试模拟题**。  
> 当前项目已清理学习进度、遗漏检查和个人问答准备类内容，只保留详细知识点、代码实践和面试模拟题。

## 在线访问

```text
https://Yiang-Puak.github.io/study/
```

站点支持：

- 全文搜索
- 深色 / 浅色模式
- 移动端自适应阅读
- 代码块复制
- Mermaid 图表渲染

## 内容结构

### AI Agent 面试实践

围绕 AI Agent 面试高频概念进行系统整理：

- AI 系统底层框架全景图
- LLM 与 Token 底层原理
- Context Window、Memory、RAG
- Agent 基础架构、Agentic Loop、ReAct、Function Call
- Multi-Agent 协作
- LangChain / LangGraph
- Prompt 工程
- Harness 工程
- Tool 与 MCP 工程实践
- Explore-Plan-Act 与 Agent Skill
- AI Agent 综合模拟面试题库

### Vibe Coding 流程

整理如何借助 AI 编程工具完成一个真实项目：

- 需求澄清
- PRD 编写
- 技术方案设计
- 任务拆解
- Prompt 设计
- 迭代开发
- 测试验收
- 部署交付
- 复盘优化

### 综合面试冲刺

用于集中复习跨方向的综合材料：

- 项目介绍表达
- 面试答题结构
- 高频综合问题
- 面试前快速复盘

### Python 面试实践

覆盖 Python 基础、语言特性、常用数据结构和高频手撕题：

- 变量与数据类型
- 输入输出与运算符
- 条件判断与循环
- 字符串操作
- 函数基础
- Python 语言特性
- 内置数据结构
- 滑动窗口、快速排序、LRU、TopK、二分查找、动态规划等题型

### Git 面试实践

整理 Git 面试和日常工程协作必备内容：

- Git 核心概念
- 分支、提交、合并、冲突处理
- Git 进阶与实战

## 本地预览

在项目根目录执行：

```powershell
python -m mkdocs serve -a 127.0.0.1:8000
```

浏览器打开：

```text
http://127.0.0.1:8000
```

如果站点使用 `site_url` 跳转到 `/study/`，也可以访问：

```text
http://127.0.0.1:8000/study/
```

## 构建验证

推送前建议运行严格构建：

```powershell
python -m mkdocs build --strict
```

如果在中文路径下遇到工作目录识别问题，可以使用通用占位路径：

```powershell
python -m mkdocs build --strict -f "<project-root>\mkdocs.yml"
```

## 自动部署

项目使用 GitHub Actions 自动部署到 GitHub Pages。

推送到 `main` 分支后，会自动构建并发布到：

```text
https://Yiang-Puak.github.io/study/
```

常用提交命令：

```powershell
git add .
git commit -m "docs: update study notes"
git push origin main
```

如果需要避免中文路径导致命令目录错误，可以使用通用占位路径：

```powershell
git -C "<project-root>" add .
git -C "<project-root>" commit -m "docs: update study notes"
git -C "<project-root>" push origin main
```

## 技术栈

- MkDocs
- Material for MkDocs
- mkdocs-minify-plugin
- GitHub Actions
- GitHub Pages

## 项目原则

- 不保留个人隐私信息
- 不保留学习进度跟踪类页面
- 不保留遗漏检查类页面
- 内容以详细知识点和面试模拟题为主
- 每次重要调整后使用 `mkdocs build --strict` 验证
