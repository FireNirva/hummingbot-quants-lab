# ⚡ 高频订单簿采集配置指南（5秒间隔）

## 🎯 使用场景

**秒级高频交易** - 需要最新订单簿数据以快速响应市场变化

---

## 📊 5秒采集频率分析

### **基础参数**

- **交易对数量**: 24 个
- **采集频率**: 每 5 秒
- **交易所**: Gate.io
- **订单簿深度**: 100 档

---

## 🔢 **关键指标计算**

### **请求频率**

```
每5秒采集24个交易对
= 24 请求 / 5 秒
= 4.8 请求/秒
= 288 请求/分钟
= 17,280 请求/小时
= 414,720 请求/天
```

### **Gate.io API 限制对比**

| 项目 | 你的使用 | Gate.io 限制 | 使用率 | 状态 |
|------|---------|-------------|--------|------|
| **请求频率** | 4.8次/秒 | 100次/秒 | **4.8%** | ✅ 安全 |
| **并发连接** | 8个（Semaphore控制） | 10个 | **80%** | ⚠️ 需监控 |
| **每秒峰值** | ~24次（突发） | 100次/秒 | 24% | ✅ 安全 |

**结论**: ✅ 在API限制范围内，但需要严格的并发控制

---

## 💾 **存储成本分析**

### **数据量估算**

每个订单簿快照大小（Parquet压缩后）：
- 100档订单簿 ≈ 15 KB
- 包含元数据 ≈ 20 KB

```
每5秒: 24对 × 20 KB = 480 KB
每分钟: 480 KB × 12 = 5.76 MB
每小时: 5.76 MB × 60 = 345.6 MB
每天: 345.6 MB × 24 = 8.3 GB
每月: 8.3 GB × 30 = 249 GB
每年: 249 GB × 12 = 2.98 TB
```

### **成本对比**

| 频率 | 每天 | 每月 | 年度 | 相对成本 |
|------|------|------|------|---------|
| **5秒** | **8.3 GB** | **249 GB** | **2.98 TB** | **100%** |
| 10秒 | 4.2 GB | 125 GB | 1.5 TB | 50% |
| 30秒 | 1.4 GB | 42 GB | 500 GB | 17% |
| 1分钟 | 0.7 GB | 21 GB | 250 GB | 8% |

**存储需求**: 
- **每月 ~250 GB**（建议准备 **500 GB** 空间）
- **年度 ~3 TB**（建议准备 **5 TB** 空间）

---

## ⚠️ **风险评估与缓解**

### **风险 1: API 限流 ⚠️⚠️⚠️**

**风险等级**: 🔴 **中高**

**具体风险**:
- 24个请求在5秒内发出
- 如果网络延迟，可能积压请求
- 突发并发可能超过10个连接限制

**缓解措施**:

✅ **已实施**:
```python
# 在 OrderBookSnapshotTask 中
MAX_CONCURRENT = 8  # 限制并发连接
semaphore = asyncio.Semaphore(MAX_CONCURRENT)
await asyncio.sleep(0.1)  # 请求间隔0.1秒
```

⚠️ **需要额外实施**:

1. **增强的错误处理**

```python
# 建议添加到 OrderBookSnapshotTask._collect_orderbook_snapshot
from aiohttp import ClientResponseError
import asyncio

async def _collect_orderbook_snapshot_with_retry(self, trading_pair: str):
    """带重试和指数退避的订单簿采集"""
    max_retries = 3
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            return await self._collect_orderbook_snapshot(trading_pair)
        except ClientResponseError as e:
            if e.status == 429:  # Too Many Requests
                delay = base_delay * (2 ** attempt)  # 指数退避
                logger.warning(f"Rate limited for {trading_pair}, retry in {delay}s")
                await asyncio.sleep(delay)
            else:
                raise
    
    logger.error(f"Failed to collect {trading_pair} after {max_retries} retries")
    return None
```

2. **请求分批策略**

```python
# 将24个交易对分为3批，每批8个
BATCH_SIZE = 8
BATCH_DELAY = 1.5  # 批次间延迟1.5秒

for i in range(0, len(self.trading_pairs), BATCH_SIZE):
    batch = self.trading_pairs[i:i+BATCH_SIZE]
    tasks = [collect_with_limit(pair) for pair in batch]
    await asyncio.gather(*tasks, return_exceptions=True)
    
    if i + BATCH_SIZE < len(self.trading_pairs):
        await asyncio.sleep(BATCH_DELAY)  # 批次间延迟
```

---

### **风险 2: 磁盘空间不足 ⚠️⚠️**

**风险等级**: 🟡 **中**

**具体风险**:
- 每月249GB，可能快速填满磁盘
- 磁盘满导致任务失败

**缓解措施**:

1. **自动清理旧数据**

```python
# 建议创建清理脚本
from datetime import datetime, timedelta
import shutil

def cleanup_old_orderbook_data(days_to_keep=7):
    """清理超过N天的订单簿数据"""
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    orderbook_dir = data_paths.orderbook_snapshots_dir
    
    for file in orderbook_dir.glob("*.parquet"):
        # 从文件名解析日期
        # gate_io_IRON_USDT_20241112.parquet
        date_str = file.stem.split('_')[-1]
        file_date = datetime.strptime(date_str, '%Y%m%d')
        
        if file_date < cutoff_date:
            file.unlink()
            logger.info(f"Deleted old file: {file.name}")
```

2. **磁盘监控**

```bash
# 添加到 crontab
0 */6 * * * python scripts/check_disk_space.py
```

```python
# scripts/check_disk_space.py
import shutil
import logging

def check_disk_space(warning_threshold_gb=50):
    """检查可用磁盘空间"""
    total, used, free = shutil.disk_usage("/")
    free_gb = free / (2**30)
    
    if free_gb < warning_threshold_gb:
        logger.error(f"⚠️ Low disk space: {free_gb:.1f} GB remaining")
        # 发送告警邮件或通知
        return False
    
    logger.info(f"✅ Disk space OK: {free_gb:.1f} GB free")
    return True
```

---

### **风险 3: 网络延迟积压 ⚠️**

**风险等级**: 🟡 **中低**

**具体风险**:
- Gate.io API 响应慢（>1秒）
- 5秒内无法完成24个请求
- 请求积压

**缓解措施**:

1. **超时控制**

```python
# 在配置中
config:
  request_timeout_seconds: 3  # 单个请求最长3秒
```

2. **性能监控**

```python
# 在任务中记录执行时间
import time

start = time.time()
# ... 执行采集 ...
duration = time.time() - start

if duration > 4.5:  # 接近5秒周期
    logger.warning(f"⚠️ Cycle took {duration:.2f}s, may cause backlog")
```

---

## 📈 **监控指标**

### **关键指标**

创建监控脚本 `scripts/monitor_orderbook_collection.py`:

```python
import pandas as pd
from datetime import datetime, timedelta
from core.data_paths import data_paths

def monitor_orderbook_collection():
    """监控订单簿采集健康度"""
    
    # 1. 检查最新数据时间
    latest_files = {}
    for pair in TRADING_PAIRS:
        today = datetime.now().strftime('%Y%m%d')
        filename = f"gate_io_{pair.replace('-', '_')}_{today}.parquet"
        filepath = data_paths.orderbook_snapshots_dir / filename
        
        if filepath.exists():
            df = pd.read_parquet(filepath)
            latest_time = df['timestamp'].max()
            latest_files[pair] = latest_time
    
    # 2. 检测数据滞后
    now = datetime.now()
    lagging_pairs = []
    
    for pair, last_time in latest_files.items():
        lag = (now - last_time).total_seconds()
        if lag > 30:  # 滞后超过30秒
            lagging_pairs.append((pair, lag))
            logger.warning(f"⚠️ {pair} data lagging by {lag:.0f}s")
    
    # 3. 检测采集率
    for pair, last_time in latest_files.items():
        df = pd.read_parquet(filepath)
        # 最近5分钟应该有60个数据点（每5秒一个）
        recent = df[df['timestamp'] > now - timedelta(minutes=5)]
        expected_count = 60
        actual_count = len(recent)
        collection_rate = (actual_count / expected_count) * 100
        
        if collection_rate < 90:
            logger.warning(f"⚠️ {pair} collection rate: {collection_rate:.1f}%")
    
    # 4. 生成报告
    print("=" * 60)
    print(f"📊 Orderbook Collection Health Report - {now}")
    print("=" * 60)
    print(f"✅ Pairs with fresh data: {len(latest_files)}/24")
    print(f"⚠️ Lagging pairs: {len(lagging_pairs)}")
    if lagging_pairs:
        for pair, lag in lagging_pairs:
            print(f"   • {pair}: {lag:.0f}s behind")
    print("=" * 60)

if __name__ == "__main__":
    monitor_orderbook_collection()
```

**运行监控**:
```bash
# 每5分钟运行一次
*/5 * * * * cd /path/to/quants-lab && python scripts/monitor_orderbook_collection.py
```

---

## 🚀 **部署清单**

### **启动前检查**

- [ ] **配置文件更新**: `config/orderbook_snapshot_gateio.yml` → `frequency_seconds: 5` ✅
- [ ] **磁盘空间**: 至少 500 GB 可用空间
- [ ] **并发控制**: `MAX_CONCURRENT = 8` 已设置 ✅
- [ ] **错误处理**: 429 错误重试机制（建议实施）
- [ ] **监控脚本**: `monitor_orderbook_collection.py` 已部署
- [ ] **清理脚本**: 定期清理旧数据（建议7-14天）
- [ ] **告警机制**: 磁盘空间、数据滞后告警

---

## 🔧 **启动命令**

### **测试运行（单次）**

```bash
# 单次采集测试
python cli.py trigger-task \
    --task orderbook_snapshot_gateio \
    --config config/orderbook_snapshot_gateio.yml
```

**预期结果**:
- 24个交易对全部采集成功
- 总耗时 < 4 秒
- 无 429 错误

---

### **生产运行（持续）**

```bash
# 后台持续运行
nohup python cli.py run-tasks \
    --config config/orderbook_snapshot_gateio.yml \
    > logs/orderbook_collection.log 2>&1 &

# 查看日志
tail -f logs/orderbook_collection.log
```

---

## 📊 **预期性能指标**

### **正常运行状态**

| 指标 | 目标值 | 告警阈值 |
|------|--------|---------|
| **采集成功率** | >99% | <95% |
| **数据滞后** | <10秒 | >30秒 |
| **周期耗时** | <4秒 | >4.5秒 |
| **429错误率** | 0% | >1% |
| **磁盘增长** | ~8.3GB/天 | >10GB/天 |

---

## ⚡ **性能优化建议**

### **如果遇到性能问题**

1. **减少并发数**
   ```python
   MAX_CONCURRENT = 6  # 从8降到6
   ```

2. **增加请求间隔**
   ```python
   await asyncio.sleep(0.2)  # 从0.1秒增加到0.2秒
   ```

3. **分批执行**
   - 将24个交易对分为3批
   - 每批8个，批次间延迟1.5秒

4. **减少订单簿深度**
   ```yaml
   depth_limit: 50  # 从100降到50档
   ```

---

## 🎯 **最佳实践**

### **运行前**

1. ✅ 确认磁盘空间充足（>500GB）
2. ✅ 测试单次采集成功
3. ✅ 设置监控和告警

### **运行中**

1. ✅ 每小时检查日志中的429错误
2. ✅ 每天检查磁盘空间
3. ✅ 监控数据滞后情况

### **运行后**

1. ✅ 定期清理旧数据（7-14天）
2. ✅ 分析采集成功率
3. ✅ 优化性能瓶颈

---

## 🔄 **回滚方案**

如果5秒频率导致问题：

### **方案1: 降低到10秒**

```yaml
schedule:
  frequency_seconds: 10  # 从5秒降到10秒
```

**影响**:
- 存储减少50%
- API压力减少50%
- 仍适合高频交易

### **方案2: 降低到30秒**

```yaml
schedule:
  frequency_seconds: 30  # 从5秒降到30秒
```

**影响**:
- 存储减少83%
- API压力减少83%
- 适合中频交易

---

## 📞 **问题排查**

### **常见问题**

#### **Q1: 频繁出现429错误**

**解决方案**:
1. 增加并发控制延迟
2. 减少 `MAX_CONCURRENT` 到 6
3. 增加批次间延迟到 2 秒

#### **Q2: 数据滞后严重（>1分钟）**

**解决方案**:
1. 检查网络连接
2. 检查Gate.io API状态
3. 增加请求超时时间

#### **Q3: 磁盘空间快速耗尽**

**解决方案**:
1. 立即执行清理脚本
2. 减少保留天数（7天 → 3天）
3. 考虑降低采集频率

---

## 🎊 **总结**

### ✅ **5秒采集频率适合你的场景**

**理由**:
- ✅ 秒级高频交易需求
- ✅ API限流安全（4.8次/秒）
- ✅ 并发控制已实施
- ⚠️ 需要充足存储空间（500GB+）
- ⚠️ 需要严格监控

### **关键成功因素**

1. **严格的并发控制**（Semaphore = 8）
2. **完善的错误处理**（429重试机制）
3. **充足的磁盘空间**（500GB+）
4. **实时监控告警**（每5分钟检查）
5. **定期数据清理**（7-14天）

---

## 📁 **相关文档**

- [订单簿采集指南](ORDERBOOK_COLLECTION_GUIDE.md)
- [Gate.io API限流策略](GATEIO_API_RATE_LIMITS.md)
- [订单簿采集频率分析](ORDERBOOK_SAMPLING_FREQUENCY_GUIDE.md)

---

**🎯 配置已更新到5秒，你可以开始测试运行了！** ⚡

**记得密切监控前24小时的运行情况！** 🔍

