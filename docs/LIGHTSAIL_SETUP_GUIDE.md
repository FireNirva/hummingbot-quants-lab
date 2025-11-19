# 🚀 AWS Lightsail 新加坡实例部署指南 - quants-lab-orderbook

> **实例名称**: quants-lab-orderbook  
> **区域**: Singapore (ap-southeast-1)  
> **SSH 密钥**: quants-lab-orderbook

---

## ✅ **步骤 1: 准备工作（已完成）**

✅ SSH 密钥已创建
- 私钥：`~/.ssh/quants-lab-orderbook`
- 公钥：`~/.ssh/quants-lab-orderbook.pub`

✅ SSH 配置已更新
- 别名：`quants-lab`
- 等待填入 Lightsail IP

---

## 🔓 **你的公钥（需要上传）**

**复制下面这行内容：**

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEKwhpnwT2AfR/vChTx35ZVsvfoiWTLJAT1eh3DnegLg quants-lab-orderbook@lightsail
```

---

## 🌐 **步骤 2: 创建 Lightsail 实例**

### **方法 A: 在创建实例时上传密钥（推荐）**

1. **访问 Lightsail 控制台**
   ```
   https://lightsail.aws.amazon.com/
   ```

2. **点击 "Create instance"**

3. **选择实例位置**
   ```
   ✅ 区域: Asia Pacific
   ✅ 可用区: Singapore (ap-southeast-1a)
   ```

4. **选择实例镜像**
   ```
   ✅ 平台: Linux/Unix
   ✅ 蓝图: OS Only → Ubuntu 22.04 LTS
   ```

5. **配置 SSH 密钥 ⚠️ 重要！**
   - 展开 "SSH key pair" 部分
   - 点击 "Change SSH key pair"
   - 选择 "Upload New"
   - 复制粘贴你的公钥：
     ```
     ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEKwhpnwT2AfR/vChTx35ZVsvfoiWTLJAT1eh3DnegLg quants-lab-orderbook@lightsail
     ```
   - 密钥名称：`quants-lab-orderbook`

6. **选择实例套餐**
   ```
   ✅ 选择: $20/月
   ✅ 配置: 4 GB RAM, 2 vCPU, 80 GB SSD
   ✅ 流量: 4 TB
   ```

7. **设置实例名称**
   ```
   ✅ 实例名称: quants-lab-orderbook
   ```

8. **创建实例**
   - 点击 "Create instance"
   - 等待 3-5 分钟实例启动

9. **记录实例 IP**
   - 实例启动后，记录公网 IP
   - 例如：`18.139.xxx.xxx`

---

### **方法 B: 在实例创建后手动添加密钥**

如果你已经创建了实例但没有上传密钥：

1. **使用 Lightsail 浏览器终端连接**
   - 在 Lightsail 控制台点击实例名称
   - 点击 "Connect using SSH"

2. **添加公钥到 authorized_keys**
   ```bash
   # 在 Lightsail 终端中运行
   echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEKwhpnwT2AfR/vChTx35ZVsvfoiWTLJAT1eh3DnegLg quants-lab-orderbook@lightsail" >> ~/.ssh/authorized_keys
   
   # 设置正确权限
   chmod 600 ~/.ssh/authorized_keys
   
   # 验证
   cat ~/.ssh/authorized_keys
   ```

---

## 🔌 **步骤 3: 更新本地 SSH 配置**

1. **更新 SSH config 文件**

   在你的本地 Mac 上运行：

   ```bash
   nano ~/.ssh/config
   ```

2. **找到这一段并更新 IP：**

   ```
   Host quants-lab
     HostName REPLACE-WITH-LIGHTSAIL-IP  ← 改成实际 IP
     Port 22
     User ubuntu
     IdentityFile ~/.ssh/quants-lab-orderbook
     IdentitiesOnly yes
     ServerAliveInterval 60
     ServerAliveCountMax 3
   ```

   **例如：**
   ```
   Host quants-lab
     HostName 18.139.123.45
     Port 22
     User ubuntu
     IdentityFile ~/.ssh/quants-lab-orderbook
     IdentitiesOnly yes
     ServerAliveInterval 60
     ServerAliveCountMax 3
   ```

3. **保存并退出**
   - 按 `Ctrl+X`
   - 按 `Y` 确认
   - 按 `Enter` 保存

---

## 🧪 **步骤 4: 测试连接**

```bash
# 测试 SSH 连接
ssh quants-lab

# 应该看到
# Welcome to Ubuntu 22.04 LTS...
# ubuntu@ip-xxx-xxx-xxx-xxx:~$
```

✅ **连接成功！**

---

## 📦 **步骤 5: 部署 quants-lab 系统**

现在在 Lightsail 实例上运行：

### **5.1 更新系统**

```bash
sudo apt update && sudo apt upgrade -y
```

### **5.2 安装 Miniconda**

```bash
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
rm Miniconda3-latest-Linux-x86_64.sh
```

### **5.3 初始化 Conda**

```bash
eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
echo 'eval "$($HOME/miniconda3/bin/conda shell.bash hook)"' >> ~/.bashrc
source ~/.bashrc
```

### **5.4 克隆项目**

```bash
cd ~
git clone https://github.com/YOUR-USERNAME/quants-lab.git
cd quants-lab
```

⚠️ **替换 `YOUR-USERNAME` 为你的 GitHub 用户名**

或者如果还没上传到 GitHub，从本地上传：

```bash
# 在本地 Mac 运行
cd /Users/alice/Dropbox/投资/量化交易/quants-lab
scp -r . quants-lab:~/quants-lab/
```

### **5.5 创建 Conda 环境**

```bash
cd ~/quants-lab
conda env create -f environment.yml
```

### **5.6 激活环境并安装**

```bash
conda activate quants-lab
pip install -e .
```

### **5.7 创建数据目录**

```bash
mkdir -p app/data/raw/orderbook_snapshots
mkdir -p logs
```

### **5.8 验证安装**

```bash
python cli.py --help
```

✅ **看到帮助信息 = 安装成功！**

---

## 🚀 **步骤 6: 启动订单簿采集**

### **6.1 检查配置文件**

```bash
cat config/orderbook_snapshot_gateio.yml
```

### **6.2 创建 systemd 服务**

```bash
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
```

### **6.3 启动服务**

```bash
# 重载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start orderbook-gateio

# 设置开机自启
sudo systemctl enable orderbook-gateio

# 查看状态
sudo systemctl status orderbook-gateio
```

### **6.4 查看日志**

```bash
# 实时日志
sudo journalctl -u orderbook-gateio -f

# 或查看文件
tail -f ~/quants-lab/logs/orderbook_gateio.log
```

---

## 📊 **步骤 7: 验证数据采集**

等待 30-60 秒后：

```bash
cd ~/quants-lab
conda activate quants-lab

# 检查采集状态
python scripts/check_realtime_orderbook.py

# 查看数据文件
ls -lh app/data/raw/orderbook_snapshots/

# 应该看到类似：
# gate_io_VIRTUAL-USDT_20251116.parquet
# gate_io_LMTS-USDT_20251116.parquet
# ...
```

✅ **看到数据文件 = 采集成功！**

---

## 🔧 **常用管理命令**

### **连接到服务器**

```bash
ssh quants-lab
```

### **查看采集状态**

```bash
cd ~/quants-lab
conda activate quants-lab
python scripts/check_realtime_orderbook.py
```

### **查看服务状态**

```bash
sudo systemctl status orderbook-gateio
```

### **重启服务**

```bash
sudo systemctl restart orderbook-gateio
```

### **停止服务**

```bash
sudo systemctl stop orderbook-gateio
```

### **查看日志**

```bash
# 实时日志
sudo journalctl -u orderbook-gateio -f

# 最近 100 行
sudo journalctl -u orderbook-gateio -n 100
```

### **查看系统资源**

```bash
# CPU 和内存
htop

# 磁盘空间
df -h

# 网络流量
nethogs
```

---

## 🗑️ **数据管理**

### **清理旧数据**

```bash
cd ~/quants-lab
conda activate quants-lab

# 预览要删除的文件（不实际删除）
python scripts/cleanup_old_orderbook_data.py --days 7 --dry-run

# 实际删除
python scripts/cleanup_old_orderbook_data.py --days 7
```

### **设置自动清理**

```bash
# 编辑 crontab
crontab -e

# 添加（每天凌晨 2 点清理超过 7 天的数据）
0 2 * * * cd /home/ubuntu/quants-lab && /home/ubuntu/miniconda3/envs/quants-lab/bin/python scripts/cleanup_old_orderbook_data.py --days 7 >> logs/cleanup.log 2>&1
```

---

## 📈 **运行套利分析**

### **下载 CEX 数据**

```bash
cd ~/quants-lab
conda activate quants-lab

python scripts/import_freqtrade_data.py \
  --config config/gateio_USDT_downloader_full.yml \
  --days 7
```

### **下载 DEX 数据**

```bash
python scripts/build_pool_mapping.py --connector gate_io --network base
python scripts/download_dex_ohlcv.py --network base --days 3
```

### **分析价差**

```bash
python scripts/analyze_cex_dex_spread.py --compare-all
```

### **计算最优交易规模**

```bash
python scripts/calculate_optimal_trade_size.py VIRTUAL-USDT 1.5 --connector gate_io
```

---

## 💾 **数据备份**

### **导出到本地**

在本地 Mac 运行：

```bash
# 导出订单簿数据
scp -r quants-lab:~/quants-lab/app/data/raw/orderbook_snapshots/ \
  ./local_backup/

# 导出日志
scp -r quants-lab:~/quants-lab/logs/ \
  ./local_logs/
```

### **创建 Lightsail 快照**

1. 在 Lightsail 控制台进入实例页面
2. 点击 "Snapshots" 标签
3. 点击 "Create snapshot"
4. 命名：`quants-lab-orderbook-20251116`
5. 等待快照完成

---

## 🚨 **故障排除**

### **问题 1: SSH 连接失败**

```bash
# 检查 SSH 配置
cat ~/.ssh/config | grep -A 7 "quants-lab"

# 测试连接（详细模式）
ssh -v quants-lab

# 检查密钥权限
ls -l ~/.ssh/quants-lab-orderbook
# 应该是 -rw-------（600）
```

### **问题 2: 采集进程停止**

```bash
# 查看服务状态
sudo systemctl status orderbook-gateio

# 查看错误日志
tail -100 ~/quants-lab/logs/orderbook_gateio_error.log

# 重启服务
sudo systemctl restart orderbook-gateio
```

### **问题 3: 磁盘空间不足**

```bash
# 检查磁盘使用
df -h

# 清理旧数据
python scripts/cleanup_old_orderbook_data.py --days 3

# 清理系统缓存
sudo apt clean
sudo apt autoremove -y
```

---

## ✅ **部署检查清单**

- [ ] SSH 密钥已创建
- [ ] Lightsail 实例已创建（新加坡）
- [ ] 公钥已上传到 Lightsail
- [ ] SSH config 已更新（填入实际 IP）
- [ ] SSH 连接测试成功
- [ ] 系统已更新
- [ ] Miniconda 已安装
- [ ] quants-lab 已克隆
- [ ] Conda 环境已创建
- [ ] 项目已安装
- [ ] 数据目录已创建
- [ ] systemd 服务已创建
- [ ] 订单簿采集已启动
- [ ] 数据采集验证成功
- [ ] 监控定时任务已设置

---

## 📚 **相关文档**

- 快速开始：`docs/AWS_LIGHTSAIL_QUICKSTART.md`
- 完整指南：`docs/AWS_LIGHTSAIL_DEPLOYMENT_GUIDE.md`
- 延迟分析：`docs/AWS_REGION_LATENCY_ANALYSIS.md`
- 订单簿采集：`docs/ORDERBOOK_COLLECTION_GUIDE.md`

---

## 🎉 **恭喜！部署完成！**

你现在有一个：
- ✅ 24/7 运行的订单簿数据采集系统
- ✅ 5 秒高频数据（100 档深度）
- ✅ 6 个 Gate.io 交易对 + 3 个 MEXC 交易对
- ✅ 自动重启和监控
- ✅ 新加坡低延迟服务器
- ✅ 月成本仅 $20（¥145）

**开始收集数据并进行套利分析吧！** 🚀💰

