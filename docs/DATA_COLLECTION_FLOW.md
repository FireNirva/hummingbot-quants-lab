# 📊 QuantsLab 数据收集流程详解

## 🔄 完整数据流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                     1. 配置文件 (YAML)                            │
│                                                                   │
│  tasks:                                                          │
│    my_task:                                                      │
│      task_class: app.tasks.data_collection....                  │
│      schedule: {...}                                             │
│      config: {...}                                               │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ python cli.py run-tasks
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    2. CLI (cli.py)                                │
│                                                                   │
│  解析命令行参数                                                    │
│  加载环境变量 (.env)                                              │
│  创建 TaskRunner                                                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│            3. TaskRunner (core/tasks/runner.py)                   │
│                                                                   │
│  • 读取 YAML 配置文件                                             │
│  • 创建 TaskConfig 对象                                          │
│  • 导入并实例化任务类                                             │
│  • 初始化 TaskOrchestrator                                       │
│  • 设置 MongoDB Storage                                          │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│       4. TaskOrchestrator (core/tasks/orchestrator.py)            │
│                                                                   │
│  主循环:                                                          │
│  ├─ 检查每个任务的调度条件                                        │
│  ├─ 检查依赖关系                                                  │
│  ├─ 控制并发数量 (Semaphore)                                     │
│  └─ 触发任务执行                                                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│           5. BaseTask.run() (core/tasks/base.py)                  │
│                                                                   │
│  生命周期:                                                        │
│  ┌──────────────────────────────────────────────┐               │
│  │  setup(context)                              │               │
│  │    ↓                                         │               │
│  │  execute(context) ──→ 返回结果               │               │
│  │    ↓         ↓                               │               │
│  │  成功      失败                               │               │
│  │    ↓         ↓                               │               │
│  │  on_success  on_failure → retry?            │               │
│  │    ↓                        ↓                │               │
│  │  cleanup(context, result)   on_retry()       │               │
│  └──────────────────────────────────────────────┘               │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│         6. 具体任务实现 (app/tasks/data_collection/)              │
│                                                                   │
│  例如: CandlesDownloaderTask.execute()                           │
│  ┌──────────────────────────────────────────────┐               │
│  │  1. 计算时间范围                             │               │
│  │  2. 获取交易对列表                           │               │
│  │  3. 遍历交易对和时间间隔                     │               │
│  │  4. 调用 CLOBDataSource.get_candles()       │               │
│  │  5. 统计下载数据                             │               │
│  │  6. 保存缓存到文件                           │               │
│  └──────────────────────────────────────────────┘               │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│           7. CLOBDataSource (core/data_sources/clob.py)           │
│                                                                   │
│  get_candles() 流程:                                             │
│  ┌──────────────────────────────────────────────┐               │
│  │  检查缓存 (cache_key)                        │               │
│  │    ↓                                         │               │
│  │  缓存命中? ──Yes──→ 返回缓存数据             │               │
│  │    ↓ No                                      │               │
│  │  调用交易所 API (Hummingbot Candles Feed)   │               │
│  │    ↓                                         │               │
│  │  数据验证和清洗                              │               │
│  │    ↓                                         │               │
│  │  更新内存缓存 (_candles_cache)               │               │
│  │    ↓                                         │               │
│  │  dump_candles_cache() 写入 Parquet          │               │
│  └──────────────────────────────────────────────┘               │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│          8. 数据持久化 (app/data/)                                │
│                                                                   │
│  app/data/cache/candles/                                         │
│  ├─ binance_perpetual|BTC-USDT|15m.parquet                      │
│  ├─ binance_perpetual|BTC-USDT|1h.parquet                       │
│  ├─ binance_perpetual|ETH-USDT|15m.parquet                      │
│  └─ ...                                                          │
│                                                                   │
│  MongoDB (quants_lab):                                           │
│  ├─ task_executions   (任务执行历史)                             │
│  ├─ pools             (池子筛选结果)                             │
│  └─ ...               (其他集合)                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔍 详细执行流程示例

### 场景: 下载 BTC-USDT 的 15 分钟 K线

#### 步骤 1: 用户执行命令
```bash
python cli.py trigger-task --task btc_downloader --config my_config.yml
```

#### 步骤 2: CLI 初始化
```python
# cli.py
async def trigger_task(task_name: str, config_path: str, timeout: int):
    runner = TaskRunner(config_path=config_path)
    # ... 初始化 orchestrator
    result = await runner.orchestrator.execute_task(
        task_name=task_name,
        force=True
    )
```

#### 步骤 3: TaskRunner 加载配置
```python
# core/tasks/runner.py
def _load_config(self) -> Dict[str, Any]:
    with open(self.config_path, 'r') as f:
        config = yaml.safe_load(f)  # 读取 YAML
    return config

async def _initialize_tasks(self) -> List[BaseTask]:
    for task_name, task_data in self.config["tasks"].items():
        config = self._create_task_config(task_name, task_data)
        task = self._create_task_instance(config)
        tasks.append(task)
```

#### 步骤 4: 创建任务实例
```python
# core/tasks/runner.py
def _create_task_instance(self, config: TaskConfig) -> BaseTask:
    # 导入: app.tasks.data_collection.simple_candles_downloader.SimpleCandlesDownloader
    task_class = self._import_task_class(config.task_class)
    # 实例化
    return task_class(config)  # SimpleCandlesDownloader(config)
```

#### 步骤 5: Orchestrator 执行任务
```python
# core/tasks/orchestrator.py
async def execute_task(self, task_name: str, ...):
    task = self.tasks[task_name]
    
    # 检查是否应该运行
    if not force and not task.should_run_now(last_run):
        return None
    
    # 控制并发
    async with self.task_semaphore:
        # 创建上下文
        context = TaskContext(task_name=task_name)
        
        # 执行任务（包含重试逻辑）
        for attempt in range(1, config.max_retries + 1):
            result = await task.run(context)
            if result.status == TaskStatus.COMPLETED:
                break
```

#### 步骤 6: 任务生命周期
```python
# core/tasks/base.py
async def run(self, context: TaskContext) -> TaskResult:
    # 1. Setup
    await self.setup(context)  # 初始化 MongoDB、通知管理器
    
    # 2. Execute
    result_data = await self.execute(context)  # 调用子类实现
    
    # 3. Success/Failure
    if success:
        await self.on_success(context, result)
    else:
        await self.on_failure(context, result)
    
    # 4. Cleanup
    await self.cleanup(context, result)
    
    return result
```

#### 步骤 7: 执行具体业务逻辑
```python
# app/tasks/data_collection/simple_candles_downloader.py
async def execute(self, context: TaskContext) -> Dict[str, Any]:
    # 计算时间范围
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=self.days_data_retention)
    
    # 遍历交易对
    for trading_pair in self.trading_pairs:  # ["BTC-USDT"]
        for interval in self.intervals:      # ["15m"]
            # 调用 CLOB 数据源
            candles = await self.clob.get_candles(
                connector_name="binance_perpetual",
                trading_pair="BTC-USDT",
                interval="15m",
                start_time=int(start_time.timestamp()),
                end_time=int(end_time.timestamp())
            )
            
            stats["candles_downloaded"] += len(candles.data)
    
    # 保存到文件
    self.clob.dump_candles_cache()
    
    return {"status": "completed", "stats": stats}
```

#### 步骤 8: CLOBDataSource 处理数据
```python
# core/data_sources/clob.py
async def get_candles(self, connector_name, trading_pair, interval, start_time, end_time):
    cache_key = (connector_name, trading_pair, interval)
    
    # 1. 检查缓存
    if cache_key in self._candles_cache:
        cached_df = self._candles_cache[cache_key]
        if 时间范围在缓存内:
            return 缓存数据
    
    # 2. 加载 Parquet 文件
    parquet_path = f"app/data/cache/candles/{connector_name}|{trading_pair}|{interval}.parquet"
    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
        self._candles_cache[cache_key] = df
    
    # 3. 调用交易所 API
    candles_config = CandlesConfig(
        connector=connector_name,
        trading_pair=trading_pair,
        interval=interval
    )
    candles = await self.candles_factory.get_candles(candles_config)
    
    # 4. 合并数据
    if cache_key in self._candles_cache:
        # 合并新旧数据
        merged_df = pd.concat([cached_df, new_df]).drop_duplicates()
    else:
        merged_df = new_df
    
    # 5. 更新缓存
    self._candles_cache[cache_key] = merged_df
    
    return Candles(candles_df=merged_df, ...)

def dump_candles_cache(self):
    # 保存所有缓存的数据到 Parquet 文件
    for cache_key, df in self._candles_cache.items():
        connector, pair, interval = cache_key
        filename = f"{connector}|{pair}|{interval}.parquet"
        filepath = f"app/data/cache/candles/{filename}"
        df.to_parquet(filepath)
```

#### 步骤 9: 结果返回和存储
```python
# core/tasks/orchestrator.py
async def execute_task(...):
    result = await task.run(context)
    
    # 保存执行结果到 MongoDB
    await self.storage.save_execution(result)
    
    # 触发依赖任务
    if result.status == TaskStatus.COMPLETED:
        await self._trigger_dependent_tasks(task_name, result)
    
    return result
```

---

## 📊 数据存储结构

### Parquet 文件结构
```
app/data/cache/candles/
├── binance_perpetual|BTC-USDT|15m.parquet
│   └── 列: timestamp, open, high, low, close, volume, ...
├── binance_perpetual|BTC-USDT|1h.parquet
└── binance_perpetual|ETH-USDT|15m.parquet
```

**Parquet 文件内容示例**:
```
   timestamp        open     high      low    close      volume
0  1704067200.0  42150.5  42200.0  42100.0  42180.0   1234.567
1  1704067800.0  42180.0  42250.0  42150.0  42230.0   1456.789
2  1704068400.0  42230.0  42300.0  42200.0  42280.0   1678.901
...
```

### MongoDB 存储结构

**集合: task_executions**
```json
{
  "_id": ObjectId("..."),
  "execution_id": "uuid-string",
  "task_name": "btc_downloader",
  "status": "completed",
  "started_at": ISODate("2024-01-01T00:00:00Z"),
  "completed_at": ISODate("2024-01-01T00:10:00Z"),
  "duration_seconds": 600,
  "result_data": {
    "status": "completed",
    "stats": {
      "pairs_processed": 1,
      "candles_downloaded": 2880
    }
  },
  "error_message": null
}
```

**集合: pools**
```json
{
  "_id": ObjectId("..."),
  "timestamp": ISODate("2024-01-01T00:00:00Z"),
  "execution_id": "uuid-string",
  "trending_pools": [
    {
      "name": "SOL/USDC",
      "address": "pool-address",
      "fdv_usd": 125000,
      "volume_usd_h24": 250000,
      "reserve_in_usd": 80000,
      "volume_liquidity_ratio": 3.125
    }
  ],
  "filtered_trending_pools": [...]
}
```

---

## 🔗 关键组件交互图

```
                    ┌──────────────┐
                    │   用户命令    │
                    └──────┬───────┘
                           │
                           ▼
           ┌───────────────────────────────┐
           │        CLI (cli.py)            │
           │  • 解析参数                    │
           │  • 加载环境变量                │
           └───────────────┬───────────────┘
                           │
                           ▼
           ┌───────────────────────────────┐
           │      TaskRunner               │
           │  • 加载 YAML                  │
           │  • 创建任务实例                │
           └───────────────┬───────────────┘
                           │
                           ▼
           ┌───────────────────────────────┐
           │    TaskOrchestrator           │
           │  • 任务调度                    │
           │  • 依赖管理                    │
           │  • 并发控制                    │
           └───────────────┬───────────────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
    ┌─────────────────┐    ┌─────────────────┐
    │  MongoStorage   │    │    BaseTask     │
    │  • 保存状态     │◄───│  • setup()      │
    │  • 查询历史     │    │  • execute()    │
    └─────────────────┘    │  • cleanup()    │
                           └────────┬────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │  具体任务实现              │
                    │  • CandlesDownloader      │
                    │  • PoolsScreener          │
                    └───────────┬───────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
        ┌──────────────────┐    ┌──────────────────┐
        │ CLOBDataSource   │    │ GeckoTerminal    │
        │ • get_candles()  │    │ • get_pools()    │
        │ • 缓存管理       │    │ • 数据筛选       │
        └────────┬─────────┘    └────────┬─────────┘
                 │                       │
                 ▼                       ▼
        ┌──────────────────┐    ┌──────────────────┐
        │  Parquet Files   │    │     MongoDB      │
        │  (K线数据)       │    │  (池子/执行历史) │
        └──────────────────┘    └──────────────────┘
```

---

## 💡 关键设计模式

### 1. 模板方法模式 (Template Method)
BaseTask 定义了任务执行的骨架：
```python
async def run(self):
    await self.setup()      # 子类可选重写
    await self.execute()    # 子类必须实现
    await self.cleanup()    # 子类可选重写
```

### 2. 策略模式 (Strategy)
不同的调度策略：
- FrequencySchedule
- CronSchedule
- DependencyTriggered

### 3. 观察者模式 (Observer)
任务生命周期钩子：
- on_success()
- on_failure()
- on_retry()

### 4. 单例模式 (Singleton)
全局数据路径管理：
```python
from core.data_paths import data_paths
candles_dir = data_paths.candles_dir
```

---

## 🎯 总结

**数据收集流程的核心要点**:

1. **配置驱动**: YAML 文件定义一切
2. **生命周期管理**: Setup → Execute → Cleanup
3. **智能缓存**: Parquet 文件 + 内存缓存
4. **依赖编排**: 任务间自动触发
5. **错误恢复**: 自动重试机制
6. **数据持久化**: 文件 + MongoDB 双重存储

**数据流向**:
```
交易所 API → CLOBDataSource → 内存缓存 → Parquet 文件 → 回测引擎/分析工具
                                    ↓
                              MongoDB 元数据
```

这个系统设计精巧、模块化强、易于扩展！ 🚀

