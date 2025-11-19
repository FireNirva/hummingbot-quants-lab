#!/bin/bash

# 安全合并 Upstream - 保留我们的所有修改
# 策略：获取 upstream 的新功能，但冲突时优先使用我们的代码

set -e

echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║         🔄 安全合并 Upstream（保留我们的所有修改）                            ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ============================================================================
# 步骤 1: 安全检查
# ============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📋 步骤 1/6: 安全检查${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 检查是否有未提交的更改
if [[ -n $(git status -s) ]]; then
    echo -e "${RED}❌ 错误：工作区有未提交的更改${NC}"
    echo ""
    echo "请先提交或暂存所有更改："
    echo "  git add ."
    echo "  git commit -m 'your message'"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ 工作区干净${NC}"
echo ""

# ============================================================================
# 步骤 2: 创建备份分支
# ============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📋 步骤 2/6: 创建备份分支${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

BACKUP_BRANCH="backup-before-merge-$(date +%Y%m%d-%H%M%S)"
git branch $BACKUP_BRANCH

echo -e "${GREEN}✓ 已创建备份分支: ${BACKUP_BRANCH}${NC}"
echo -e "${YELLOW}  如果合并出问题，可以回退：${NC}"
echo -e "${YELLOW}    git reset --hard ${BACKUP_BRANCH}${NC}"
echo ""

# ============================================================================
# 步骤 3: 显示合并预览
# ============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📋 步骤 3/6: 合并预览${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo "将要合并的 upstream commits:"
git log --oneline --no-decorate HEAD..upstream/main | head -10
echo ""

echo "预计会添加的新文件（不冲突）:"
echo "  • Binance Perpetual 支持"
echo "  • Market Feeds Manager"
echo "  • Gateway Data Source"
echo "  • Feature Storage"
echo "  • 新的研究笔记本"
echo ""

echo "预计会保留的你的文件（冲突时）:"
echo "  • 订单簿采集系统"
echo "  • NoOpTaskStorage"
echo "  • AWS 部署文档"
echo "  • Docker 配置"
echo "  • 所有你的脚本和文档"
echo ""

# ============================================================================
# 步骤 4: 用户确认
# ============================================================================
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}⚠️  确认合并${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "合并策略："
echo "  ✓ 添加 upstream 的新文件"
echo "  ✓ 冲突时保留你的版本"
echo "  ✓ 你的所有功能不受影响"
echo ""
read -p "确认开始合并？[y/N] " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ 已取消${NC}"
    git branch -D $BACKUP_BRANCH 2>/dev/null || true
    exit 1
fi

echo ""

# ============================================================================
# 步骤 5: 执行合并（保留我们的版本）
# ============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📋 步骤 5/6: 执行合并${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo "开始合并 upstream/main..."
echo ""

# 尝试合并
if git merge upstream/main --no-commit --no-ff; then
    echo -e "${GREEN}✓ 合并成功，没有冲突${NC}"
    MERGE_SUCCESS=true
else
    echo -e "${YELLOW}⚠️  检测到冲突，正在自动解决（保留我们的版本）...${NC}"
    echo ""
    MERGE_SUCCESS=false
    
    # 获取所有冲突的文件
    CONFLICTS=$(git diff --name-only --diff-filter=U)
    
    if [ -n "$CONFLICTS" ]; then
        echo "冲突文件列表："
        echo "$CONFLICTS" | while read file; do
            echo "  • $file"
        done
        echo ""
        
        echo "正在解决冲突（使用我们的版本）..."
        # 对所有冲突文件使用我们的版本
        echo "$CONFLICTS" | while read file; do
            if [ -f "$file" ]; then
                git checkout --ours "$file"
                git add "$file"
                echo -e "${GREEN}  ✓ 已保留我们的版本: $file${NC}"
            fi
        done
        echo ""
    fi
fi

# 检查是否还有未解决的冲突
REMAINING_CONFLICTS=$(git diff --name-only --diff-filter=U 2>/dev/null || echo "")
if [ -n "$REMAINING_CONFLICTS" ]; then
    echo -e "${RED}❌ 仍有未解决的冲突${NC}"
    echo ""
    echo "未解决的文件："
    echo "$REMAINING_CONFLICTS"
    echo ""
    echo "请手动解决这些冲突，然后运行："
    echo "  git add <file>"
    echo "  git commit"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ 所有冲突已解决${NC}"
echo ""

# ============================================================================
# 步骤 6: 完成合并
# ============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📋 步骤 6/6: 完成合并${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 提交合并
git commit -m "🔀 merge: 合并 upstream/main 保留本地修改

合并策略：
- 添加 upstream 的新功能（Binance Perpetual, Market Feeds 等）
- 冲突时保留本地版本（订单簿采集、NoOpTaskStorage 等）
- 保持所有本地功能完整

新增功能：
- Binance Perpetual 支持
- Market Feeds Manager
- Gateway Data Source (Meteora)
- Feature Storage
- 新的研究笔记本

保留功能：
- 订单簿采集系统
- CEX-DEX 套利分析
- NoOpTaskStorage
- AWS 部署配置
- Docker 配置
- 所有本地脚本和文档

备份分支: $BACKUP_BRANCH"

echo -e "${GREEN}✓ 合并已提交${NC}"
echo ""

# ============================================================================
# 完成总结
# ============================================================================
echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║                          ✅ 合并完成！                                         ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📊 合并结果："
echo ""

# 显示新增的文件（来自 upstream）
echo "新增文件（来自 upstream）:"
git diff --name-only --diff-filter=A $BACKUP_BRANCH HEAD | head -20 | while read file; do
    echo "  + $file"
done
echo ""

# 显示保留的文件（我们的版本）
echo "保留文件（我们的版本，覆盖了 upstream）:"
if [ "$MERGE_SUCCESS" = false ]; then
    echo "$CONFLICTS" | head -10 | while read file; do
        echo "  ✓ $file"
    done
else
    echo "  （没有冲突）"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 验证步骤"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "1. 检查你的核心功能是否完整："
echo "   ls app/tasks/data_collection/orderbook_snapshot_task.py"
echo "   ls config/orderbook_snapshot_gateio.yml"
echo "   ls docs/NO_MONGODB_MODE.md"
echo ""

echo "2. 检查新增的 upstream 功能："
echo "   ls core/data_sources/market_feeds/"
echo "   ls core/data_sources/gateway.py"
echo "   ls core/features/storage.py"
echo ""

echo "3. 运行测试确保系统正常："
echo "   python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 下一步"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "如果一切正常："
echo "  git push origin main"
echo ""

echo "如果发现问题，回退到合并前："
echo "  git reset --hard $BACKUP_BRANCH"
echo "  git branch -D $BACKUP_BRANCH  # 清理备份分支"
echo ""

echo "查看详细的合并变更："
echo "  git diff $BACKUP_BRANCH HEAD"
echo "  git log --oneline --graph -20"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}🎉 合并成功完成！你的所有功能已保留，同时获得了 upstream 的新功能。${NC}"
echo ""

