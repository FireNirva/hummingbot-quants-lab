# 📤 Git 上传指南

本指南帮助你将 QuantsLab 项目上传到 GitHub。

---

## ✅ **准备工作（已完成）**

- [x] 清理重复和临时文件（45 个文件已删除）
- [x] 整理文件结构（docs/ 和 scripts/）
- [x] 创建文档索引（docs/INDEX.md, scripts/README.md）
- [x] 更新主 README.md
- [x] .gitignore 已存在

---

## 🚀 **上传步骤**

### **1. 初始化 Git 仓库（如果还没有）**

```bash
cd /Users/alice/Dropbox/投资/量化交易/quants-lab

# 检查是否已经是 Git 仓库
if [ -d .git ]; then
    echo "✅ 已经是 Git 仓库"
else
    echo "初始化 Git 仓库..."
    git init
fi
```

---

### **2. 查看将要上传的文件**

```bash
# 查看所有文件状态
git status

# 查看哪些文件会被忽略
git status --ignored
```

**预期输出**：
```
新文件:
  - README.md (已更新)
  - docs/INDEX.md
  - scripts/README.md
  - docs/PROJECT_ORGANIZATION_SUMMARY.md
  等等...

忽略的文件:
  - __pycache__/
  - *.pyc
  - .env
  - app/data/raw/
  - app/data/cache/
  - user_data/
  等等...
```

---

### **3. 添加文件到 Git**

```bash
# 添加所有文件
git add .

# 查看将要提交的文件
git status
```

---

### **4. 创建提交**

```bash
# 创建提交（建议的提交信息）
git commit -m "feat: 完整的 CEX-DEX 套利和订单簿采集系统

主要功能：
- ✅ CEX-DEX 跨交易所套利分析（Gate.io, MEXC, Uniswap）
- ✅ 5秒高频订单簿数据采集（100档深度）
- ✅ 流动性分析和最优交易规模计算
- ✅ 多交易所和多链支持（Base, BSC, Solana）
- ✅ AWS 一键部署
- ✅ 完整文档系统（55个文档，36个脚本）

技术栈：
- Python 3.12+
- Pandas, Parquet（高性能数据存储）
- asyncio（并发订单簿采集）
- Freqtrade（CEX 数据）
- GeckoTerminal（DEX 数据）

清理和整理：
- 删除 45 个重复/临时文件
- 整理文件结构（docs/, scripts/）
- 创建完整索引和文档"
```

---

### **5. 连接 GitHub 仓库**

#### **方法 A：新建 GitHub 仓库（推荐）**

1. 访问 https://github.com/new
2. 创建新仓库：
   - **Repository name**: `quants-lab` 或你喜欢的名称
   - **Description**: `CEX-DEX 跨交易所套利和高频订单簿采集系统`
   - **Public/Private**: 根据需要选择
   - **不要** 初始化 README、.gitignore 或 License（我们已经有了）
3. 创建后，GitHub 会显示命令

```bash
# 添加远程仓库（替换 YOUR-USERNAME 和 REPO-NAME）
git remote add origin https://github.com/YOUR-USERNAME/REPO-NAME.git

# 或使用 SSH（推荐）
git remote add origin git@github.com:YOUR-USERNAME/REPO-NAME.git
```

#### **方法 B：使用现有仓库**

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR-USERNAME/EXISTING-REPO.git

# 或更新现有远程
git remote set-url origin https://github.com/YOUR-USERNAME/EXISTING-REPO.git
```

---

### **6. 推送到 GitHub**

```bash
# 推送主分支
git push -u origin main

# 如果分支名是 master
git push -u origin master

# 如果遇到错误：Updates were rejected
# 先拉取远程更改
git pull origin main --rebase
git push -u origin main
```

---

### **7. 验证上传**

访问你的 GitHub 仓库页面，确认：
- ✅ README.md 正确显示
- ✅ docs/ 和 scripts/ 目录完整
- ✅ 文件数量正确
- ✅ 没有上传敏感数据（.env, 数据文件等）

---

## 🔒 **安全检查**

### **确保以下文件/目录被忽略**

```bash
# 查看 .gitignore 内容
cat .gitignore

# 验证敏感文件没有被跟踪
git ls-files | grep -E '\.env|password|secret|key'

# 如果有，立即取消跟踪
git rm --cached .env
git commit -m "chore: 移除敏感文件"
```

### **应该被忽略的目录**

- ✅ `__pycache__/`
- ✅ `*.pyc`
- ✅ `.env`
- ✅ `app/data/raw/` （订单簿原始数据）
- ✅ `app/data/cache/` （缓存数据）
- ✅ `user_data/` （用户数据）
- ✅ `logs/` （日志文件）
- ✅ `.vscode/`
- ✅ `.idea/`

---

## 📝 **后续更新**

### **常规提交流程**

```bash
# 1. 查看修改
git status

# 2. 添加修改
git add .

# 3. 提交
git commit -m "feat: 添加新功能"
# 或
git commit -m "fix: 修复 bug"
# 或
git commit -m "docs: 更新文档"

# 4. 推送
git push
```

### **提交信息规范**

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
feat: 新功能
fix: Bug 修复
docs: 文档更新
style: 代码格式（不影响功能）
refactor: 重构
perf: 性能优化
test: 测试
chore: 构建/工具链
```

**示例**：
```bash
git commit -m "feat: 添加 MEXC 订单簿采集支持"
git commit -m "fix: 修复订单簿重复 Update ID 问题"
git commit -m "docs: 更新 AWS 部署指南"
git commit -m "perf: 优化订单簿采集精度到 5.00 秒"
```

---

## 🌿 **分支管理（可选）**

### **创建开发分支**

```bash
# 创建并切换到开发分支
git checkout -b develop

# 进行开发...
git add .
git commit -m "feat: 新功能开发中"

# 推送开发分支
git push -u origin develop

# 开发完成后，合并到主分支
git checkout main
git merge develop
git push
```

---

## 🏷️ **创建版本标签（可选）**

```bash
# 创建标签
git tag -a v1.0.0 -m "Release v1.0.0: 完整的 CEX-DEX 套利系统"

# 推送标签
git push origin v1.0.0

# 推送所有标签
git push origin --tags
```

---

## 🚨 **常见问题**

### **问题 1：推送失败 - Updates were rejected**

**原因**：远程仓库有本地没有的提交

**解决**：
```bash
git pull origin main --rebase
git push
```

---

### **问题 2：文件太大**

**原因**：GitHub 有 100MB 单文件限制

**解决**：
```bash
# 查找大文件
find . -type f -size +10M | grep -v .git

# 将大文件添加到 .gitignore
echo "path/to/large/file" >> .gitignore

# 如果已经提交，从历史中删除
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/large/file" \
  --prune-empty --tag-name-filter cat -- --all
```

---

### **问题 3：忘记添加 .gitignore**

**解决**：
```bash
# 确保 .gitignore 存在并正确
cat .gitignore

# 移除已跟踪的应该被忽略的文件
git rm -r --cached app/data/raw/
git rm -r --cached app/data/cache/
git rm -r --cached __pycache__/

# 提交
git commit -m "chore: 更新 .gitignore 并移除不需要的文件"
git push
```

---

### **问题 4：敏感信息已上传**

**紧急处理**：
```bash
# 1. 立即改密码/密钥
# 2. 从历史中删除
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# 3. 强制推送（危险！）
git push origin --force --all
```

---

## ✅ **上传检查清单**

完成以下检查后再推送：

- [ ] README.md 已更新
- [ ] 文档索引已创建（docs/INDEX.md, scripts/README.md）
- [ ] 没有敏感信息（.env, 密钥等）
- [ ] 没有大文件（> 50MB）
- [ ] 没有不必要的数据文件
- [ ] .gitignore 正确配置
- [ ] 提交信息清晰
- [ ] 代码可以正常运行

---

## 📚 **参考资源**

- [Git 官方文档](https://git-scm.com/doc)
- [GitHub 使用指南](https://docs.github.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [.gitignore 模板](https://github.com/github/gitignore)

---

**准备好了就上传吧！🚀**

