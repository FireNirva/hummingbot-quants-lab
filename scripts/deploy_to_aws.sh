#!/bin/bash
# 本地打包并部署到 AWS 脚本
# 用途: 从本地 Mac 打包项目并上传到 AWS EC2
#
# 使用方法:
# 1. 配置下方的变量（AWS_IP, KEY_FILE）
# 2. 运行: bash scripts/deploy_to_aws.sh
#
# 此脚本会：
# - 打包项目（排除大文件和缓存）
# - 上传到 AWS
# - 在 AWS 上运行配置脚本

set -e

echo "=========================================="
echo "📦 AWS 部署脚本 - 本地打包上传"
echo "=========================================="
echo ""

# ========================================
# 配置变量（请修改）
# ========================================

# AWS EC2 信息
AWS_IP="3.1.123.45"           # 替换为你的 AWS 弹性 IP
KEY_FILE="$HOME/Downloads/orderbook-key.pem"  # 替换为你的密钥文件路径
AWS_USER="ubuntu"             # EC2 用户名（Ubuntu AMI 默认为 ubuntu）

# 项目路径
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_NAME="quants-lab"

# 临时文件
TAR_FILE="/tmp/${PROJECT_NAME}.tar.gz"

echo "📋 配置信息:"
echo "   • 项目目录: $PROJECT_DIR"
echo "   • AWS IP: $AWS_IP"
echo "   • 密钥文件: $KEY_FILE"
echo "   • 用户名: $AWS_USER"
echo ""

# ========================================
# 检查配置
# ========================================

# 检查密钥文件
if [ ! -f "$KEY_FILE" ]; then
    echo "❌ 密钥文件不存在: $KEY_FILE"
    echo "   请修改脚本中的 KEY_FILE 变量"
    exit 1
fi

# 检查密钥权限
KEY_PERMS=$(stat -f "%A" "$KEY_FILE" 2>/dev/null || stat -c "%a" "$KEY_FILE" 2>/dev/null)
if [ "$KEY_PERMS" != "400" ] && [ "$KEY_PERMS" != "600" ]; then
    echo "⚠️  修正密钥文件权限..."
    chmod 400 "$KEY_FILE"
fi

# 测试 SSH 连接
echo "🔌 测试 SSH 连接..."
if ssh -i "$KEY_FILE" -o ConnectTimeout=5 -o StrictHostKeyChecking=no "$AWS_USER@$AWS_IP" "echo '✅ SSH 连接成功'" 2>/dev/null; then
    echo ""
else
    echo "❌ SSH 连接失败"
    echo "   请检查："
    echo "   1. AWS_IP 是否正确"
    echo "   2. KEY_FILE 路径是否正确"
    echo "   3. EC2 实例是否运行中"
    echo "   4. 安全组是否允许 SSH (22)"
    exit 1
fi

# ========================================
# 阶段 1: 打包项目
# ========================================

echo "📦 阶段 1: 打包项目..."
cd "$PROJECT_DIR"

# 删除旧的压缩包
rm -f "$TAR_FILE"

# 打包（排除不必要的文件）
echo "   压缩中（这可能需要几分钟）..."
tar czf "$TAR_FILE" \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='.DS_Store' \
    --exclude='app/data/cache/orderbook_snapshots/*' \
    --exclude='app/data/cache/candles/*' \
    --exclude='app/data/processed/*' \
    --exclude='*.egg-info' \
    --exclude='.pytest_cache' \
    --exclude='user_data/*' \
    --exclude='logs/*.log' \
    .

# 获取压缩包大小
TAR_SIZE=$(du -h "$TAR_FILE" | cut -f1)
echo "✅ 打包完成: $TAR_SIZE"
echo ""

# ========================================
# 阶段 2: 上传到 AWS
# ========================================

echo "📤 阶段 2: 上传到 AWS..."
echo "   上传中（这可能需要几分钟）..."

scp -i "$KEY_FILE" \
    -o StrictHostKeyChecking=no \
    "$TAR_FILE" \
    "$AWS_USER@$AWS_IP:~/${PROJECT_NAME}.tar.gz"

echo "✅ 上传完成"
echo ""

# ========================================
# 阶段 3: 上传配置脚本
# ========================================

echo "📤 阶段 3: 上传配置脚本..."

scp -i "$KEY_FILE" \
    -o StrictHostKeyChecking=no \
    "$PROJECT_DIR/scripts/aws_setup.sh" \
    "$AWS_USER@$AWS_IP:~/aws_setup.sh"

echo "✅ 配置脚本上传完成"
echo ""

# ========================================
# 阶段 4: 在 AWS 上运行配置
# ========================================

echo "🚀 阶段 4: 运行 AWS 配置脚本..."
echo "   （这可能需要 5-10 分钟，请耐心等待）"
echo ""

ssh -i "$KEY_FILE" \
    -o StrictHostKeyChecking=no \
    "$AWS_USER@$AWS_IP" \
    "bash ~/aws_setup.sh"

echo ""
echo "=========================================="
echo "🎉 部署完成！"
echo "=========================================="
echo ""
echo "📊 下一步:"
echo ""
echo "   1️⃣  SSH 登录到服务器"
echo "   ssh -i $KEY_FILE $AWS_USER@$AWS_IP"
echo ""
echo "   2️⃣  查看服务状态"
echo "   sudo systemctl status orderbook-collector"
echo ""
echo "   3️⃣  查看实时日志"
echo "   tail -f ~/quants-lab/logs/orderbook_collection.log"
echo ""
echo "   4️⃣  运行健康检查"
echo "   cd ~/quants-lab && python scripts/monitor_orderbook_collection.py"
echo ""
echo "   5️⃣  查看数据"
echo "   ls -lh ~/quants-lab/app/data/cache/orderbook_snapshots/ | head -20"
echo ""
echo "📚 完整文档:"
echo "   ssh -i $KEY_FILE $AWS_USER@$AWS_IP 'cat ~/quants-lab/docs/AWS_DEPLOYMENT_GUIDE.md'"
echo ""
echo "=========================================="
echo "✅ 所有操作完成！订单簿采集已在 AWS 上运行！🚀"
echo "=========================================="

