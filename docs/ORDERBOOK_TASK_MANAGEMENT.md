# 📋 订单簿采集任务管理指南

## 🎯 **当前问题**

你发现 `cli.py` 没有 `stop-tasks` 命令，无法直接停止任务。

```bash
# ❌ 这个命令不存在
python cli.py stop-tasks
```

**原因**：QuantsLab 的 `cli.py` 设计为持续运行的服务，没有内置停止命令。

---

## 🔍 **查看运行中的任务**

### **方法 1：使用专用脚本（推荐）**

```bash
bash scripts/status_orderbook_tasks.sh
```

**输出示例**：

```
🔍 订单簿采集任务状态
==================================================

✅ 找到 2 个运行中的任务：

📋 任务详情：
   PID:    6618
   CPU:    0.2%
   内存:   0.5%
   运行时长: 4:08.97
   配置:   config/orderbook_snapshot_gateio.yml

📋 任务详情：
   PID:    80565
   CPU:    0.2%
   内存:   0.5%
   运行时长: 0:15.91
   配置:   config/orderbook_snapshot_mexc.yml
```

---

### **方法 2：使用 ps 命令**

```bash
ps aux | grep "cli.py run-tasks.*orderbook" | grep -v grep
```

**输出示例**：

```
alice    6618   0.2  0.5 ... python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
alice    80565  0.2  0.5 ... python cli.py run-tasks --config config/orderbook_snapshot_mexc.yml
```

---

## 🛑 **停止任务**

### **方法 1：一键停止所有任务（推荐）**

```bash
bash scripts/stop_all_orderbook.sh
```

**特点**：
- ✅ 无需确认，直接停止
- ✅ 自动查找所有订单簿任务
- ✅ 优雅停止 + 强制停止
- ✅ 自动验证

---

### **方法 2：交互式停止（需要确认）**

```bash
bash scripts/stop_orderbook_tasks.sh
```

**特点**：
- ✅ 显示详细信息
- ⚠️ 需要手动确认
- ✅ 优雅停止

---

### **方法 3：手动停止（使用 kill 命令）**

```bash
# 1. 查找 PID
ps aux | grep "cli.py run-tasks.*orderbook" | grep -v grep

# 2. 停止指定任务
# Gate.io 任务
kill 6618

# MEXC 任务
kill 80565

# 或者一次性停止所有
kill 6618 80565

# 如果优雅停止失败，强制停止
kill -9 6618 80565
```

---

### **方法 4：停止所有 Python 任务（危险⚠️）**

```bash
# ⚠️ 警告：这会停止所有 Python 进程，包括其他可能在运行的脚本
pkill -f "cli.py run-tasks"

# 强制停止
pkill -9 -f "cli.py run-tasks"
```

---

## 🔄 **重启任务**

### **完整重启流程**

```bash
# 1. 停止旧任务
bash scripts/stop_all_orderbook.sh

# 2. 等待 2 秒
sleep 2

# 3. 启动新任务
# Gate.io
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml &

# MEXC（如果需要）
python cli.py run-tasks --config config/orderbook_snapshot_mexc.yml &

# 4. 验证
bash scripts/status_orderbook_tasks.sh
```

---

### **使用已有的重启脚本**

```bash
# Gate.io
bash scripts/restart_orderbook_gateio.sh

# 或使用快速重启
bash scripts/quick_restart.sh
```

---

## 📊 **任务管理总结**

| 操作 | 命令 | 说明 |
|------|------|------|
| **查看状态** | `bash scripts/status_orderbook_tasks.sh` | 显示运行中的任务 |
| **停止所有** | `bash scripts/stop_all_orderbook.sh` | 一键停止（推荐） |
| **停止确认** | `bash scripts/stop_orderbook_tasks.sh` | 需要手动确认 |
| **手动停止** | `kill <PID>` | 停止指定进程 |
| **重启** | `bash scripts/restart_orderbook_gateio.sh` | 重启 Gate.io 任务 |
| **查看数据** | `python scripts/check_realtime_orderbook.py` | 检查采集状态 |

---

## 🎬 **实际操作演示**

### **场景 1：停止所有任务**

```bash
# 查看当前运行的任务
bash scripts/status_orderbook_tasks.sh

# 输出：
# ✅ 找到 2 个运行中的任务：
#    PID: 6618 (Gate.io)
#    PID: 80565 (MEXC)

# 停止所有任务
bash scripts/stop_all_orderbook.sh

# 输出：
# 🛑 正在停止 2 个任务...
#    • 停止 PID 6618: config/orderbook_snapshot_gateio.yml
#    • 停止 PID 80565: config/orderbook_snapshot_mexc.yml
# ✅ 所有订单簿采集任务已停止

# 验证
bash scripts/status_orderbook_tasks.sh

# 输出：
# ❌ 没有运行中的订单簿采集任务
```

---

### **场景 2：只停止 Gate.io 任务**

```bash
# 1. 查找 Gate.io 任务的 PID
ps aux | grep "orderbook_snapshot_gateio" | grep -v grep

# 输出：
# alice    6618   0.2  0.5 ... config/orderbook_snapshot_gateio.yml

# 2. 停止该任务
kill 6618

# 3. 等待 2 秒
sleep 2

# 4. 验证
ps aux | grep "orderbook_snapshot_gateio" | grep -v grep
# （没有输出表示已停止）
```

---

### **场景 3：停止后重新启动**

```bash
# 1. 停止所有任务
bash scripts/stop_all_orderbook.sh

# 2. 清理旧数据（可选）
rm app/data/raw/orderbook_snapshots/*_20251116.parquet

# 3. 重新启动 Gate.io 任务
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml &

# 4. 等待 30 秒让任务初始化
sleep 30

# 5. 验证
python scripts/check_realtime_orderbook.py 2>&1 | grep -v IOError | head -50
```

---

## 💡 **为什么 cli.py 没有 stop-tasks？**

### **设计理念**

QuantsLab 的 `cli.py` 设计为：
1. ✅ **长期运行的服务**：任务应该持续运行，不需要频繁停止
2. ✅ **进程管理**：使用系统级别的进程管理（如 systemd、supervisor）
3. ✅ **Docker 部署**：在生产环境中通常在容器中运行

### **生产环境推荐做法**

#### **使用 systemd（Linux）**

```bash
# 创建服务文件
sudo nano /etc/systemd/system/orderbook-gateio.service
```

```ini
[Unit]
Description=QuantsLab Orderbook Collection - Gate.io
After=network.target

[Service]
Type=simple
User=alice
WorkingDirectory=/Users/alice/Dropbox/投资/量化交易/quants-lab
ExecStart=/opt/miniconda3/envs/quants-lab/bin/python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 启动服务
sudo systemctl start orderbook-gateio

# 停止服务
sudo systemctl stop orderbook-gateio

# 查看状态
sudo systemctl status orderbook-gateio

# 开机自启
sudo systemctl enable orderbook-gateio
```

---

#### **使用 Docker（推荐用于生产）**

```bash
# 启动
docker-compose up -d orderbook-gateio

# 停止
docker-compose stop orderbook-gateio

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f orderbook-gateio
```

---

## 🚨 **紧急情况处理**

### **任务卡死无法停止**

```bash
# 1. 尝试优雅停止
kill <PID>

# 2. 等待 5 秒
sleep 5

# 3. 强制停止
kill -9 <PID>

# 4. 验证
ps -p <PID>
# 输出：No such process（表示已停止）
```

---

### **端口被占用**

```bash
# 查找占用端口的进程
lsof -i :<PORT>

# 停止该进程
kill <PID>
```

---

### **内存占用过高**

```bash
# 查看内存使用
ps aux | grep "cli.py" | awk '{print $2, $4, $11}'

# 停止内存占用最高的任务
kill <PID>
```

---

## 📝 **最佳实践**

### **1. 使用后台运行**

```bash
# ✅ 推荐：使用 & 在后台运行
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml &

# ❌ 不推荐：前台运行（终端关闭后任务停止）
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
```

---

### **2. 使用 nohup 防止终端关闭影响**

```bash
nohup python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml > orderbook_gateio.log 2>&1 &

# 查看日志
tail -f orderbook_gateio.log
```

---

### **3. 定期检查任务状态**

```bash
# 添加到 crontab
crontab -e
```

```cron
# 每小时检查一次任务状态
0 * * * * /path/to/scripts/status_orderbook_tasks.sh >> /path/to/logs/task_status.log 2>&1
```

---

### **4. 监控脚本**

```bash
# 每分钟检查，如果任务停止则自动重启
while true; do
  if ! pgrep -f "orderbook_snapshot_gateio" > /dev/null; then
    echo "[$(date)] Task stopped, restarting..."
    python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml &
  fi
  sleep 60
done
```

---

## 🎯 **快速参考卡**

```bash
# 查看状态
bash scripts/status_orderbook_tasks.sh

# 停止所有
bash scripts/stop_all_orderbook.sh

# 重启
bash scripts/restart_orderbook_gateio.sh

# 查看数据
python scripts/check_realtime_orderbook.py

# 清理数据
rm app/data/raw/orderbook_snapshots/*

# 启动 Gate.io
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml &

# 启动 MEXC
python cli.py run-tasks --config config/orderbook_snapshot_mexc.yml &
```

---

**现在你有完整的任务管理工具了！** 🎉✨

