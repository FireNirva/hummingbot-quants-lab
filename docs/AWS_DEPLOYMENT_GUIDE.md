# ☁️ AWS 部署指南 - 订单簿高频采集系统

> **推荐方案**: 将 5 秒高频订单簿采集系统部署到 AWS 云端

---

## 🎯 为什么选择 AWS 部署？

### **相比本地部署的优势**

| 对比项 | 本地部署 | AWS 部署 | 优势 |
|--------|---------|---------|------|
| **网络稳定性** | 依赖家庭网络 | 企业级网络 | ✅ AWS 更稳定 |
| **运行时间** | 电脑需开机 | 24/7 运行 | ✅ AWS 持续运行 |
| **存储空间** | 有限（本地硬盘） | 弹性扩展 | ✅ AWS 按需扩展 |
| **延迟** | 取决于位置 | 可选最优区域 | ✅ AWS 更低延迟 |
| **监控告警** | 需自建 | CloudWatch | ✅ AWS 开箱即用 |
| **成本** | 电费 + 硬件损耗 | 按需付费 | ⚖️ 长期看 AWS 更优 |
| **维护** | 需手动管理 | 自动化管理 | ✅ AWS 更省心 |

**结论**: ✅ **AWS 部署是更优选择**

---

## 💰 成本估算

### **推荐配置**

```
EC2 实例:    t3.medium (2 vCPU, 4GB RAM)
EBS 存储:    500 GB gp3 (通用型 SSD)
区域:        ap-southeast-1 (新加坡) 或 ap-northeast-1 (东京)
运行时间:    24/7
```

### **月度成本**

| 服务 | 配置 | 月费（美元） | 说明 |
|------|------|------------|------|
| **EC2 实例** | t3.medium | ~$30 | 2 vCPU, 4GB RAM |
| **EBS 存储** | 500 GB gp3 | ~$40 | 通用型 SSD |
| **数据传输** | 入站免费，出站 | ~$5-10 | 少量数据导出 |
| **CloudWatch** | 基础监控 | 免费 | 基础指标 |
| **合计** | - | **~$75-80/月** | 约 ¥550/月 |

**对比**：
- **本地运行**: 电费 ~¥50/月 + 硬件损耗 + 不稳定
- **AWS 运行**: ¥550/月 + 稳定 + 专业

**如果预算有限**：
- 使用 **t3.small** (1 vCPU, 2GB RAM): ~$15/月，但性能会受限
- 使用 **300 GB 存储** + 定期清理: 节省 ~$16/月

---

## 🏗️ 推荐架构

```
┌─────────────────────────────────────────────────────────┐
│                    AWS 云端架构                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │   EC2 Instance (t3.medium)                       │  │
│  │   OS: Amazon Linux 2 或 Ubuntu 22.04             │  │
│  │                                                  │  │
│  │   ┌──────────────────────────────────────────┐  │  │
│  │   │  Conda 环境                               │  │
│  │   │  • quants-lab (Python 3.10)               │  │
│  │   │  • 订单簿采集任务                          │  │
│  │   │  • 监控脚本 (cron)                        │  │
│  │   │  • 清理脚本 (cron)                        │  │
│  │   └──────────────────────────────────────────┘  │  │
│  │                                                  │  │
│  │   ┌──────────────────────────────────────────┐  │  │
│  │   │  EBS Volume (500 GB gp3)                  │  │
│  │   │  /home/ubuntu/quants-lab/                 │  │
│  │   │  └── app/data/cache/orderbook_snapshots/  │  │
│  │   └──────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
│                        │                                │
│                        │ 公网 IP (弹性 IP)                │
│                        ↓                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │   Gate.io API                                    │  │
│  │   api.gateio.ws                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │   CloudWatch (监控告警)                          │  │
│  │   • CPU 使用率                                    │  │
│  │   • 磁盘使用率                                    │  │
│  │   • 网络流量                                      │  │
│  │   • 自定义指标（采集成功率）                       │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │   SNS (告警通知)                                 │  │
│  │   • 邮件通知                                      │  │
│  │   • 短信通知（可选）                              │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 部署步骤（详细）

### **阶段 1: 创建 EC2 实例**

#### **1.1 登录 AWS 控制台**

```
https://console.aws.amazon.com/
```

#### **1.2 创建 EC2 实例**

```
服务 → EC2 → 启动实例
```

**配置选项**：

| 配置项 | 推荐值 | 说明 |
|--------|--------|------|
| **名称** | `orderbook-collector` | 易识别 |
| **AMI** | Ubuntu Server 22.04 LTS | 稳定，兼容性好 |
| **实例类型** | t3.medium | 2 vCPU, 4GB RAM |
| **密钥对** | 新建或选择现有 | 用于 SSH 登录 |
| **网络设置** | 默认 VPC | 允许 SSH (22), HTTPS (443) |
| **存储** | 500 GB gp3 SSD | 足够存储 2 个月数据 |

**安全组规则**：

```yaml
入站规则:
  - 类型: SSH
    协议: TCP
    端口: 22
    源: 你的 IP 地址 (或 0.0.0.0/0，但不安全)
    
  - 类型: HTTPS
    协议: TCP
    端口: 443
    源: 0.0.0.0/0
    描述: Gate.io API 访问

出站规则:
  - 类型: 所有流量
    协议: 全部
    端口: 全部
    目标: 0.0.0.0/0
```

**点击"启动实例"**

#### **1.3 分配弹性 IP（推荐）**

```
EC2 → 网络与安全 → 弹性 IP → 分配弹性 IP 地址
→ 关联到刚创建的实例
```

**优势**: IP 地址固定，重启不会变化

---

### **阶段 2: 连接并配置服务器**

#### **2.1 SSH 连接**

```bash
# 从本地终端连接
ssh -i /path/to/your-key.pem ubuntu@<弹性IP地址>

# 例如
ssh -i ~/Downloads/orderbook-key.pem ubuntu@3.1.123.45
```

#### **2.2 更新系统**

```bash
sudo apt update
sudo apt upgrade -y
```

#### **2.3 安装依赖**

```bash
# 安装基础工具
sudo apt install -y git htop curl wget vim tmux

# 安装 Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 验证安装
conda --version
```

---

### **阶段 3: 部署应用**

#### **3.1 克隆项目**

**方案 A: 从 GitHub（如果你的项目已上传）**

```bash
cd ~
git clone https://github.com/your-username/quants-lab.git
cd quants-lab
```

**方案 B: 从本地上传（推荐）**

```bash
# 在本地终端运行（不是 SSH）
cd /Users/alice/Dropbox/投资/量化交易/quants-lab
tar czf quants-lab.tar.gz \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='app/data/cache/orderbook_snapshots/*' \
    .

# 上传到 AWS
scp -i ~/Downloads/orderbook-key.pem \
    quants-lab.tar.gz \
    ubuntu@3.1.123.45:~/

# 在 AWS 上解压
# （切换回 SSH 终端）
tar xzf quants-lab.tar.gz
mv quants-lab ~/quants-lab
cd ~/quants-lab
```

#### **3.2 创建 Conda 环境**

```bash
cd ~/quants-lab

# 创建环境
conda create -n quants-lab python=3.10 -y
conda activate quants-lab

# 安装依赖
pip install -r requirements.txt

# 验证
python -c "import pandas; print('✅ 环境配置成功')"
```

#### **3.3 创建必要目录**

```bash
mkdir -p ~/quants-lab/logs
mkdir -p ~/quants-lab/app/data/cache/orderbook_snapshots
```

---

### **阶段 4: 配置自动启动**

#### **4.1 测试单次采集**

```bash
cd ~/quants-lab
conda activate quants-lab

python cli.py trigger-task \
    --task orderbook_snapshot_gateio \
    --config config/orderbook_snapshot_gateio.yml
```

**预期输出**: 24 个交易对全部采集成功

#### **4.2 创建 systemd 服务（推荐）**

创建服务文件：

```bash
sudo nano /etc/systemd/system/orderbook-collector.service
```

**文件内容**：

```ini
[Unit]
Description=Orderbook Collector Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/quants-lab
Environment="PATH=/home/ubuntu/miniconda3/envs/quants-lab/bin:/home/ubuntu/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/home/ubuntu/miniconda3/envs/quants-lab/bin/python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
Restart=always
RestartSec=10
StandardOutput=append:/home/ubuntu/quants-lab/logs/orderbook_collection.log
StandardError=append:/home/ubuntu/quants-lab/logs/orderbook_collection.log

[Install]
WantedBy=multi-user.target
```

**启动服务**：

```bash
# 重载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start orderbook-collector

# 设置开机自启
sudo systemctl enable orderbook-collector

# 检查状态
sudo systemctl status orderbook-collector

# 查看日志
tail -f ~/quants-lab/logs/orderbook_collection.log
```

**管理命令**：

```bash
# 停止服务
sudo systemctl stop orderbook-collector

# 重启服务
sudo systemctl restart orderbook-collector

# 查看服务日志
sudo journalctl -u orderbook-collector -f
```

---

### **阶段 5: 配置监控和告警**

#### **5.1 设置 Cron 任务**

```bash
crontab -e
```

**添加以下任务**：

```cron
# 订单簿采集系统监控和维护

# 环境变量
SHELL=/bin/bash
PATH=/home/ubuntu/miniconda3/envs/quants-lab/bin:/home/ubuntu/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# 每5分钟检查健康状态
*/5 * * * * cd /home/ubuntu/quants-lab && python scripts/monitor_orderbook_collection.py >> logs/monitor.log 2>&1

# 每天凌晨2点清理超过7天的数据
0 2 * * * cd /home/ubuntu/quants-lab && python scripts/cleanup_old_orderbook_data.py --days 7 >> logs/cleanup.log 2>&1

# 每天凌晨3点检查磁盘空间
0 3 * * * df -h /home/ubuntu/quants-lab >> logs/disk_usage.log 2>&1

# 每小时生成采集统计报告
0 * * * * cd /home/ubuntu/quants-lab && tail -1000 logs/orderbook_collection.log | grep "Stats:" | tail -1 >> logs/hourly_stats.log 2>&1
```

**验证 cron 任务**：

```bash
# 列出当前 cron 任务
crontab -l

# 查看 cron 日志
tail -f logs/monitor.log
```

#### **5.2 配置 CloudWatch 监控（可选但推荐）**

**安装 CloudWatch Agent**：

```bash
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb
```

**配置自定义指标**：

创建配置文件 `cloudwatch-config.json`:

```json
{
  "metrics": {
    "namespace": "OrderbookCollector",
    "metrics_collected": {
      "disk": {
        "measurement": [
          {"name": "used_percent", "rename": "DiskUsedPercent"}
        ],
        "metrics_collection_interval": 300,
        "resources": ["*"]
      },
      "mem": {
        "measurement": [
          {"name": "mem_used_percent", "rename": "MemoryUsedPercent"}
        ],
        "metrics_collection_interval": 300
      }
    }
  },
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/home/ubuntu/quants-lab/logs/orderbook_collection.log",
            "log_group_name": "/aws/orderbook-collector",
            "log_stream_name": "{instance_id}"
          }
        ]
      }
    }
  }
}
```

**启动 Agent**：

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config \
    -m ec2 \
    -c file:/home/ubuntu/cloudwatch-config.json \
    -s
```

#### **5.3 配置告警（CloudWatch Alarms）**

在 AWS 控制台：

```
CloudWatch → 告警 → 创建告警
```

**推荐告警**：

1. **磁盘使用率 > 80%**
   - 指标: `DiskUsedPercent`
   - 阈值: 80%
   - 操作: 发送 SNS 通知到邮箱

2. **CPU 使用率 > 90%（持续5分钟）**
   - 指标: `CPUUtilization`
   - 阈值: 90%
   - 持续时间: 5 分钟
   - 操作: 发送 SNS 通知

3. **网络连接失败**
   - 指标: `NetworkIn` (如果突然为0)
   - 操作: 发送 SNS 通知

---

### **阶段 6: 数据备份（重要）**

#### **6.1 自动快照（EBS Snapshots）**

```
EC2 → 卷 → 选择你的 EBS 卷 → 操作 → 创建生命周期策略
```

**配置**：
- 频率: 每天
- 保留: 7 天
- 时间: 04:00 UTC（避开高峰）

#### **6.2 数据导出到 S3（可选）**

```bash
# 安装 AWS CLI
sudo apt install awscli -y

# 配置 AWS CLI（需要 IAM 权限）
aws configure

# 创建备份脚本
cat > ~/backup_to_s3.sh << 'EOF'
#!/bin/bash
# 备份订单簿数据到 S3

DATE=$(date +%Y%m%d)
BACKUP_DIR=/home/ubuntu/quants-lab/app/data/cache/orderbook_snapshots
S3_BUCKET=s3://your-bucket-name/orderbook-backups

# 压缩并上传
tar czf /tmp/orderbook_backup_${DATE}.tar.gz ${BACKUP_DIR}
aws s3 cp /tmp/orderbook_backup_${DATE}.tar.gz ${S3_BUCKET}/
rm /tmp/orderbook_backup_${DATE}.tar.gz

echo "✅ Backup completed: ${DATE}"
EOF

chmod +x ~/backup_to_s3.sh

# 添加到 crontab（每周备份）
# 0 5 * * 0 /home/ubuntu/backup_to_s3.sh >> /home/ubuntu/quants-lab/logs/backup.log 2>&1
```

---

## 🔧 管理和维护

### **日常操作命令**

```bash
# ============================================
# 服务管理
# ============================================

# 查看服务状态
sudo systemctl status orderbook-collector

# 重启服务
sudo systemctl restart orderbook-collector

# 查看实时日志
tail -f ~/quants-lab/logs/orderbook_collection.log

# 查看系统资源
htop


# ============================================
# 监控检查
# ============================================

# 健康检查
cd ~/quants-lab && python scripts/monitor_orderbook_collection.py

# 查看磁盘使用
df -h

# 查看订单簿数据大小
du -sh ~/quants-lab/app/data/cache/orderbook_snapshots/

# 查看最新数据文件
ls -lht ~/quants-lab/app/data/cache/orderbook_snapshots/ | head -20


# ============================================
# 数据管理
# ============================================

# 清理旧数据（预览）
cd ~/quants-lab && python scripts/cleanup_old_orderbook_data.py --days 7 --dry-run

# 清理旧数据（实际删除）
cd ~/quants-lab && python scripts/cleanup_old_orderbook_data.py --days 7


# ============================================
# 下载数据到本地
# ============================================

# 从 AWS 下载数据到本地（在本地终端运行）
scp -i ~/Downloads/orderbook-key.pem -r \
    ubuntu@3.1.123.45:~/quants-lab/app/data/cache/orderbook_snapshots/ \
    /Users/alice/Dropbox/投资/量化交易/quants-lab/app/data/cache/


# ============================================
# 更新代码
# ============================================

# 停止服务
sudo systemctl stop orderbook-collector

# 更新代码（如果从 git）
cd ~/quants-lab && git pull

# 或上传新代码（从本地）
# scp -i ~/key.pem file.py ubuntu@ip:~/quants-lab/

# 重启服务
sudo systemctl start orderbook-collector
```

---

## 📊 性能优化建议

### **网络优化**

1. **选择最优区域**
   - 测试 Gate.io API 延迟：
     ```bash
     ping api.gateio.ws
     ```
   - 推荐: 新加坡 (ap-southeast-1) 或东京 (ap-northeast-1)

2. **使用增强型网络**
   - 实例类型选择带 "n" 的（如 t3n.medium）
   - 更高的网络性能

### **存储优化**

1. **使用 gp3 而非 gp2**
   - 更好的性价比
   - 可调节 IOPS 和吞吐量

2. **定期清理**
   - 保留 7-14 天数据即可
   - 旧数据备份到 S3（更便宜）

### **成本优化**

1. **使用预留实例或 Savings Plans**
   - 1年承诺: 节省 ~30%
   - 3年承诺: 节省 ~50%

2. **使用 Spot 实例（高级）**
   - 成本降低 ~70%
   - 但可能被中断（需要处理中断逻辑）

---

## 🔐 安全最佳实践

### **1. SSH 安全**

```bash
# 禁用密码登录（仅密钥登录）
sudo nano /etc/ssh/sshd_config

# 修改以下配置
PasswordAuthentication no
PubkeyAuthentication yes

# 重启 SSH
sudo systemctl restart sshd
```

### **2. 防火墙配置**

```bash
# 安装 UFW
sudo apt install ufw

# 允许 SSH
sudo ufw allow 22/tcp

# 允许 HTTPS（API 访问）
sudo ufw allow 443/tcp

# 启用防火墙
sudo ufw enable

# 查看状态
sudo ufw status
```

### **3. 定期更新**

```bash
# 自动安全更新
sudo apt install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

---

## 📞 故障排查

### **问题1: 服务启动失败**

```bash
# 查看详细日志
sudo journalctl -u orderbook-collector -n 100 --no-pager

# 检查权限
ls -la /home/ubuntu/quants-lab/

# 手动测试
cd /home/ubuntu/quants-lab
conda activate quants-lab
python cli.py trigger-task --task orderbook_snapshot_gateio --config config/orderbook_snapshot_gateio.yml
```

### **问题2: 429 限流错误**

```bash
# 检查错误频率
grep "429" ~/quants-lab/logs/orderbook_collection.log | wc -l

# 临时解决: 降低并发
# 编辑 app/tasks/data_collection/orderbook_snapshot_task.py
# MAX_CONCURRENT = 6  # 从8降到6
```

### **问题3: 磁盘空间满**

```bash
# 立即清理
cd ~/quants-lab && python scripts/cleanup_old_orderbook_data.py --days 3

# 扩展 EBS 卷（如果需要）
# AWS Console → EC2 → 卷 → 修改卷 → 增加大小
# 然后运行:
sudo growpart /dev/xvda 1
sudo resize2fs /dev/xvda1
```

---

## 🎯 完整部署检查清单

- [ ] **EC2 实例创建**: t3.medium, 500GB gp3
- [ ] **弹性 IP 分配**: 固定 IP 地址
- [ ] **安全组配置**: SSH(22), HTTPS(443)
- [ ] **SSH 连接成功**: 可以登录服务器
- [ ] **系统更新**: apt update && upgrade
- [ ] **Miniconda 安装**: conda --version
- [ ] **项目部署**: quants-lab 目录存在
- [ ] **环境创建**: quants-lab conda 环境
- [ ] **依赖安装**: pip install -r requirements.txt
- [ ] **单次测试**: 采集 24 个交易对成功
- [ ] **systemd 服务**: 服务运行正常
- [ ] **开机自启**: systemctl enable
- [ ] **Cron 任务**: 监控和清理脚本
- [ ] **CloudWatch**: 监控指标配置
- [ ] **SNS 告警**: 邮件通知配置
- [ ] **EBS 快照**: 每日自动快照
- [ ] **防火墙**: UFW 配置
- [ ] **SSH 安全**: 禁用密码登录
- [ ] **文档**: 记录 IP、密钥位置

---

## 📚 相关文档

- [快速启动指南](QUICKSTART_5S_ORDERBOOK.md)
- [高频采集配置](HIGH_FREQUENCY_ORDERBOOK_SETUP.md)
- [API 限流策略](GATEIO_API_RATE_LIMITS.md)

---

## 🎊 总结

### ✅ **AWS 部署的核心优势**

1. **稳定性**: 24/7 运行，不受本地环境影响
2. **性能**: 更低延迟，更快响应
3. **可扩展**: 存储和计算按需扩展
4. **监控**: CloudWatch 专业监控
5. **维护**: 自动化管理，省心省力

### 💰 **成本**

- **月费**: ~$75-80（约 ¥550）
- **价值**: 专业级数据采集平台
- **性价比**: 远超本地部署

### 🚀 **下一步**

1. 创建 AWS 账号（如果还没有）
2. 按照步骤创建 EC2 实例
3. 部署应用并测试
4. 配置监控和告警
5. 开始采集！

**准备好开始 AWS 部署了吗？** ☁️🎉

