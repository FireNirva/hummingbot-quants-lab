# 🛑 停止订单簿采集任务 - 快速指南

## ⚡ **最快方法（3秒搞定）**

```bash
bash scripts/stop_all_orderbook.sh
```

---

## 📋 **你的当前情况**

### **运行中的任务**

```
✅ 找到 2 个运行中的任务：

📋 PID 6618 - Gate.io 任务
   • 运行时长: 4小时11分
   • 配置: config/orderbook_snapshot_gateio.yml
   • CPU: 0.2%
   • 内存: 0.5%

📋 PID 80565 - MEXC 任务
   • 运行时长: 17分钟
   • 配置: config/orderbook_snapshot_mexc.yml
   • CPU: 2.8%
   • 内存: 0.5%
```

---

## 🎯 **三种停止方法**

### **方法 1：一键停止（推荐）**

```bash
bash scripts/stop_all_orderbook.sh
```

✅ **优点**：
- 最快最简单
- 自动查找所有任务
- 无需手动输入 PID
- 自动验证停止成功

---

### **方法 2：使用 kill 命令**

```bash
# 停止 Gate.io
kill 6618

# 停止 MEXC
kill 80565

# 或者一次性停止
kill 6618 80565
```

✅ **优点**：
- 直接控制
- 可以选择停止哪个

---

### **方法 3：强制停止（如果方法1失败）**

```bash
# 强制停止
kill -9 6618 80565

# 或使用 pkill
pkill -9 -f "cli.py run-tasks.*orderbook"
```

⚠️ **注意**：只在任务无法正常停止时使用

---

## 🔍 **验证任务已停止**

```bash
# 查看状态
bash scripts/status_orderbook_tasks.sh

# 或使用 ps
ps aux | grep "cli.py run-tasks.*orderbook" | grep -v grep
```

**如果已停止**：
```
❌ 没有运行中的订单簿采集任务
```

---

## 🔄 **停止后重新启动**

```bash
# 1. 停止所有任务
bash scripts/stop_all_orderbook.sh

# 2. 重新启动（选择你需要的）
# Gate.io
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml &

# MEXC
python cli.py run-tasks --config config/orderbook_snapshot_mexc.yml &

# 3. 验证
bash scripts/status_orderbook_tasks.sh
```

---

## 📚 **完整文档**

详细说明请查看：`ORDERBOOK_TASK_MANAGEMENT.md`

---

## 🎬 **实际操作演示**

### **停止所有任务**

```bash
$ bash scripts/stop_all_orderbook.sh

🔍 查找正在运行的订单簿采集任务...
🛑 正在停止 2 个任务...

   • 停止 PID 6618: config/orderbook_snapshot_gateio.yml
   • 停止 PID 80565: config/orderbook_snapshot_mexc.yml

✅ 所有订单簿采集任务已停止
```

### **验证已停止**

```bash
$ bash scripts/status_orderbook_tasks.sh

🔍 订单簿采集任务状态
==================================================

❌ 没有运行中的订单簿采集任务

💡 启动方法：
   # Gate.io
   python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml &

   # MEXC
   python cli.py run-tasks --config config/orderbook_snapshot_mexc.yml &
```

---

## ❓ **常见问题**

### **Q: 为什么没有 `cli.py stop-tasks` 命令？**

**A:** QuantsLab 设计为长期运行的服务，使用系统级别的进程管理。在开发阶段，我们提供了脚本来管理。

### **Q: 如何只停止 Gate.io 任务？**

**A:** 
```bash
kill 6618  # 使用具体的 PID
```

### **Q: 任务卡死无法停止怎么办？**

**A:**
```bash
# 强制停止
kill -9 6618
```

### **Q: 如何防止终端关闭后任务停止？**

**A:**
```bash
# 使用 nohup
nohup python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml > orderbook.log 2>&1 &
```

---

## 🚀 **你现在可以这样做**

```bash
# 1. 停止所有任务
bash scripts/stop_all_orderbook.sh

# 2. 清理旧数据（如果需要）
rm app/data/raw/orderbook_snapshots/*_20251116.parquet

# 3. 重新启动
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml &

# 4. 检查状态
bash scripts/status_orderbook_tasks.sh

# 5. 查看数据
python scripts/check_realtime_orderbook.py
```

---

**现在你知道如何停止任务了！** 🎉

**下一步**：如果你想停止任务，直接运行：
```bash
bash scripts/stop_all_orderbook.sh
```

