# 🚀 启动订单簿采集 - 使用 run-tasks 命令

> **使用 QuantsLab 的 `run-tasks` 命令启动订单簿采集**

---

## ✅ **推荐方式：使用 run-tasks**

### **Gate.io 订单簿采集**

```bash
cd /Users/alice/Dropbox/投资/量化交易/quants-lab

# 启动 Gate.io 订单簿采集（6个交易对）
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
```

**配置文件**: `config/orderbook_snapshot_gateio.yml`
- **交易对**: VIRTUAL-USDT, LMTS-USDT, BNKR-USDT, PRO-USDT, IRON-USDT, MIGGLES-USDT
- **频率**: 每 5 秒采集一次
- **深度**: 100 档

---

### **MEXC 订单簿采集**

```bash
cd /Users/alice/Dropbox/投资/量化交易/quants-lab

# 启动 MEXC 订单簿采集（3个交易对）
python cli.py run-tasks --config config/orderbook_snapshot_mexc.yml
```

**配置文件**: `config/orderbook_snapshot_mexc.yml`
- **交易对**: AUKI-USDT, SERV-USDT, IRON-USDT
- **频率**: 每 5 秒采集一次
- **深度**: 100 档

---

## 📋 **运行方式对比**

| 方式 | 命令 | 说明 | 适用场景 |
|------|------|------|----------|
| **run-tasks** ✅ | `python cli.py run-tasks --config xxx.yml` | 持续运行任务 | **生产环境**（推荐） |
| **trigger-task** | `python cli.py trigger-task --task xxx --config xxx.yml` | 运行一次任务 | 测试、调试 |
| **测试脚本** | `python scripts/test_xxx.py` | 快速测试 | 开发、验证 |

---

## 🎯 **推荐部署方式**

### **方式 1: 直接运行（前台）**

```bash
# 直接在终端运行（会占用终端）
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
```

**优点**: 简单直接，可以立即看到输出
**缺点**: 关闭终端后程序停止

---

### **方式 2: 后台运行（nohup）**

```bash
# 后台运行 Gate.io 采集
nohup python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml \
  > logs/orderbook_gateio.log 2>&1 &

# 后台运行 MEXC 采集
nohup python cli.py run-tasks --config config/orderbook_snapshot_mexc.yml \
  > logs/orderbook_mexc.log 2>&1 &

# 查看进程
ps aux | grep "run-tasks"

# 查看日志
tail -f logs/orderbook_gateio.log
tail -f logs/orderbook_mexc.log
```

**优点**: 后台运行，不占用终端
**缺点**: 需要手动管理进程

---

### **方式 3: systemd 服务（推荐生产环境）** ⭐

#### **创建 Gate.io 服务**

```bash
sudo nano /etc/systemd/system/orderbook-gateio.service
```

```ini
[Unit]
Description=OrderBook Collection - Gate.io
After=network.target

[Service]
Type=simple
User=alice
WorkingDirectory=/Users/alice/Dropbox/投资/量化交易/quants-lab
ExecStart=/opt/anaconda3/envs/quants-lab/bin/python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
Restart=always
RestartSec=10
StandardOutput=append:/Users/alice/Dropbox/投资/量化交易/quants-lab/logs/orderbook_gateio.log
StandardError=append:/Users/alice/Dropbox/投资/量化交易/quants-lab/logs/orderbook_gateio.log

[Install]
WantedBy=multi-user.target
```

#### **创建 MEXC 服务**

```bash
sudo nano /etc/systemd/system/orderbook-mexc.service
```

```ini
[Unit]
Description=OrderBook Collection - MEXC
After=network.target

[Service]
Type=simple
User=alice
WorkingDirectory=/Users/alice/Dropbox/投资/量化交易/quants-lab
ExecStart=/opt/anaconda3/envs/quants-lab/bin/python cli.py run-tasks --config config/orderbook_snapshot_mexc.yml
Restart=always
RestartSec=10
StandardOutput=append:/Users/alice/Dropbox/投资/量化交易/quants-lab/logs/orderbook_mexc.log
StandardError=append:/Users/alice/Dropbox/投资/量化交易/quants-lab/logs/orderbook_mexc.log

[Install]
WantedBy=multi-user.target
```

#### **启动服务**

```bash
# 重新加载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start orderbook-gateio
sudo systemctl start orderbook-mexc

# 设置开机自启
sudo systemctl enable orderbook-gateio
sudo systemctl enable orderbook-mexc

# 查看状态
sudo systemctl status orderbook-gateio
sudo systemctl status orderbook-mexc

# 停止服务
sudo systemctl stop orderbook-gateio
sudo systemctl stop orderbook-mexc

# 重启服务
sudo systemctl restart orderbook-gateio
sudo systemctl restart orderbook-mexc
```

**优点**: 
- ✅ 自动重启
- ✅ 开机自启
- ✅ 统一管理
- ✅ 日志管理

---

## 📊 **运行时日志**

### **实时查看日志**

```bash
# Gate.io 日志
tail -f logs/orderbook_gateio.log

# MEXC 日志
tail -f logs/orderbook_mexc.log
```

### **预期输出**

```
INFO:__main__:Starting task runner with 1 tasks
INFO:__main__:Task orderbook_snapshot_gateio is scheduled to run every 5 seconds
INFO:app.tasks.data_collection.orderbook_snapshot_task:Starting orderbook snapshot collection for 6 pairs
INFO:app.tasks.data_collection.orderbook_snapshot_task:Using concurrent limit: 8
INFO:app.tasks.data_collection.orderbook_snapshot_task:✅ VIRTUAL-USDT: Collected with update_id=548631456, 100 bids, 100 asks
INFO:app.tasks.data_collection.orderbook_snapshot_task:✅ IRON-USDT: Collected with update_id=548632001, 100 bids, 100 asks
INFO:app.tasks.data_collection.orderbook_snapshot_task:Orderbook snapshot collection completed: 6/6 successful
```

---

## 🔍 **验证运行状态**

### **1. 检查进程**

```bash
# 查看 Python 进程
ps aux | grep "cli.py run-tasks"

# 查看订单簿采集进程
ps aux | grep orderbook
```

### **2. 检查数据文件**

```bash
# 查看数据目录
ls -lh app/data/raw/orderbook_snapshots/

# 预期文件（按日期命名）
gate_io_VIRTUAL_USDT_20241116.parquet
gate_io_LMTS_USDT_20241116.parquet
gate_io_BNKR_USDT_20241116.parquet
gate_io_PRO_USDT_20241116.parquet
gate_io_IRON_USDT_20241116.parquet
gate_io_MIGGLES_USDT_20241116.parquet
```

### **3. 验证数据质量**

```python
from app.tasks.data_collection.orderbook_snapshot_task import (
    load_orderbook_snapshots,
    validate_update_ids
)

# 读取数据
df = load_orderbook_snapshots('gate_io', 'IRON-USDT')

print(f"📊 数据记录: {len(df)} 条")
print(f"📅 时间范围: {df['timestamp'].min()} - {df['timestamp'].max()}")
print(f"🔢 Update ID: {df['update_id'].min():.0f} - {df['update_id'].max():.0f}")

# 验证质量
report = validate_update_ids(df)
print(f"✅ 数据质量: {report['quality_score']:.1f}/100")
```

---

## ⚠️ **常见问题**

### **问题 1: 端口已被占用**

如果看到端口占用错误，检查是否已有程序在运行：

```bash
ps aux | grep "cli.py"
kill <PID>  # 停止旧进程
```

### **问题 2: 权限错误**

确保用户有写入日志和数据目录的权限：

```bash
chmod -R 755 logs/
chmod -R 755 app/data/raw/orderbook_snapshots/
```

### **问题 3: 日志文件不存在**

创建日志目录：

```bash
mkdir -p logs
```

---

## 📋 **快速命令参考**

### **启动采集**

```bash
# 前台运行（测试用）
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml

# 后台运行（生产用）
nohup python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml \
  > logs/orderbook_gateio.log 2>&1 &

# systemd 服务（推荐）
sudo systemctl start orderbook-gateio
```

### **监控状态**

```bash
# 查看日志
tail -f logs/orderbook_gateio.log

# 查看进程
ps aux | grep orderbook

# 查看数据文件
ls -lh app/data/raw/orderbook_snapshots/
```

### **停止采集**

```bash
# 后台进程
ps aux | grep "cli.py run-tasks"
kill <PID>

# systemd 服务
sudo systemctl stop orderbook-gateio
```

---

## 🎉 **总结**

| 特性 | run-tasks | 测试脚本 |
|------|-----------|----------|
| **持续运行** | ✅ 是 | ❌ 否 |
| **自动重试** | ✅ 是 | ❌ 否 |
| **日志记录** | ✅ 完整 | ⚠️ 简单 |
| **适用场景** | **生产环境** ✅ | 开发测试 |

---

**推荐流程**:

1. **测试阶段**: 使用测试脚本快速验证
   ```bash
   python scripts/test_multi_exchange_orderbook.py
   ```

2. **生产运行**: 使用 run-tasks 命令 ⭐
   ```bash
   python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
   ```

3. **长期部署**: 配置 systemd 服务
   ```bash
   sudo systemctl start orderbook-gateio
   ```

---

**🚀 现在就可以使用 `run-tasks` 启动订单簿采集了！** ✨

