# ⚡ AWS Lightsail 快速开始 - 10 分钟完成部署

## 📋 **部署检查清单**

### **阶段 1: 创建 Lightsail 实例（5 分钟）**

- [ ] 1. 访问 https://lightsail.aws.amazon.com/
- [ ] 2. 点击 "Create instance"
- [ ] 3. 选择配置：
  ```
  区域:    Singapore
  平台:    Ubuntu 22.04 LTS
  套餐:    $20/月 (4 GB RAM, 2 vCPU, 80 GB SSD)
  名称:    quants-lab-orderbook
  ```
- [ ] 4. 下载 SSH 密钥（保存为 `lightsail-quants-lab.pem`）
- [ ] 5. 点击 "Create instance"
- [ ] 6. 等待实例启动（3-5 分钟）
- [ ] 7. 记录实例公网 IP: `_________________`

---

### **阶段 2: 部署系统（3 分钟）**

#### **连接到实例**

```bash
# 本地终端运行（替换 YOUR-IP）
chmod 400 ~/Downloads/lightsail-quants-lab.pem
ssh -i ~/Downloads/lightsail-quants-lab.pem ubuntu@YOUR-IP
```

#### **自动部署**

在 Lightsail 实例上运行：

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 下载并运行安装脚本（一行命令）
cd ~ && \
curl -sSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh && \
bash miniconda.sh -b -p $HOME/miniconda3 && \
rm miniconda.sh && \
eval "$($HOME/miniconda3/bin/conda shell.bash hook)" && \
echo 'eval "$($HOME/miniconda3/bin/conda shell.bash hook)"' >> ~/.bashrc && \
git clone https://github.com/YOUR-USERNAME/quants-lab.git && \
cd quants-lab && \
conda env create -f environment.yml && \
conda activate quants-lab && \
pip install -e . && \
mkdir -p app/data/raw/orderbook_snapshots logs
```

**检查安装：**

```bash
cd ~/quants-lab
conda activate quants-lab
python cli.py --help
```

✅ 看到帮助信息 = 安装成功！

---

### **阶段 3: 启动订单簿采集（2 分钟）**

#### **方法 A: 使用 systemd（推荐）**

```bash
# 创建服务
sudo tee /etc/systemd/system/orderbook-gateio.service > /dev/null <<'EOF'
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

# 启动服务
sudo systemctl daemon-reload
sudo systemctl start orderbook-gateio
sudo systemctl enable orderbook-gateio

# 查看状态
sudo systemctl status orderbook-gateio
```

#### **方法 B: 使用 screen（简单）**

```bash
cd ~/quants-lab
conda activate quants-lab

# 创建后台会话
screen -S orderbook

# 启动采集
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml

# 按 Ctrl+A 然后 D 退出（任务继续运行）
```

---

### **阶段 4: 验证采集（1 分钟）**

```bash
cd ~/quants-lab
conda activate quants-lab

# 等待 30 秒后检查
sleep 30

# 查看实时状态
python scripts/check_realtime_orderbook.py
```

**预期输出：**
```
📊 实时订单簿采集状态

交易对: VIRTUAL-USDT
   • 最新采集: 2025-11-17 10:23:45 UTC
   • 平均间隔: 5.01 秒 ✅
   • Update ID 范围: 1234567890 → 1234568123
   • 最新买1价: $0.1234
   • 最新卖1价: $0.1235
```

✅ 看到实时数据 = 采集成功！

---

## 🎯 **核心命令（记住这 5 个）**

### **1. 连接实例**
```bash
ssh -i ~/Downloads/lightsail-quants-lab.pem ubuntu@YOUR-IP
```

### **2. 查看采集状态**
```bash
cd ~/quants-lab
conda activate quants-lab
python scripts/check_realtime_orderbook.py
```

### **3. 查看日志**
```bash
# systemd
sudo journalctl -u orderbook-gateio -f

# 或查看日志文件
tail -f ~/quants-lab/logs/orderbook_gateio.log
```

### **4. 重启采集**
```bash
sudo systemctl restart orderbook-gateio
```

### **5. 查看数据文件**
```bash
ls -lh ~/quants-lab/app/data/raw/orderbook_snapshots/
```

---

## 📊 **设置监控（可选）**

### **定时检查**

```bash
# 编辑 crontab
crontab -e

# 添加（每小时检查，每天凌晨清理）
0 * * * * cd /home/ubuntu/quants-lab && /home/ubuntu/miniconda3/envs/quants-lab/bin/python scripts/check_realtime_orderbook.py >> logs/monitoring.log 2>&1
0 2 * * * cd /home/ubuntu/quants-lab && /home/ubuntu/miniconda3/envs/quants-lab/bin/python scripts/cleanup_old_orderbook_data.py --days 7 >> logs/cleanup.log 2>&1
```

---

## 💰 **成本控制**

### **预期成本**
```
Lightsail 实例:  $20/月
快照备份:        $2/月（可选）
总计:           约 $22/月（¥160/月）
```

### **节省成本**
- 使用 $10/月 套餐（2 GB RAM）- 但可能不够用
- 定期清理数据（保留 7 天）
- 不需要时停止实例

---

## 🚨 **常见问题**

### **Q1: 采集没有数据？**

**检查：**
```bash
sudo systemctl status orderbook-gateio
tail -100 ~/quants-lab/logs/orderbook_gateio.log
```

**解决：**
```bash
sudo systemctl restart orderbook-gateio
```

### **Q2: 磁盘空间满了？**

**检查：**
```bash
df -h
```

**解决：**
```bash
python scripts/cleanup_old_orderbook_data.py --days 3
```

### **Q3: 如何停止采集？**

```bash
sudo systemctl stop orderbook-gateio
```

### **Q4: 如何导出数据到本地？**

```bash
# 在本地运行
scp -i ~/Downloads/lightsail-quants-lab.pem -r \
  ubuntu@YOUR-IP:/home/ubuntu/quants-lab/app/data/raw/orderbook_snapshots/ \
  ./local_backup/
```

---

## 📈 **数据分析（在 AWS 上）**

### **价差分析**

```bash
cd ~/quants-lab
conda activate quants-lab

# 下载 CEX 和 DEX 数据
python scripts/import_freqtrade_data.py --config config/gateio_USDT_downloader_full.yml --days 7
python scripts/build_pool_mapping.py --connector gate_io --network base
python scripts/download_dex_ohlcv.py --network base --days 3

# 分析价差
python scripts/analyze_cex_dex_spread.py --compare-all

# 计算最优交易规模
python scripts/calculate_optimal_trade_size.py VIRTUAL-USDT 1.5 --connector gate_io
```

---

## ✅ **部署完成检查清单**

- [ ] Lightsail 实例已创建
- [ ] 系统已部署（conda, quants-lab）
- [ ] 订单簿采集已启动
- [ ] 实时状态检查正常（5 秒间隔）
- [ ] 数据文件正常生成
- [ ] 日志无错误
- [ ] 监控定时任务已设置
- [ ] 记录了实例 IP 和 SSH 命令

---

## 🎉 **恭喜！部署完成！**

你现在有一个：
- ✅ 24/7 运行的订单簿数据采集系统
- ✅ 5 秒高频数据（100 档深度）
- ✅ 6 个 Gate.io 交易对
- ✅ 自动重启和监控
- ✅ 月成本只需 $20（¥145）

---

**需要详细文档？查看：**
- 📚 完整部署指南：`docs/AWS_LIGHTSAIL_DEPLOYMENT_GUIDE.md`
- 📖 订单簿采集：`docs/ORDERBOOK_COLLECTION_GUIDE.md`
- 🛠️ 所有脚本：`scripts/README.md`

**开始套利吧！** 🚀💰

