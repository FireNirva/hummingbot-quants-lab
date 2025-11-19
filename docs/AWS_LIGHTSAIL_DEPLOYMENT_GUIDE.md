# ☁️ AWS Lightsail 部署指南 - 订单簿数据采集系统

> **专为 AWS Lightsail 定制的完整部署指南**

---

## 🎯 **为什么选择 Lightsail？**

### **Lightsail vs EC2**

| 对比项 | Lightsail | EC2 | 推荐 |
|--------|-----------|-----|------|
| **价格** | 固定月费 | 按小时计费 | ✅ Lightsail 更便宜 |
| **简单性** | 一键部署 | 需配置复杂 | ✅ Lightsail 更简单 |
| **流量** | 包含流量 | 单独计费 | ✅ Lightsail 更划算 |
| **适用场景** | 小规模应用 | 大规模应用 | ✅ Lightsail 适合订单簿采集 |

**结论**: ✅ **订单簿采集项目选 Lightsail 更合适**

---

## 💰 **成本估算**

### **推荐配置**

```
Lightsail 套餐:  4 GB RAM / 2 vCPU / 80 GB SSD
价格:           $20/月 (约 ¥145/月)
流量:           包含 4 TB 传输流量
区域:           Singapore (ap-southeast-1)
```

### **月度成本明细**

| 项目 | 配置 | 月费 |
|------|------|------|
| **Lightsail 实例** | 4 GB RAM, 2 vCPU | $20/月 |
| **额外存储** | 无需（80 GB 够用）| $0 |
| **流量** | 包含 4 TB | $0 |
| **快照备份** | 每月1次（可选）| ~$2/月 |
| **合计** | - | **$20-22/月** |

**约 ¥145-160/月** - 性价比极高！

---

## 🚀 **快速部署（3 步完成）**

### **步骤 1: 创建 Lightsail 实例**

1. **登录 AWS Lightsail**
   - 访问: https://lightsail.aws.amazon.com/
   - 登录你的 AWS 账号

2. **创建实例**
   ```
   点击 "Create instance"
   ```

3. **选择配置**
   ```
   实例位置:    Asia Pacific (Singapore)
   平台:        Linux/Unix
   蓝图:        OS Only → Ubuntu 22.04 LTS
   实例套餐:    $20/月 (4 GB RAM, 2 vCPU, 80 GB SSD)
   实例名称:    quants-lab-orderbook
   ```

4. **配置 SSH 密钥**
   ```
   下载默认密钥对或上传自己的公钥
   保存密钥到本地（如 ~/.ssh/lightsail-quants-lab.pem）
   ```

5. **创建实例**
   ```
   点击 "Create instance"
   等待 3-5 分钟实例启动
   ```

---

### **步骤 2: 连接到实例并部署**

#### **2.1 SSH 连接**

**从本地终端连接：**

```bash
# 设置密钥权限
chmod 400 ~/.ssh/lightsail-quants-lab.pem

# 连接到实例（替换 YOUR-IP 为你的实例 IP）
ssh -i ~/.ssh/lightsail-quants-lab.pem ubuntu@YOUR-IP
```

**或使用 Lightsail 浏览器终端：**
- 在 Lightsail 控制台点击实例名称
- 点击 "Connect using SSH" 按钮

---

#### **2.2 一键部署脚本**

在 Lightsail 实例上运行：

```bash
# 下载并运行部署脚本
curl -sSL https://raw.githubusercontent.com/YOUR-USERNAME/quants-lab/main/scripts/aws_setup.sh | bash

# 或手动部署（推荐）
git clone https://github.com/YOUR-USERNAME/quants-lab.git
cd quants-lab
bash scripts/aws_setup.sh
```

**部署脚本会自动：**
- ✅ 安装 Miniconda
- ✅ 创建 Python 环境
- ✅ 安装项目依赖
- ✅ 配置环境变量
- ✅ 创建数据目录

---

#### **2.3 手动部署步骤（如果自动脚本失败）**

```bash
# 1. 更新系统
sudo apt update && sudo apt upgrade -y

# 2. 安装基础依赖
sudo apt install -y git wget curl build-essential

# 3. 安装 Miniconda
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
rm Miniconda3-latest-Linux-x86_64.sh

# 4. 初始化 Conda
eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
echo 'eval "$($HOME/miniconda3/bin/conda shell.bash hook)"' >> ~/.bashrc

# 5. 克隆项目
cd ~
git clone https://github.com/YOUR-USERNAME/quants-lab.git
cd quants-lab

# 6. 创建 Conda 环境
conda env create -f environment.yml
conda activate quants-lab

# 7. 安装项目
pip install -e .

# 8. 创建数据目录
mkdir -p app/data/raw/orderbook_snapshots
mkdir -p logs

# 9. 验证安装
python cli.py --help
```

---

### **步骤 3: 启动订单簿采集**

#### **3.1 配置订单簿采集**

检查配置文件：

```bash
cd ~/quants-lab

# 查看 Gate.io 配置
cat config/orderbook_snapshot_gateio.yml

# 查看 MEXC 配置（如果需要）
cat config/orderbook_snapshot_mexc.yml
```

**配置内容示例：**
```yaml
tasks:
  orderbook_snapshot_gateio:
    enabled: true
    schedule:
      type: frequency
      frequency_hours: 0.001389  # 5 秒
    config:
      connector_name: "gate_io"
      trading_pairs:
        - "VIRTUAL-USDT"
        - "LMTS-USDT"
        - "BNKR-USDT"
        - "PRO-USDT"
        - "IRON-USDT"
        - "MIGGLES-USDT"
      depth_limit: 100
```

---

#### **3.2 启动采集任务**

**方法 1: 使用 screen（推荐）**

```bash
cd ~/quants-lab
conda activate quants-lab

# 创建一个后台会话
screen -S orderbook

# 在 screen 中启动采集
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml

# 按 Ctrl+A 然后 D 退出 screen（任务继续运行）
```

**恢复 screen 会话：**
```bash
screen -r orderbook
```

---

**方法 2: 使用 nohup**

```bash
cd ~/quants-lab
conda activate quants-lab

# 后台运行并记录日志
nohup python cli.py run-tasks \
  --config config/orderbook_snapshot_gateio.yml \
  > logs/orderbook_gateio.log 2>&1 &

# 记录进程 ID
echo $! > logs/orderbook_gateio.pid

# 查看日志
tail -f logs/orderbook_gateio.log
```

---

**方法 3: 使用 systemd 服务（最稳定）**

创建服务文件：

```bash
sudo tee /etc/systemd/system/orderbook-gateio.service > /dev/null <<EOF
[Unit]
Description=QuantsLab Order Book Collection - Gate.io
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/quants-lab
Environment="PATH=/home/ubuntu/miniconda3/envs/quants-lab/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/ubuntu/miniconda3/envs/quants-lab/bin/python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
Restart=always
RestartSec=10
StandardOutput=append:/home/ubuntu/quants-lab/logs/orderbook_gateio.log
StandardError=append:/home/ubuntu/quants-lab/logs/orderbook_gateio_error.log

[Install]
WantedBy=multi-user.target
EOF

# 重载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start orderbook-gateio

# 设置开机自启
sudo systemctl enable orderbook-gateio

# 查看状态
sudo systemctl status orderbook-gateio

# 查看日志
sudo journalctl -u orderbook-gateio -f
```

---

#### **3.3 验证采集是否正常**

**检查实时状态：**

```bash
cd ~/quants-lab
conda activate quants-lab

# 运行实时监控
python scripts/check_realtime_orderbook.py
```

**预期输出：**
```
📊 实时订单簿采集状态

交易对: VIRTUAL-USDT
   • 最新采集: 2025-11-17 10:23:45 UTC
   • 平均间隔: 5.01 秒
   • Update ID 范围: 1234567890 → 1234568123
   • 最新买1价: $0.1234
   • 最新卖1价: $0.1235

交易对: LMTS-USDT
   • 最新采集: 2025-11-17 10:23:50 UTC
   • 平均间隔: 5.02 秒
   ...
```

---

**检查数据文件：**

```bash
# 查看数据目录
ls -lh app/data/raw/orderbook_snapshots/

# 预期输出（每天一个文件）
# gate_io_VIRTUAL-USDT_20251117.parquet
# gate_io_LMTS-USDT_20251117.parquet
# gate_io_BNKR-USDT_20251117.parquet
# ...

# 查看文件大小和数量
du -sh app/data/raw/orderbook_snapshots/
```

---

**使用监控脚本：**

```bash
# 流动性分析
python scripts/monitor_orderbook_liquidity.py

# 数据质量检查
python scripts/check_orderbook_data.py
```

---

## 📊 **数据监控**

### **监控方案 1: 定时检查（cron）**

创建监控脚本：

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每小时检查一次）
0 * * * * cd /home/ubuntu/quants-lab && /home/ubuntu/miniconda3/envs/quants-lab/bin/python scripts/check_realtime_orderbook.py >> logs/monitoring.log 2>&1

# 每天凌晨 2 点清理超过 7 天的数据
0 2 * * * cd /home/ubuntu/quants-lab && /home/ubuntu/miniconda3/envs/quants-lab/bin/python scripts/cleanup_old_orderbook_data.py --days 7 >> logs/cleanup.log 2>&1
```

---

### **监控方案 2: 实时监控脚本**

创建一个持续监控脚本：

```bash
# 创建 monitoring.sh
cat > ~/quants-lab/scripts/continuous_monitoring.sh << 'EOF'
#!/bin/bash

cd ~/quants-lab
source ~/miniconda3/etc/profile.d/conda.sh
conda activate quants-lab

while true; do
    echo "============================================"
    echo "📊 $(date '+%Y-%m-%d %H:%M:%S')"
    echo "============================================"
    
    # 检查订单簿采集状态
    python scripts/check_realtime_orderbook.py
    
    # 检查磁盘空间
    echo ""
    echo "💾 磁盘使用情况:"
    df -h /home/ubuntu/quants-lab/app/data/raw/orderbook_snapshots/
    
    # 检查进程
    echo ""
    echo "🔄 采集进程状态:"
    ps aux | grep "cli.py run-tasks" | grep -v grep || echo "❌ 采集进程未运行"
    
    echo ""
    sleep 300  # 每 5 分钟检查一次
done
EOF

chmod +x ~/quants-lab/scripts/continuous_monitoring.sh

# 在 screen 中运行监控
screen -dmS monitoring bash -c "cd ~/quants-lab && ./scripts/continuous_monitoring.sh"

# 查看监控输出
screen -r monitoring
```

---

### **监控方案 3: CloudWatch（高级）**

在 Lightsail 控制台：

1. 进入实例页面
2. 点击 "Metrics" 标签
3. 查看：
   - CPU 使用率
   - 网络传输
   - 磁盘 I/O

设置告警：
1. 点击 "Alarms" 标签
2. 创建告警：
   - CPU > 80%
   - 磁盘空间 < 10 GB
3. 配置通知（邮件）

---

## 🔧 **任务管理命令**

### **查看运行状态**

```bash
# 方法 1: systemd
sudo systemctl status orderbook-gateio

# 方法 2: 进程查看
ps aux | grep "cli.py run-tasks"

# 方法 3: screen 列表
screen -ls
```

---

### **停止采集**

```bash
# 方法 1: systemd
sudo systemctl stop orderbook-gateio

# 方法 2: 使用 stop 脚本
cd ~/quants-lab
bash scripts/stop_all_orderbook.sh

# 方法 3: 手动 kill
ps aux | grep "cli.py run-tasks" | grep -v grep | awk '{print $2}' | xargs kill
```

---

### **重启采集**

```bash
# 方法 1: systemd
sudo systemctl restart orderbook-gateio

# 方法 2: 使用重启脚本
cd ~/quants-lab
bash scripts/restart_orderbook_gateio.sh
```

---

### **查看日志**

```bash
# systemd 日志
sudo journalctl -u orderbook-gateio -f

# 应用日志
tail -f ~/quants-lab/logs/orderbook_gateio.log

# 错误日志
tail -f ~/quants-lab/logs/orderbook_gateio_error.log
```

---

## 📦 **数据导出和备份**

### **导出到本地**

```bash
# 从本地机器运行（替换 YOUR-IP）
scp -i ~/.ssh/lightsail-quants-lab.pem -r \
  ubuntu@YOUR-IP:/home/ubuntu/quants-lab/app/data/raw/orderbook_snapshots/ \
  ./local_backup/
```

---

### **创建 Lightsail 快照（推荐）**

1. 在 Lightsail 控制台进入实例页面
2. 点击 "Snapshots" 标签
3. 点击 "Create snapshot"
4. 命名快照（如 `quants-lab-20251117`）
5. 等待快照完成（约 5-10 分钟）

**快照用途：**
- ✅ 数据备份
- ✅ 快速恢复
- ✅ 迁移到新实例

**成本：** 约 $2-3/月（80 GB 快照）

---

### **自动备份脚本**

```bash
# 创建备份脚本
cat > ~/quants-lab/scripts/backup_to_s3.sh << 'EOF'
#!/bin/bash

# 配置
BACKUP_DIR="/home/ubuntu/quants-lab/app/data/raw/orderbook_snapshots"
S3_BUCKET="s3://your-bucket-name/orderbook-backups/"
DATE=$(date +%Y%m%d)

# 打包
tar -czf /tmp/orderbook_backup_${DATE}.tar.gz -C $BACKUP_DIR .

# 上传到 S3（需要配置 AWS CLI）
aws s3 cp /tmp/orderbook_backup_${DATE}.tar.gz $S3_BUCKET

# 清理
rm /tmp/orderbook_backup_${DATE}.tar.gz

echo "✅ 备份完成: orderbook_backup_${DATE}.tar.gz"
EOF

chmod +x ~/quants-lab/scripts/backup_to_s3.sh

# 添加到 crontab（每周日凌晨备份）
# 0 3 * * 0 /home/ubuntu/quants-lab/scripts/backup_to_s3.sh >> /home/ubuntu/quants-lab/logs/backup.log 2>&1
```

---

## 🔍 **套利价差分析**

### **在 AWS 上运行价差分析**

```bash
cd ~/quants-lab
conda activate quants-lab

# 下载 CEX 数据（7 天，1 分钟）
python scripts/import_freqtrade_data.py \
  --config config/gateio_USDT_downloader_full.yml \
  --days 7

# 下载 DEX 数据
python scripts/build_pool_mapping.py --connector gate_io --network base
python scripts/download_dex_ohlcv.py --network base --days 3

# 分析价差
python scripts/analyze_cex_dex_spread.py --compare-all

# 查看结果
cat app/data/processed/spread_analysis/*.csv
```

---

### **使用订单簿数据计算最优交易规模**

```bash
# 单个交易对
python scripts/calculate_optimal_trade_size.py VIRTUAL-USDT 1.5 --connector gate_io

# 批量优化
python scripts/batch_optimize_trade_size.py \
  --config config/gateio_USDT_downloader_full.yml
```

---

## 🚨 **故障排除**

### **问题 1: 采集进程停止**

**检查：**
```bash
sudo systemctl status orderbook-gateio
```

**解决：**
```bash
sudo systemctl restart orderbook-gateio
```

---

### **问题 2: 磁盘空间不足**

**检查：**
```bash
df -h
du -sh ~/quants-lab/app/data/raw/orderbook_snapshots/
```

**解决：**
```bash
# 清理旧数据
python scripts/cleanup_old_orderbook_data.py --days 7

# 或手动删除
rm ~/quants-lab/app/data/raw/orderbook_snapshots/gate_io_*_20251101.parquet
```

---

### **问题 3: API 限流**

**检查：**
```bash
tail -100 ~/quants-lab/logs/orderbook_gateio.log | grep "429"
```

**解决：**
- 降低采集频率（改为 10 秒）
- 减少交易对数量
- 确认 API 限流设置（Semaphore=8）

---

### **问题 4: 网络连接问题**

**检查：**
```bash
ping -c 5 api.gateio.ws
curl -I https://api.gateio.ws/api/v4/spot/order_book?currency_pair=BTC_USDT
```

**解决：**
- 检查 Lightsail 防火墙
- 确认出站流量未被限制

---

## 📋 **快速命令参考**

### **连接实例**
```bash
ssh -i ~/.ssh/lightsail-quants-lab.pem ubuntu@YOUR-IP
```

### **激活环境**
```bash
cd ~/quants-lab
conda activate quants-lab
```

### **查看采集状态**
```bash
python scripts/check_realtime_orderbook.py
```

### **启动采集**
```bash
sudo systemctl start orderbook-gateio
```

### **停止采集**
```bash
sudo systemctl stop orderbook-gateio
```

### **查看日志**
```bash
sudo journalctl -u orderbook-gateio -f
```

### **清理数据**
```bash
python scripts/cleanup_old_orderbook_data.py --days 7
```

---

## 💡 **最佳实践**

1. ✅ **使用 systemd 管理服务**（最稳定）
2. ✅ **设置自动重启**（Restart=always）
3. ✅ **定期清理数据**（cron 定时任务）
4. ✅ **监控磁盘空间**（每天检查）
5. ✅ **定期备份**（每周快照）
6. ✅ **监控采集状态**（每小时检查）
7. ✅ **使用 screen/tmux**（方便管理）

---

## 📞 **需要帮助？**

- 📚 完整文档：`docs/INDEX.md`
- 🛠️ 脚本索引：`scripts/README.md`
- 📖 订单簿采集：`docs/ORDERBOOK_COLLECTION_GUIDE.md`
- ☁️ AWS 部署：`docs/AWS_DEPLOYMENT_GUIDE.md`

---

**部署完成！开始收集订单簿数据吧！** 🚀📊

