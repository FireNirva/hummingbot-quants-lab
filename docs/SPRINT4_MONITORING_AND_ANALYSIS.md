# 🚀 Sprint 4: 数据监控与分析系统

## 📋 总览

**目标**：在 Sprint 3 成功完成双交易所数据收集的基础上，建立完整的数据监控和分析能力。

**开始时间**：2025-11-19  
**预计周期**：5-7 天  
**优先级**：高  
**依赖**：Sprint 3（✅ 已完成）

---

## 🎯 Sprint 3 回顾

### 已完成功能

| 功能 | 交易所 | 状态 | 数据量 |
|------|--------|------|--------|
| **WebSocket 实时收集** | Gate.io | ✅ | 1,191+ 文件 |
| **WebSocket 实时收集** | MEXC | ✅ | 25+ 文件 |
| **REST 快照收集** | 两所 | ✅ | 多个文件 |
| **数据完整性保护** | 全部 | ✅ | 文档完善 |
| **Protobuf 支持** | MEXC | ✅ | 已实现 |

### 当前系统能力

```
✅ 数据收集：双交易所，12个交易对
✅ 实时性：100ms (Gate.io), 60s (MEXC)
✅ 数据格式：Parquet (columnar, compressed)
✅ 存储策略：分区、多 part 文件
✅ 容错机制：缓冲、自动刷新、优雅关闭
✅ 文档完整：85个技术文档
```

### 系统规模

```
总文件数：1,234 个 Parquet 文件
数据量：近 10 万条 ticks
存储占用：9.1 MB
运行时间：累计 20+ 小时
稳定性：0 崩溃，0 数据损坏
```

---

## 🎯 Sprint 4 目标

### 核心任务

基于 Sprint 3 总结的建议，Sprint 4 将实现三大核心功能：

1. **数据质量监控 Dashboard** 📊
2. **套利分析工具** 💰
3. **性能优化** ⚡

### 预期成果

- ✅ 实时监控数据收集状态
- ✅ 自动检测数据质量问题
- ✅ 跨交易所价差分析
- ✅ 套利机会识别与告警
- ✅ 存储和查询性能优化

---

## 📊 任务 1：数据质量监控 Dashboard

### 1.1 目标

建立一个轻量级的监控系统，实时跟踪数据收集状态和质量。

### 1.2 功能需求

#### 核心监控指标

| 指标 | 描述 | 告警阈值 |
|------|------|---------|
| **数据新鲜度** | 最后更新时间 | > 5 分钟 |
| **文件完整性** | 损坏文件检测 | > 0 个 |
| **采集速率** | 每分钟新增记录数 | < 预期的 50% |
| **存储空间** | 磁盘使用情况 | > 80% |
| **进程状态** | 任务运行状态 | 进程停止 |
| **序列号间隙** | update_id 缺失 | > 100 |

#### Dashboard 界面

```
╔══════════════════════════════════════════════════════════════╗
║           📊 Orderbook 数据收集监控 Dashboard              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🟢 Gate.io WebSocket                      ✅ 运行中        ║
║     VIRTUAL-USDT    │ 最新: 5秒前  │ 今日: 53,086 条      ║
║     IRON-USDT       │ 最新: 3秒前  │ 今日: 8,189 条       ║
║     ...                                                      ║
║                                                              ║
║  🟢 MEXC WebSocket                         ✅ 运行中        ║
║     AUKIUSDT        │ 最新: 2分钟前 │ 今日: 4,613 条       ║
║     IRONUSDT        │ 最新: 2分钟前 │ 今日: 1,001 条       ║
║     ...                                                      ║
║                                                              ║
║  📈 今日统计                                                 ║
║     总记录数: 95,588           平均延迟: 0.5ms             ║
║     存储占用: 9.1 MB           文件数: 1,234              ║
║     运行时长: 5小时23分         健康度: 100%              ║
║                                                              ║
║  ⚠️  告警 (0)                                               ║
║     无告警                                                   ║
╚══════════════════════════════════════════════════════════════╝

最后更新: 2025-11-19 09:30:15
```

### 1.3 技术方案

#### 方案 A：命令行 Dashboard（推荐 - 快速实现）

**优点**：
- ✅ 实现简单（1天）
- ✅ 无额外依赖
- ✅ 适合服务器环境
- ✅ 低资源消耗

**技术栈**：
```python
import curses  # 终端 UI
import psutil  # 进程监控
import pandas  # 数据读取
```

**实现**：
```bash
# 启动监控
python scripts/monitor_dashboard.py

# 或后台运行，定期输出
python scripts/monitor_dashboard.py --log --interval 60
```

#### 方案 B：Web Dashboard（可选 - 功能丰富）

**优点**：
- ✅ 界面友好
- ✅ 远程访问
- ✅ 图表可视化
- ⚠️ 实现复杂（3天）

**技术栈**：
```python
Flask / FastAPI  # Web 框架
Plotly / Dash    # 图表库
```

### 1.4 实施步骤

**Phase 1：基础监控（1天）**

```python
# scripts/monitor_dashboard.py
class DataQualityMonitor:
    def check_data_freshness(self) -> Dict[str, int]:
        """检查每个交易对的数据新鲜度（秒）"""
        
    def check_file_integrity(self) -> List[str]:
        """检查损坏的文件列表"""
        
    def check_process_status(self) -> Dict[str, bool]:
        """检查采集进程状态"""
        
    def get_collection_stats(self) -> Dict:
        """获取采集统计数据"""
```

**Phase 2：告警系统（1天）**

```python
class AlertManager:
    def check_alerts(self) -> List[Alert]:
        """检查所有告警条件"""
        
    def send_notification(self, alert: Alert):
        """发送告警通知（邮件/Telegram/日志）"""
```

**Phase 3：Dashboard UI（1天）**

```python
# 命令行版本
def render_dashboard(stats: Dict):
    """使用 curses 渲染终端 Dashboard"""
    
# 或 Web 版本（可选）
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', stats=get_stats())
```

### 1.5 可交付成果

- ✅ `scripts/monitor_dashboard.py` - 监控主程序
- ✅ `scripts/alert_manager.py` - 告警管理器
- ✅ `docs/MONITORING_GUIDE.md` - 使用文档
- ✅ 配置文件：`config/monitoring.yml`

---

## 💰 任务 2：套利分析工具

### 2.1 目标

开发跨交易所价差分析和套利机会识别系统。

### 2.2 功能需求

#### 核心分析功能

1. **实时价差监控**
   - 计算 Gate.io vs MEXC 的价差
   - 识别套利机会（价差 > 阈值）
   - 考虑交易费用和滑点

2. **历史套利回测**
   - 分析历史数据中的套利机会
   - 计算潜在收益
   - 评估机会频率

3. **套利策略模拟**
   - 模拟资金流动
   - 计算实际收益率
   - 考虑资金占用成本

#### 分析指标

| 指标 | 计算公式 | 说明 |
|------|---------|------|
| **价差百分比** | `(P_mexc - P_gate) / P_gate * 100` | 基础价差 |
| **净价差** | 价差 - 手续费 - 滑点 | 实际可获利空间 |
| **套利收益率** | `净价差 / 资金 * 100` | ROI |
| **年化收益率** | `收益率 * 365 / 持有天数` | 年化 ROI |

### 2.3 技术方案

#### 数据对齐策略

```python
def align_orderbook_data(gate_df, mexc_df):
    """
    对齐两个交易所的时间序列数据
    
    策略：
    - Gate.io: 100ms 实时数据
    - MEXC: 60s 快照数据
    - 对齐方法：向前填充（forward fill）
    """
    # 合并时间序列
    combined = pd.merge_asof(
        gate_df.sort_values('timestamp'),
        mexc_df.sort_values('timestamp'),
        on='timestamp',
        direction='backward',  # 使用最近的 MEXC 数据
        tolerance=pd.Timedelta('60s')  # 最大容忍度
    )
    return combined
```

#### 套利机会识别

```python
def identify_arbitrage_opportunities(combined_df, threshold=0.5):
    """
    识别套利机会
    
    Args:
        combined_df: 对齐后的数据
        threshold: 最小价差阈值（百分比）
    
    Returns:
        DataFrame with arbitrage opportunities
    """
    # 计算价差
    combined_df['spread_pct'] = (
        (combined_df['mexc_mid'] - combined_df['gate_mid']) / 
        combined_df['gate_mid'] * 100
    )
    
    # 考虑费用
    combined_df['net_spread'] = (
        combined_df['spread_pct'] - 
        GATE_FEE - MEXC_FEE - SLIPPAGE
    )
    
    # 过滤机会
    opportunities = combined_df[
        combined_df['net_spread'] > threshold
    ]
    
    return opportunities
```

### 2.4 实施步骤

**Phase 1：数据加载与对齐（1天）**

```python
# scripts/arbitrage_analyzer.py
class ArbitrageAnalyzer:
    def load_orderbook_data(self, symbol, date):
        """加载 Gate.io 和 MEXC 的订单簿数据"""
        
    def align_timestamps(self, gate_df, mexc_df):
        """时间对齐"""
```

**Phase 2：套利计算（1天）**

```python
    def calculate_spread(self, combined_df):
        """计算价差"""
        
    def identify_opportunities(self, threshold=0.5):
        """识别套利机会"""
        
    def calculate_potential_profit(self, opportunity, capital):
        """计算潜在收益"""
```

**Phase 3：可视化与报告（1天）**

```python
    def plot_spread_timeline(self):
        """绘制价差时间序列图"""
        
    def generate_report(self, date):
        """生成每日套利分析报告"""
```

### 2.5 使用示例

```python
from scripts.arbitrage_analyzer import ArbitrageAnalyzer

# 初始化分析器
analyzer = ArbitrageAnalyzer()

# 加载数据
analyzer.load_orderbook_data(
    symbol="IRON",
    date="20251119"
)

# 识别机会
opportunities = analyzer.identify_opportunities(
    threshold=0.5,  # 最小净价差 0.5%
    min_duration=5   # 持续至少 5 秒
)

print(f"发现 {len(opportunities)} 个套利机会")
print(f"平均净价差: {opportunities['net_spread'].mean():.2f}%")
print(f"最大净价差: {opportunities['net_spread'].max():.2f}%")

# 生成报告
analyzer.generate_report(date="20251119")
```

### 2.6 可交付成果

- ✅ `scripts/arbitrage_analyzer.py` - 套利分析器
- ✅ `scripts/generate_arbitrage_report.py` - 报告生成器
- ✅ `docs/ARBITRAGE_ANALYSIS_GUIDE.md` - 使用文档
- ✅ 示例 Jupyter Notebook

---

## ⚡ 任务 3：性能优化

### 3.1 目标

优化数据存储、查询性能和磁盘空间使用。

### 3.2 优化方向

#### 3.2.1 存储空间优化

**当前状态**：
- 总文件：1,234 个
- 占用空间：9.1 MB
- 压缩方式：Snappy

**优化目标**：
- 减少 20-30% 存储空间
- 加快压缩/解压速度

**方案**：

```python
# 方案 A：更激进的压缩
pq.write_table(
    table,
    part_path,
    compression='zstd',  # 改用 zstd（更好的压缩比）
    compression_level=3,  # 平衡压缩比和速度
    use_dictionary=True
)

# 方案 B：数据类型优化
schema = pa.schema([
    ('timestamp', pa.timestamp('us', tz='UTC')),
    ('price', pa.decimal128(18, 8)),  # 使用 decimal 而不是 float
    ('amount', pa.decimal128(18, 8)),
    ('side', pa.dictionary(pa.int8(), pa.string())),  # 字典编码
])
```

#### 3.2.2 查询性能优化

**当前状态**：
- 查询方式：加载全部 parquet 文件
- 无索引
- 无分区优化

**优化目标**：
- 加快数据加载速度 50%
- 支持高效的时间范围查询

**方案**：

```python
# 方案 A：使用 PyArrow Dataset API
import pyarrow.dataset as ds

dataset = ds.dataset(
    'app/data/raw/orderbook_ticks',
    format='parquet',
    partitioning=ds.partitioning(
        pa.schema([
            ('exchange', pa.string()),
            ('symbol', pa.string()),
            ('date', pa.string())
        ])
    )
)

# 高效过滤查询
filtered = dataset.to_table(
    columns=['timestamp', 'price', 'amount'],
    filter=(
        (ds.field('exchange') == 'gate_io') &
        (ds.field('symbol') == 'VIRTUAL-USDT') &
        (ds.field('date') == '20251119') &
        (ds.field('timestamp') >= start_time) &
        (ds.field('timestamp') <= end_time)
    )
)
```

```python
# 方案 B：创建索引文件
class OrderbookIndex:
    def build_index(self, base_dir):
        """
        为每个分区创建元数据索引
        
        索引内容：
        - 文件路径
        - 时间范围
        - 记录数
        - 文件大小
        """
        
    def query_with_index(self, filters):
        """使用索引快速定位相关文件"""
```

#### 3.2.3 数据归档策略

**目标**：管理长期数据存储

**方案**：

```python
class DataArchiver:
    def archive_old_data(self, days=30):
        """
        归档超过 N 天的数据
        
        策略：
        1. 合并多个 part 文件为单个文件
        2. 使用更高压缩率
        3. 移动到归档目录
        """
        
    def clean_old_data(self, days=90):
        """删除超过 N 天的数据"""
```

### 3.3 实施步骤

**Phase 1：基准测试（0.5天）**

```python
# scripts/benchmark_storage.py
def benchmark_compression():
    """测试不同压缩算法的性能"""
    
def benchmark_query():
    """测试查询性能"""
```

**Phase 2：存储优化（1天）**

```python
# 更新 tick_orderbook_writer.py
def write_with_optimized_compression():
    """使用优化的压缩设置"""
```

**Phase 3：查询优化（1天）**

```python
# core/data_sources/orderbook_index.py
class OrderbookIndex:
    """订单簿数据索引"""
```

**Phase 4：归档工具（0.5天）**

```python
# scripts/archive_old_data.py
def archive_data(days=30):
    """归档旧数据"""
```

### 3.4 可交付成果

- ✅ `scripts/benchmark_storage.py` - 性能基准测试
- ✅ `scripts/archive_old_data.py` - 数据归档工具
- ✅ `core/data_sources/orderbook_index.py` - 数据索引
- ✅ `docs/PERFORMANCE_OPTIMIZATION.md` - 优化文档

---

## 📅 实施计划

### 时间表

| 任务 | 子任务 | 工作量 | 开始日期 | 结束日期 | 状态 |
|------|--------|--------|---------|---------|------|
| **任务1** | 基础监控 | 1天 | Day 1 | Day 1 | ⏳ |
| | 告警系统 | 1天 | Day 2 | Day 2 | ⏳ |
| | Dashboard UI | 1天 | Day 3 | Day 3 | ⏳ |
| **任务2** | 数据对齐 | 1天 | Day 2 | Day 2 | ⏳ |
| | 套利计算 | 1天 | Day 3 | Day 3 | ⏳ |
| | 可视化报告 | 1天 | Day 4 | Day 4 | ⏳ |
| **任务3** | 基准测试 | 0.5天 | Day 4 | Day 4 | ⏳ |
| | 存储优化 | 1天 | Day 5 | Day 5 | ⏳ |
| | 查询优化 | 1天 | Day 6 | Day 6 | ⏳ |
| | 归档工具 | 0.5天 | Day 7 | Day 7 | ⏳ |
| **总计** | | **7天** | | | |

### 优先级排序

#### P0 - 必须完成（核心功能）

1. ✅ 基础数据监控
2. ✅ 文件完整性检查
3. ✅ 基础套利分析

#### P1 - 应该完成（重要功能）

4. ✅ 告警系统
5. ✅ 套利报告生成
6. ✅ 存储压缩优化

#### P2 - 可选（增强功能）

7. ⭕ Web Dashboard
8. ⭕ 实时套利告警
9. ⭕ 查询性能优化

---

## 🎯 成功标准

### 定量指标

| 指标 | 当前 | 目标 | 测量方法 |
|------|------|------|---------|
| **监控延迟** | N/A | < 5秒 | Dashboard 更新时间 |
| **告警准确率** | N/A | > 95% | 准确告警/总告警 |
| **套利识别** | N/A | > 10个/天 | 发现的机会数 |
| **查询速度** | 基准 | -50% | 查询耗时 |
| **存储空间** | 9.1MB | -30% | 磁盘占用 |

### 定性标准

- ✅ 监控系统稳定运行 24 小时无故障
- ✅ 套利分析结果准确可靠
- ✅ 文档完整，示例齐全
- ✅ 代码质量高，易于维护

---

## 🛠️ 技术选型

### 推荐技术栈

| 组件 | 技术选择 | 原因 |
|------|---------|------|
| **监控 UI** | curses (Python) | 轻量、无依赖、服务器友好 |
| **数据处理** | Pandas + PyArrow | 已有依赖，性能好 |
| **可视化** | Matplotlib | 已有依赖，够用 |
| **压缩** | zstd | 压缩比好，速度快 |
| **告警** | 日志 + 可选邮件 | 简单实用 |

### 可选升级方案

如果需要更丰富的功能：

| 组件 | 升级选择 | 额外工作量 |
|------|---------|-----------|
| **Web Dashboard** | Flask + Plotly | +2天 |
| **实时告警** | Telegram Bot | +1天 |
| **数据库** | TimescaleDB | +2天 |

---

## 📚 文档计划

### 需要创建的文档

1. **MONITORING_GUIDE.md**
   - 监控系统使用说明
   - 告警配置指南
   - 故障排查

2. **ARBITRAGE_ANALYSIS_GUIDE.md**
   - 套利分析工具使用
   - 策略参数配置
   - 回测方法

3. **PERFORMANCE_OPTIMIZATION.md**
   - 性能优化技巧
   - 存储管理
   - 查询优化

4. **SPRINT4_IMPLEMENTATION_LOG.md**
   - 实施过程记录
   - 遇到的问题和解决方案
   - 经验教训

---

## 🚨 风险与应对

### 潜在风险

| 风险 | 概率 | 影响 | 应对措施 |
|------|------|------|---------|
| **时间估算不足** | 中 | 中 | 优先 P0 功能，P2 可推迟 |
| **性能优化效果不明显** | 低 | 低 | 保留基准测试，逐步优化 |
| **套利分析复杂度高** | 中 | 中 | 从简单分析开始，迭代改进 |

---

## 🎊 预期成果

完成 Sprint 4 后，你将拥有：

### 监控能力

```
✅ 实时数据质量监控
✅ 自动异常检测和告警
✅ 系统健康度评分
✅ 详细的运行统计
```

### 分析能力

```
✅ 跨交易所价差分析
✅ 套利机会识别
✅ 历史数据回测
✅ 收益率计算
```

### 性能提升

```
✅ 存储空间优化 30%
✅ 查询速度提升 50%
✅ 数据归档自动化
✅ 资源使用优化
```

---

## 🚀 启动 Sprint 4

### 准备检查清单

- ✅ Sprint 3 已完成
- ✅ 当前系统运行稳定
- ✅ 有足够的测试数据（✅ 已有 1,234 文件）
- ✅ 开发环境就绪

### 立即开始

```bash
# 1. 创建 Sprint 4 分支（可选）
git checkout -b sprint4-monitoring

# 2. 开始第一个任务：基础监控
python scripts/create_monitor_dashboard.py

# 3. 跟踪进度
# 参考本文档的时间表
```

---

**Sprint 4 - Let's Go! 🚀**

**最后更新**：2025-11-19  
**状态**：✅ 规划完成，等待启动  
**预计完成**：2025-11-26

