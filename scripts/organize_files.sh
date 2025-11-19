#!/bin/bash

# 项目文件整理脚本 - 2024-11-19
# 功能：将根目录的文档和脚本移动到对应文件夹

set -e

echo "🗂️  开始整理项目文件..."
echo "=" | tr -d '\n' | while read -r; do printf '=%.0s' {1..80}; done
echo ""

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 统计
moved_docs=0
moved_scripts=0
deleted_files=0

echo ""
echo "📄 移动文档到 docs/ 目录..."
echo "─────────────────────────────────────────────────────────────────"

# 移动 .md 文档
if [ -f "AWS_LIGHTSAIL_QUICKSTART.md" ]; then
    mv AWS_LIGHTSAIL_QUICKSTART.md docs/
    echo "  ✓ AWS_LIGHTSAIL_QUICKSTART.md → docs/"
    ((moved_docs++))
fi

if [ -f "LIGHTSAIL_SETUP_GUIDE.md" ]; then
    mv LIGHTSAIL_SETUP_GUIDE.md docs/
    echo "  ✓ LIGHTSAIL_SETUP_GUIDE.md → docs/"
    ((moved_docs++))
fi

# git_commit_plan.md 是临时文件，移到 docs/archive/ 或删除
if [ -f "git_commit_plan.md" ]; then
    mkdir -p docs/archive
    mv git_commit_plan.md docs/archive/
    echo "  ✓ git_commit_plan.md → docs/archive/ (临时文件)"
    ((moved_docs++))
fi

echo ""
echo "🔧 移动脚本到 scripts/ 目录..."
echo "─────────────────────────────────────────────────────────────────"

# 移动测试脚本
if [ -f "test_mongo_connection.py" ]; then
    mv test_mongo_connection.py scripts/
    echo "  ✓ test_mongo_connection.py → scripts/"
    ((moved_scripts++))
fi

# git_upload_all.sh 是临时脚本，移到 scripts/archive/ 或删除
if [ -f "git_upload_all.sh" ]; then
    mkdir -p scripts/archive
    mv git_upload_all.sh scripts/archive/
    echo "  ✓ git_upload_all.sh → scripts/archive/ (临时文件)"
    ((moved_scripts++))
fi

echo ""
echo "🗑️  清理临时文件..."
echo "─────────────────────────────────────────────────────────────────"

# 移动日志文件
if [ -f "build.log" ]; then
    mkdir -p logs
    mv build.log logs/
    echo "  ✓ build.log → logs/"
    ((deleted_files++))
fi

# 检查其他可能的临时文件
temp_files=(
    "*.log"
    "*.tmp"
    ".DS_Store"
    "*.pyc"
    "__pycache__"
)

for pattern in "${temp_files[@]}"; do
    # 只检查根目录
    if ls $pattern 2>/dev/null | grep -v "^logs/" | head -1 > /dev/null; then
        echo "  ⚠️  发现临时文件: $pattern (未自动删除，请手动检查)"
    fi
done

echo ""
echo "=" | tr -d '\n' | while read -r; do printf '=%.0s' {1..80}; done
echo ""
echo "✅ 文件整理完成！"
echo ""
echo "📊 整理统计:"
echo "  • 移动文档: $moved_docs 个"
echo "  • 移动脚本: $moved_scripts 个"
echo "  • 整理日志: $deleted_files 个"
echo ""

# 显示当前根目录的文档和脚本
echo "📁 根目录剩余的文档/脚本文件:"
echo "─────────────────────────────────────────────────────────────────"

remaining_docs=$(find . -maxdepth 1 -name "*.md" -type f | wc -l | tr -d ' ')
remaining_scripts=$(find . -maxdepth 1 \( -name "*.py" -o -name "*.sh" \) -type f ! -name "cli.py" ! -name "list_connectors.py" ! -name "install.sh" ! -name "uninstall.sh" | wc -l | tr -d ' ')

if [ "$remaining_docs" -eq 0 ] && [ "$remaining_scripts" -eq 0 ]; then
    echo "  ✓ 无剩余文件 - 根目录已清理干净！"
else
    if [ "$remaining_docs" -gt 0 ]; then
        echo ""
        echo "  📄 Markdown 文档:"
        find . -maxdepth 1 -name "*.md" -type f -exec basename {} \;
    fi
    
    if [ "$remaining_scripts" -gt 0 ]; then
        echo ""
        echo "  🔧 Python/Shell 脚本 (排除核心脚本):"
        find . -maxdepth 1 \( -name "*.py" -o -name "*.sh" \) -type f ! -name "cli.py" ! -name "list_connectors.py" ! -name "install.sh" ! -name "uninstall.sh" -exec basename {} \;
    fi
fi

echo ""
echo "=" | tr -d '\n' | while read -r; do printf '=%.0s' {1..80}; done
echo ""
echo "💡 提示:"
echo "  • README.md 保留在根目录（项目说明）"
echo "  • cli.py 保留在根目录（主入口）"
echo "  • install.sh/uninstall.sh 保留在根目录（安装脚本）"
echo "  • list_connectors.py 保留在根目录（工具脚本）"
echo ""
echo "🎯 下一步:"
echo "  1. 检查 docs/archive/ 和 scripts/archive/ 中的文件"
echo "  2. 确认不需要的文件可以删除"
echo "  3. 运行: git status 查看变化"
echo "  4. 运行: git add . && git commit -m '🗂️ 整理项目文件结构'"
echo ""

