# Git 面试冲刺 —— 进阶概念与实战场景

> 面向有基础的用户，覆盖面试中的进阶问题和实际工作场景

---

## 一、Git 进阶命令与场景

### 1. git stash —— 临时保存工作现场

**场景**：你正在改代码，突然需要切换到另一个分支修 bug，但当前改动还没完成不想 commit。

```bash
# 把当前工作区和暂存区的改动暂时存起来
git stash

# 查看 stash 列表
git stash list

# 恢复最近一次 stash
git stash pop

# 恢复指定 stash
git stash apply stash@{2}

# 删除指定 stash
git stash drop stash@{0}
```

**面试考点**：stash 存的是工作区 + 暂存区的改动，不会提交到版本库。

---

### 2. git cherry-pick —— 挑拣提交

**场景**：只想把某个分支上的某一个 commit 应用到当前分支，不想 merge 整个分支。

```bash
# 把指定的 commit 应用到当前分支
git cherry-pick <commit-id>

# 如果出现冲突，解决后
git add .
git cherry-pick --continue

# 放弃 cherry-pick
git cherry-pick --abort
```

**面试考点**：cherry-pick 会创建一个新的 commit（新哈希），内容相同但 ID 不同。

---

### 3. git revert —— 安全回退

**场景**：某个 commit 引入了 bug，想撤销它的改动，但不想删除历史记录（因为别人可能已经基于它开发了）。

```bash
# 创建一个新的 commit，抵消指定 commit 的改动
git revert <commit-id>

# 撤销多个连续的 commit
git revert HEAD~3..HEAD
```

**与 reset 的区别**：
- `reset`：修改历史，删除 commit（危险）
- `revert`：保留历史，新增一个"反向 commit"（安全，适合公共分支）

---

### 4. git reflog —— 后悔药

**场景**：你不小心用了 `git reset --hard`，丢了好几次 commit。

```bash
# 查看 HEAD 的所有变动记录（包括被删除的 commit）
git reflog

# 恢复被误删的 commit
git checkout <commit-id>
git checkout -b recovery-branch
```

**面试考点**：reflog 记录了 HEAD 的每一次移动（commit、checkout、reset、merge 等），默认保留 90 天。

---

### 5. .gitignore 详解

**作用**：告诉 Git 哪些文件不需要跟踪（如编译产物、临时文件、密钥等）。

```
# 忽略所有 .log 文件
*.log

# 忽略 node_modules 目录
node_modules/

# 忽略所有 .pyc 文件
*.pyc

# 忽略 build 目录下的所有内容
build/

# 但不忽略 build/config.js（例外规则）
!build/config.js

# 忽略以 temp 开头的文件
temp*

# 忽略 .env 文件（包含敏感信息）
.env
```

**面试坑点**：
- `.gitignore` 对已跟踪的文件无效！如果文件已经被 commit，需要先 `git rm --cached 文件名`，再加到 `.gitignore`
- 全局 `.gitignore`：`git config --global core.excludesfile ~/.gitignore_global`

---

### 6. GitFlow 工作流（⭐⭐⭐）

**GitFlow 是一种分支管理策略**：

```
main          ●───●───●───●───●───●
              │       │       │
release       └──●───●       │
                   │         │
develop       ●───●───●───●───●───●
              │   │   │   │
feature       │   └──●───● │
              │       │    │
feature2      └───────●───●│
                           │
hotfix                     └──●───●
```

**分支说明**：
| 分支 | 作用 |
|------|------|
| `main` | 生产环境代码，永远可部署 |
| `develop` | 开发主线，功能集成 |
| `feature/*` | 新功能开发，从 develop 分出来 |
| `release/*` | 版本发布准备，从 develop 分出来 |
| `hotfix/*` | 紧急修复生产 bug，从 main 分出来 |

**面试考点**：GitFlow 适合发布周期固定的项目；如果是持续部署（CI/CD），可以用更简单的 GitHub Flow（只有 main + feature 分支）。

---

## 二、Git 面试进阶真题

### 【真题 7】`.gitignore` 对已经跟踪的文件无效，怎么处理？（⭐⭐⭐）

**答题模板**：
1. 先用 `git rm --cached 文件名` 把文件从版本库中移除（但保留本地文件）
2. 把文件名加到 `.gitignore`
3. `git commit -m "停止跟踪某文件"`
4. 注意：这只会影响后续提交，历史版本中该文件仍然存在（需要 `git filter-branch` 或 BFG 清理历史）

---

### 【真题 8】git revert 和 git reset 有什么区别？什么时候用哪个？（⭐⭐⭐⭐）

**答题模板**：
1. `git revert`：创建一个新的 commit，反向应用指定 commit 的改动。历史记录保留，适合公共分支。
2. `git reset`：移动 HEAD 指针到指定 commit，可以修改/删除历史。适合本地分支，不适合已 push 的分支。
3. **选择原则**：
   - 本地开发，还没 push -> `reset`（可以重写历史）
   - 公共分支，已经 push -> `revert`（不破坏他人工作）
4. **常见坑点**：reset 后强制 push（`git push --force`）会覆盖远程历史，团队协作中很危险。

---

### 【真题 9】怎么删除已经 push 到远程的敏感信息（如密码、API Key）？（⭐⭐⭐⭐）

**答题模板**：
1. **轻度方案**：从当前版本中删除，提交新版本。但历史版本中仍然有敏感信息，可以通过 commit 历史查看。
2. **彻底方案**：使用 BFG Repo-Cleaner 或 `git filter-branch` 重写历史，从所有 commit 中删除敏感文件。
3. **步骤**：
   ```bash
   # 使用 BFG（推荐）
   bfg --delete-files .env
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   git push --force
   ```
4. **关键**：重写历史后必须 `git push --force`，且团队成员需要重新 clone 仓库。
5. **最佳实践**：敏感信息永远不放 Git，用环境变量或 Vault 管理。

---

### 【真题 10】Git 的底层是怎么存储文件的？（⭐⭐⭐）

**答题模板**：
1. Git 使用"内容寻址文件系统"（Content-Addressable Filesystem）。
2. 每个文件内容计算 SHA-1 哈希，作为文件名存储在 `.git/objects` 中。
3. 相同内容只存一份：如果两个文件内容相同，它们共享同一个 blob 对象。
4. Commit 对象包含：tree（目录结构）、父 commit、作者、时间、提交信息。
5. **优势**：因为基于内容寻址，改名和移动文件不会增加存储（内容没变）。

---

## 三、实际工作场景模拟

### 场景 1：代码写了一半，要临时修生产 bug

```bash
# 1. 保存当前工作现场
git stash push -m "开发到一半的登录功能"

# 2. 切换到 main，创建 hotfix 分支
git checkout main
git checkout -b hotfix/bug-123

# 3. 修 bug，提交
git add .
git commit -m "修复 bug #123"

# 4. 合并回 main，push
git checkout main
git merge hotfix/bug-123
git push

# 5. 回到之前的开发分支，恢复现场
git checkout feature-login
git stash pop
```

### 场景 2：提交写错了信息

```bash
# 最后一次 commit 信息写错了，修改
git commit --amend -m "正确的提交信息"

# 注意：如果已经 push 到远程，amend 后需要 force push（小心！）
git push --force-with-lease
```

### 场景 3：把不该提交的文件删了

```bash
# 1. 先确认文件在哪个 commit 里
git log -- 文件名

# 2. 恢复文件到当前工作区
git checkout <commit-id> -- 文件名

# 3. 重新提交
git add 文件名
git commit -m "恢复误删文件"
```

---

## 四、Git 命令速查表（面试前打印出来背诵）

```bash
# ========== 基础 ==========
git init                          # 初始化仓库
git clone <url>                   # 克隆仓库
git status                        # 查看状态
git add <file>                    # 添加文件到暂存区
git add .                         # 添加所有改动
git commit -m "msg"              # 提交
git log --oneline                 # 简洁历史
git log --graph --all            # 图形化历史

# ========== 分支 ==========
git branch                        # 列出分支
git branch <name>                 # 创建分支
git checkout <branch>            # 切换分支
git checkout -b <name>           # 创建并切换
git merge <branch>               # 合并分支
git branch -d <name>             # 删除分支

# ========== 远程 ==========
git remote -v                     # 查看远程地址
git fetch                         # 下载远程更新
git pull                          # 拉取并合并
git push                          # 推送到远程
git push -u origin main          # 首次推送并关联

# ========== 撤销 ==========
git checkout -- <file>          # 撤销工作区修改
git reset HEAD <file>           # 从暂存区撤出
git reset --soft HEAD~1         # 撤销 commit，保留 staged
git reset --mixed HEAD~1        # 撤销 commit，保留工作区
git reset --hard HEAD~1         # 彻底回退（危险！）
git revert <commit>             # 反向提交（安全）

# ========== 进阶 ==========
git stash                         # 临时保存
git stash pop                     # 恢复并删除 stash
git cherry-pick <commit>        # 挑拣提交
git reflog                        # 查看 HEAD 变动记录
git tag <name>                   # 打标签
git diff                          # 查看工作区改动
git diff --cached                # 查看暂存区改动
```

---

*本节完毕！建议：在本地测试仓库中，把每个命令都运行一遍，熟悉输出结果。*
