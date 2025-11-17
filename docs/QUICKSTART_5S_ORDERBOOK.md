# ⚡ 5秒订单簿高频采集快速启动指南

> **适用场景**: 秒级高频交易，需要最新订单簿数据

---

## 🚀 快速启动（3步）

### 1️⃣ **启动采集任务**

```bash
# 进入项目目录
cd /Users/alice/Dropbox/投资/量化交易/quants-lab

# 测试单次采集（确保配置正确）
python cli.py trigger-task \
    --task orderbook_snapshot_gateio \
    --config config/orderbook_snapshot_gateio.yml

# 如果测试成功，启动持续采集（后台运行）
nohup python cli.py run-tasks \
    --config config/orderbook_snapshot_gateio.yml \
    > logs/orderbook_collection.log 2>&1 &

echo "✅ 订单簿采集已启动！"
```

### 2️⃣ **监控运行状态**

```bash
# 查看实时日志
tail -f logs/orderbook_collection.log

# 运行健康检查（推荐每5分钟自动执行）
python scripts/monitor_orderbook_collection.py

# 设置定时监控（可选）
(crontab -l 2>/dev/null; echo "*/5 * * * * cd /Users/alice/Dropbox/投资/量化交易/quants-lab && python scripts/monitor_orderbook_collection.py >> logs/monitor.log 2>&1") | crontab -
```

### 3️⃣ **定期清理旧数据**

```bash
# 预览要删除的数据（干运行）
python scripts/cleanup_old_orderbook_data.py --days 7 --dry-run

# 实际删除超过7天的数据
python scripts/cleanup_old_orderbook_data.py --days 7

# 设置每日自动清理（可选）
(crontab -l 2>/dev/null; echo "0 2 * * * cd /Users/alice/Dropbox/投资/量化交易/quants-lab && python scripts/cleanup_old_orderbook_data.py --days 7 >> logs/cleanup.log 2>&1") | crontab -
```

---

## 📊 关键配置

### **采集频率: 5秒**

```yaml
# config/orderbook_snapshot_gateio.yml
schedule:
  frequency_seconds: 5  # ✅ 已配置
```

### **交易对: 24个**

```yaml
trading_pairs:
  - "IRON-USDT"
  - "VIRTUAL-USDT"
  - "MIGGLES-USDT"
  # ... 共24个
```

### **订单簿深度: 100档**

```yaml
depth_limit: 100  # 足够计算精确滑点
```

---

## 💾 存储需求

| 时间周期 | 存储空间 |
|---------|---------|
| **每天** | **8.3 GB** |
| **每周** | **58 GB** |
| **每月** | **249 GB** |

**建议**: 准备 **500 GB** 可用空间

---

## 🔍 监控指标

### **正常运行状态**

| 指标 | 目标值 | 告警阈值 |
|------|--------|---------|
| 采集成功率 | >99% | <95% |
| 数据滞后 | <10秒 | >30秒 |
| 周期耗时 | <4秒 | >4.5秒 |
| 429错误率 | 0% | >1% |

### **实时检查命令**

```bash
# 检查采集任务是否运行
ps aux | grep "orderbook_snapshot"

# 查看最近100行日志
tail -100 logs/orderbook_collection.log

# 运行完整健康检查
python scripts/monitor_orderbook_collection.py

# 检查磁盘空间
df -h /Users/alice/Dropbox/投资/量化交易/quants-lab/app/data/cache/orderbook_snapshots/
```

---

## ⚠️ 常见问题排查

### **Q1: 频繁出现 429 错误**

```bash
# 检查日志中的429错误
grep "429" logs/orderbook_collection.log | wc -l

# 解决方案：降低并发或增加频率
# 编辑 app/tasks/data_collection/orderbook_snapshot_task.py
# 修改: MAX_CONCURRENT = 6  # 从8降到6
```

### **Q2: 数据滞后超过1分钟**

```bash
# 检查网络连接
ping -c 5 api.gateio.ws

# 检查Gate.io API状态
curl -s https://api.gateio.ws/api/v4/spot/time

# 重启采集任务
pkill -f orderbook_snapshot
nohup python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml > logs/orderbook_collection.log 2>&1 &
```

### **Q3: 磁盘空间不足**

```bash
# 查看当前使用情况
du -sh app/data/cache/orderbook_snapshots/

# 立即清理超过3天的数据
python scripts/cleanup_old_orderbook_data.py --days 3

# 预览要删除的文件
python scripts/cleanup_old_orderbook_data.py --days 3 --dry-run
```

---

## 📈 性能优化建议

### **如果采集跟不上（周期耗时 >4.5秒）**

**方案1: 减少并发数**

编辑 `app/tasks/data_collection/orderbook_snapshot_task.py`:

```python
MAX_CONCURRENT = 6  # 从8降到6
```

**方案2: 降低采集频率**

编辑 `config/orderbook_snapshot_gateio.yml`:

```yaml
frequency_seconds: 10  # 从5秒降到10秒
```

**方案3: 减少订单簿深度**

编辑 `config/orderbook_snapshot_gateio.yml`:

```yaml
depth_limit: 50  # 从100降到50档
```

---

## 🎯 完整工作流

### **日常运维流程**

```bash
# 每天早上：检查健康状态
python scripts/monitor_orderbook_collection.py

# 每周：检查磁盘空间
du -sh app/data/cache/orderbook_snapshots/
df -h /Users/alice/Dropbox/投资/量化交易/quants-lab/

# 每月：分析采集统计
grep "Stats:" logs/orderbook_collection.log | tail -50

# 必要时：清理旧数据
python scripts/cleanup_old_orderbook_data.py --days 7
```

### **异常处理流程**

```bash
# 1. 发现问题（采集率低、数据滞后）
python scripts/monitor_orderbook_collection.py

# 2. 查看详细日志
tail -100 logs/orderbook_collection.log

# 3. 检查429错误
grep "429" logs/orderbook_collection.log

# 4. 重启任务（如果需要）
pkill -f orderbook_snapshot
nohup python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml > logs/orderbook_collection.log 2>&1 &

# 5. 持续监控（15分钟）
watch -n 60 "python scripts/monitor_orderbook_collection.py"
```

---

## 📚 相关文档

- **详细指南**: [高频订单簿采集配置](HIGH_FREQUENCY_ORDERBOOK_SETUP.md)
- **API限流**: [Gate.io API限流策略](GATEIO_API_RATE_LIMITS.md)
- **频率选择**: [订单簿采集频率分析](ORDERBOOK_SAMPLING_FREQUENCY_GUIDE.md)
- **使用指南**: [订单簿采集完整指南](ORDERBOOK_COLLECTION_GUIDE.md)

---

## ✅ 启动清单

启动前确认：

- [ ] **磁盘空间**: 至少 500 GB 可用 ✅
- [ ] **配置文件**: `frequency_seconds: 5` ✅
- [ ] **测试运行**: 单次采集成功 ✅
- [ ] **监控脚本**: 已部署 ✅
- [ ] **清理脚本**: 已部署 ✅
- [ ] **后台运行**: 使用 nohup ✅
- [ ] **日志目录**: logs/ 目录存在 ✅

启动后监控（前24小时）：

- [ ] **每小时**: 检查日志中的错误
- [ ] **每4小时**: 运行健康检查
- [ ] **每天**: 检查磁盘空间增长
- [ ] **发现问题**: 立即调整配置

---

## 🎊 快速命令参考

```bash
# ============================================
# 启动和停止
# ============================================

# 启动（后台）
nohup python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml > logs/orderbook_collection.log 2>&1 &

# 停止
pkill -f orderbook_snapshot

# 重启
pkill -f orderbook_snapshot && \
nohup python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml > logs/orderbook_collection.log 2>&1 &


# ============================================
# 监控和检查
# ============================================

# 查看实时日志
tail -f logs/orderbook_collection.log

# 健康检查
python scripts/monitor_orderbook_collection.py

# 检查进程
ps aux | grep orderbook_snapshot

# 检查磁盘
df -h /Users/alice/Dropbox/投资/量化交易/quants-lab/


# ============================================
# 数据管理
# ============================================

# 预览清理（不删除）
python scripts/cleanup_old_orderbook_data.py --days 7 --dry-run

# 实际清理
python scripts/cleanup_old_orderbook_data.py --days 7

# 查看数据大小
du -sh app/data/cache/orderbook_snapshots/


# ============================================
# 故障排查
# ============================================

# 查看错误
tail -100 logs/orderbook_collection.log | grep ERROR

# 查看429错误
grep "429" logs/orderbook_collection.log

# 查看最新数据文件
ls -lht app/data/cache/orderbook_snapshots/ | head -30
```

---

**🎯 现在可以开始运行了！** ⚡

**记得前24小时密切监控！** 🔍

