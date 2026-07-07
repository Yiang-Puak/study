# AI Agent 工程学习手册

> 基于 MkDocs Material 构建的公开学习站点，聚焦 **AI Agent、Python 与面试真题训练**。
> 站点只保留知识点讲解、代码实践、真题追问、学习路线和速查材料，不发布离线参考素材与个人化信息。

## 站点能力

- 全文搜索
- 深色 / 浅色模式
- 移动端自适应阅读
- 代码块复制
- Mermaid 图表渲染
- GitHub Pages 自动构建
- 面试薄弱点回流与学习雷达

## 内容结构

### Agent 工程体系

围绕“知识点 -> 实践 -> 八股 -> 真题追问”整理 Agent 主线：

- Agent 总览与基础架构
- Context 与 Memory
- RAG 检索工程
- Tool Calling 与 MCP
- Workflow、LangGraph 与 Multi-Agent
- Eval、Trace 与 Safety
- 规划、Skill、Prompt 与工程复盘

### 面试题库

用于把专题理解压缩成可训练输出：

- 高频八股
- 工程追问
- 公开真题整理
- Python 面试真题
- 模拟口述训练

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

## 推荐学习顺序

1. 从首页进入 Agent 学习地图，先建立模型、上下文、检索、工具、编排和治理的依赖关系。
2. 每个 Agent 核心专题先看学习页，再看代码实践，最后刷八股和真题追问。
3. Python 先补语法和容器，再补语言特性，最后练手撕题与口述复杂度。
4. 面试前只走题库训练路线，把答不清的题回流到薄弱点回流表。
5. 用 GitHub 参考项目页对照优秀开源项目，补 LangGraph、RAG、Trace 和系统设计表达。

## 本地预览

在项目根目录执行：

```powershell
pip install -r requirements.txt
python -m mkdocs serve -a 127.0.0.1:8000
```

浏览器打开：

```text
http://127.0.0.1:8000
```

如果部署环境配置了子路径，也可以按部署路径访问：

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

项目可使用 GitHub Actions 自动部署到静态站点托管环境。

推送到发布分支后，由部署配置决定最终访问地址。

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

## 发布边界

- 不发布个人隐私、个人背景、投递计划和求职画像。
- 不发布离线参考报告 `deep-research-report*.md`。
- 不发布 MkDocs 生成目录 `site/`。
- 内容只围绕 Agent、Python 与面试题训练展开。
- 每次重要调整后优先使用 `python -m mkdocs build --strict` 验证。
