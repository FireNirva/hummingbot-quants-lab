#!/bin/bash
# AWS 服务器快速配置脚本
# 用途: 在新的 Ubuntu EC2 实例上一键配置订单簿采集环境
#
# 使用方法:
# 1. SSH 连接到 AWS EC2 实例
# 2. 上传此脚本: scp -i key.pem aws_setup.sh ubuntu@ip:~/
# 3. 运行: bash aws_setup.sh
#
# 注意: 此脚本假设你已经有 quants-lab.tar.gz 文件上传到服务器

set -e  # 遇到错误立即退出

echo "=========================================="
echo "🚀 AWS 订单簿采集系统配置脚本"
echo "=========================================="
echo ""

# 配置变量
PROJECT_DIR="$HOME/quants-lab"
CONDA_ENV="quants-lab"
PYTHON_VERSION="3.10"

# 检查是否为 root
if [ "$EUID" -eq 0 ]; then 
   echo "❌ 请不要使用 root 用户运行此脚本"
   echo "   使用普通用户 (ubuntu) 运行"
   exit 1
fi

# ========================================
# 阶段 1: 系统更新
# ========================================
echo "📦 阶段 1: 更新系统..."
sudo apt update
sudo apt upgrade -y
sudo apt install -y git htop curl wget vim tmux tree

echo "✅ 系统更新完成"
echo ""

# ========================================
# 阶段 2: 安装 Miniconda
# ========================================
echo "🐍 阶段 2: 安装 Miniconda..."

if [ -d "$HOME/miniconda3" ]; then
    echo "⚠️  Miniconda 已安装，跳过"
else
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
    bash /tmp/miniconda.sh -b -p $HOME/miniconda3
    rm /tmp/miniconda.sh
    
    # 添加到 PATH
    echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
    export PATH="$HOME/miniconda3/bin:$PATH"
    
    # 初始化
    $HOME/miniconda3/bin/conda init bash
    source ~/.bashrc
    
    echo "✅ Miniconda 安装完成"
fi

echo ""

# ========================================
# 阶段 3: 解压项目
# ========================================
echo "📂 阶段 3: 部署项目..."

if [ -f "$HOME/quants-lab.tar.gz" ]; then
    echo "📦 发现项目压缩包，正在解压..."
    
    # 备份旧版本（如果存在）
    if [ -d "$PROJECT_DIR" ]; then
        echo "⚠️  检测到旧版本，备份中..."
        mv "$PROJECT_DIR" "${PROJECT_DIR}.backup.$(date +%Y%m%d_%H%M%S)"
    fi
    
    # 解压
    tar xzf "$HOME/quants-lab.tar.gz"
    
    # 如果解压后是 quants-lab/ 目录，直接重命名
    if [ -d "$HOME/quants-lab" ]; then
        mv "$HOME/quants-lab" "$PROJECT_DIR" 2>/dev/null || true
    fi
    
    echo "✅ 项目解压完成"
else
    echo "⚠️  未找到 quants-lab.tar.gz"
    echo "   请先上传项目压缩包到 $HOME/"
    echo "   命令: scp -i key.pem quants-lab.tar.gz ubuntu@ip:~/"
    
    # 如果项目目录存在，继续执行
    if [ ! -d "$PROJECT_DIR" ]; then
        echo "❌ 项目目录不存在，退出"
        exit 1
    fi
fi

echo ""

# ========================================
# 阶段 4: 创建 Conda 环境
# ========================================
echo "🔧 阶段 4: 创建 Conda 环境..."

# 确保 conda 命令可用
eval "$($HOME/miniconda3/bin/conda shell.bash hook)"

if conda env list | grep -q "^${CONDA_ENV} "; then
    echo "⚠️  环境 ${CONDA_ENV} 已存在，跳过创建"
else
    conda create -n $CONDA_ENV python=$PYTHON_VERSION -y
    echo "✅ Conda 环境创建完成"
fi

echo ""

# ========================================
# 阶段 5: 安装 Python 依赖
# ========================================
echo "📚 阶段 5: 安装 Python 依赖..."

cd "$PROJECT_DIR"
source $HOME/miniconda3/bin/activate $CONDA_ENV

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Python 依赖安装完成"
else
    echo "⚠️  未找到 requirements.txt，跳过依赖安装"
fi

echo ""

# ========================================
# 阶段 6: 创建必要目录
# ========================================
echo "📁 阶段 6: 创建必要目录..."

mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/app/data/cache/orderbook_snapshots"
mkdir -p "$PROJECT_DIR/app/data/processed/plots"
mkdir -p "$PROJECT_DIR/app/data/processed/spread_analysis"

echo "✅ 目录创建完成"
echo ""

# ========================================
# 阶段 7: 测试采集
# ========================================
echo "🧪 阶段 7: 测试单次采集..."

cd "$PROJECT_DIR"
source $HOME/miniconda3/bin/activate $CONDA_ENV

echo "运行测试采集（24个交易对）..."
python cli.py trigger-task \
    --task orderbook_snapshot_gateio \
    --config config/orderbook_snapshot_gateio.yml

if [ $? -eq 0 ]; then
    echo "✅ 测试采集成功！"
else
    echo "⚠️  测试采集失败，请检查日志"
fi

echo ""

# ========================================
# 阶段 8: 创建 systemd 服务
# ========================================
echo "⚙️  阶段 8: 创建 systemd 服务..."

CONDA_PATH="$HOME/miniconda3/envs/$CONDA_ENV/bin"
SERVICE_FILE="/etc/systemd/system/orderbook-collector.service"

sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Orderbook Collector Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$CONDA_PATH:$HOME/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=$CONDA_PATH/python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
Restart=always
RestartSec=10
StandardOutput=append:$PROJECT_DIR/logs/orderbook_collection.log
StandardError=append:$PROJECT_DIR/logs/orderbook_collection.log

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Systemd 服务配置完成"
echo ""

# 重载并启动服务
echo "🚀 启动服务..."
sudo systemctl daemon-reload
sudo systemctl enable orderbook-collector
sudo systemctl start orderbook-collector

# 等待3秒检查状态
sleep 3
sudo systemctl status orderbook-collector --no-pager

echo ""

# ========================================
# 阶段 9: 配置 Cron 任务
# ========================================
echo "⏰ 阶段 9: 配置 Cron 任务..."

# 创建临时 cron 文件
CRON_FILE="/tmp/quants-cron"
cat > $CRON_FILE <<EOF
# 订单簿采集系统监控和维护
SHELL=/bin/bash
PATH=$CONDA_PATH:$HOME/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# 每5分钟检查健康状态
*/5 * * * * cd $PROJECT_DIR && python scripts/monitor_orderbook_collection.py >> logs/monitor.log 2>&1

# 每天凌晨2点清理超过7天的数据
0 2 * * * cd $PROJECT_DIR && python scripts/cleanup_old_orderbook_data.py --days 7 >> logs/cleanup.log 2>&1

# 每天凌晨3点检查磁盘空间
0 3 * * * df -h $PROJECT_DIR >> $PROJECT_DIR/logs/disk_usage.log 2>&1

# 每小时生成采集统计报告
0 * * * * cd $PROJECT_DIR && tail -1000 logs/orderbook_collection.log | grep "Stats:" | tail -1 >> logs/hourly_stats.log 2>&1
EOF

# 安装 cron 任务
crontab $CRON_FILE
rm $CRON_FILE

echo "✅ Cron 任务配置完成"
echo ""

# ========================================
# 阶段 10: 配置防火墙
# ========================================
echo "🔒 阶段 10: 配置防火墙..."

if ! command -v ufw &> /dev/null; then
    sudo apt install -y ufw
fi

# 允许 SSH 和 HTTPS
sudo ufw allow 22/tcp  > /dev/null 2>&1
sudo ufw allow 443/tcp > /dev/null 2>&1

# 启用防火墙（如果尚未启用）
echo "y" | sudo ufw enable > /dev/null 2>&1

sudo ufw status

echo "✅ 防火墙配置完成"
echo ""

# ========================================
# 完成
# ========================================
echo "=========================================="
echo "🎉 配置完成！"
echo "=========================================="
echo ""
echo "📊 系统状态:"
echo "   • 项目目录: $PROJECT_DIR"
echo "   • Conda 环境: $CONDA_ENV"
echo "   • 服务状态: $(sudo systemctl is-active orderbook-collector)"
echo ""
echo "🔧 常用命令:"
echo "   # 查看服务状态"
echo "   sudo systemctl status orderbook-collector"
echo ""
echo "   # 查看实时日志"
echo "   tail -f $PROJECT_DIR/logs/orderbook_collection.log"
echo ""
echo "   # 重启服务"
echo "   sudo systemctl restart orderbook-collector"
echo ""
echo "   # 健康检查"
echo "   cd $PROJECT_DIR && python scripts/monitor_orderbook_collection.py"
echo ""
echo "   # 查看磁盘使用"
echo "   du -sh $PROJECT_DIR/app/data/cache/orderbook_snapshots/"
echo ""
echo "📚 文档:"
echo "   cat $PROJECT_DIR/docs/AWS_DEPLOYMENT_GUIDE.md"
echo "   cat $PROJECT_DIR/docs/QUICKSTART_5S_ORDERBOOK.md"
echo ""
echo "🎯 下一步:"
echo "   1. 查看服务日志确认正常运行"
echo "   2. 配置 CloudWatch 监控和告警"
echo "   3. 设置 EBS 自动快照"
echo ""
echo "✅ AWS 部署完成！开始采集数据吧！🚀"
echo "=========================================="

