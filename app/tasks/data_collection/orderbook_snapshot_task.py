"""
订单簿快照采集任务

功能：
- 定期采集交易所订单簿快照
- 支持多个交易对
- 自动存储为 Parquet 格式
- 与 quants-lab 现有架构完全兼容

作者：Alice
日期：2025-11-15
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import aiohttp
import pandas as pd

from core.data_sources import CLOBDataSource
from core.data_paths import data_paths
from core.tasks import BaseTask, TaskContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrderBookSnapshotTask(BaseTask):
    """
    订单簿快照采集任务
    
    配置示例：
    ```yaml
    tasks:
      orderbook_snapshot:
        enabled: true
        task_class: app.tasks.data_collection.orderbook_snapshot_task.OrderBookSnapshotTask
        
        schedule:
          type: frequency
          frequency_minutes: 1  # 每分钟采集一次
        
        config:
          connector_name: "gate_io"
          trading_pairs:
            - "IRON-USDT"
            - "VIRTUAL-USDT"
            - "AERO-USDT"
          depth_limit: 100  # 订单簿深度（档位数）
    ```
    """
    
    def __init__(self, config):
        super().__init__(config)
        
        # 配置参数
        task_config = self.config.config
        self.connector_name = task_config["connector_name"]
        self.trading_pairs = task_config.get("trading_pairs", [])
        self.depth_limit = task_config.get("depth_limit", 100)
        
        # 初始化数据源
        self.clob = CLOBDataSource()
        
        # 确保输出目录存在
        self.output_dir = data_paths.raw_dir / "orderbook_snapshots"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("OrderBookSnapshotTask initialized")
        logger.info(f"  Connector: {self.connector_name}")
        logger.info(f"  Trading pairs: {len(self.trading_pairs)}")
        logger.info(f"  Depth limit: {self.depth_limit}")
    
    async def setup(self, context: TaskContext) -> None:
        """任务启动前的设置"""
        try:
            await super().setup(context)
            
            # 验证必要参数
            if not self.connector_name:
                raise RuntimeError("connector_name not configured")
            
            if not self.trading_pairs:
                raise RuntimeError("trading_pairs not configured")
            
            # 获取连接器
            try:
                self.connector = self.clob.get_connector(self.connector_name)
                logger.info(f"Connector '{self.connector_name}' initialized successfully")
            except Exception as e:
                raise RuntimeError(f"Failed to initialize connector '{self.connector_name}': {e}")
            
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            raise
    
    async def execute(self, context: TaskContext) -> Dict[str, Any]:
        """
        主执行逻辑：采集订单簿快照
        
        并发控制：使用 Semaphore 限制同时请求数，避免触发 API 限流
        """
        start_time = datetime.now(timezone.utc)
        logger.info(f"Starting orderbook snapshot collection for {len(self.trading_pairs)} pairs")
        
        try:
            stats = {
                "pairs_processed": 0,
                "pairs_total": len(self.trading_pairs),
                "snapshots_collected": 0,
                "errors": 0,
                "start_time": start_time.isoformat(),
            }
            
            # 并发控制：限制同时请求数（避免触发 Gate.io 的10个并发连接限制）
            MAX_CONCURRENT = 8  # 安全值：小于限制，留有余地
            semaphore = asyncio.Semaphore(MAX_CONCURRENT)
            
            async def collect_with_limit(pair):
                """带并发限制的采集包装器"""
                async with semaphore:
                    # 移除延迟以实现更精确的 5 秒采集间隔
                    # Semaphore 已经提供了足够的并发控制
                    return await self._collect_orderbook_snapshot(pair)
            
            logger.info(f"Using concurrent limit: {MAX_CONCURRENT}")
            
            # 并发采集所有交易对的订单簿（受并发数限制）
            tasks = [
                collect_with_limit(pair)
                for pair in self.trading_pairs
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 统计结果
            for result in results:
                if isinstance(result, Exception):
                    stats["errors"] += 1
                    logger.error(f"Error collecting snapshot: {result}")
                elif result:
                    stats["snapshots_collected"] += 1
                    stats["pairs_processed"] += 1
            
            # 计算执行时长
            end_time = datetime.now(timezone.utc)
            stats["end_time"] = end_time.isoformat()
            stats["duration_seconds"] = (end_time - start_time).total_seconds()
            
            logger.info(f"Orderbook snapshot collection completed: {stats['snapshots_collected']}/{stats['pairs_total']} successful")
            
            return {
                "success": True,
                "stats": stats
            }
            
        except Exception as e:
            logger.error(f"Execute failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _collect_orderbook_snapshot(self, trading_pair: str) -> bool:
        """
        采集单个交易对的订单簿快照（包含 update_id）
        
        Args:
            trading_pair: 交易对（如 "IRON-USDT"）
        
        Returns:
            是否成功
        """
        try:
            logger.debug(f"Collecting orderbook for {trading_pair}")
            
            # 格式化交易对名称（不同交易所格式不同）
            if self.connector_name == "gate_io":
                formatted_pair = trading_pair.replace('-', '_')  # Gate.io: BTC_USDT
            elif self.connector_name == "mexc":
                formatted_pair = trading_pair.replace('-', '')   # MEXC: BTCUSDT
            else:
                formatted_pair = trading_pair.replace('-', '_')  # 默认使用下划线
            
            # 🆕 根据交易所类型调用相应的 API
            orderbook_data = await self._fetch_orderbook(formatted_pair)
            
            if not orderbook_data:
                logger.error(f"Failed to fetch orderbook for {trading_pair}")
                return False
            
            # 提取数据
            timestamp = datetime.now(timezone.utc)
            update_id = orderbook_data.get('id')  # 🆕 Update ID (sequence_number)
            bids = orderbook_data.get('bids', [])
            asks = orderbook_data.get('asks', [])
            
            # 限制深度
            bids = bids[:self.depth_limit]
            asks = asks[:self.depth_limit]
            
            # 构建数据结构（添加 update_id）
            snapshot_data = {
                'timestamp': timestamp,
                'update_id': update_id,  # 🆕 添加 update_id 字段
                'exchange': self.connector_name,
                'trading_pair': trading_pair,
                'best_bid_price': float(bids[0][0]) if bids else None,
                'best_bid_amount': float(bids[0][1]) if bids else None,
                'best_ask_price': float(asks[0][0]) if asks else None,
                'best_ask_amount': float(asks[0][1]) if asks else None,
                'bid_prices': [float(b[0]) for b in bids],
                'bid_amounts': [float(b[1]) for b in bids],
                'ask_prices': [float(a[0]) for a in asks],
                'ask_amounts': [float(a[1]) for a in asks],
            }
            
            # 保存到文件
            await self._save_snapshot(snapshot_data)
            
            logger.debug(f"✅ {trading_pair}: Collected with update_id={update_id}, {len(bids)} bids, {len(asks)} asks")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ {trading_pair}: Failed to collect orderbook: {e}")
            return False
    
    async def _fetch_orderbook(self, formatted_pair: str) -> Optional[Dict]:
        """
        根据交易所类型调用相应的 API 获取订单簿
        
        Args:
            formatted_pair: 格式化后的交易对（如 "BTC_USDT"）
        
        Returns:
            订单簿数据字典，包含 'id', 'bids', 'asks' 等字段
        """
        if self.connector_name == "gate_io":
            return await self._fetch_gateio_orderbook(formatted_pair)
        elif self.connector_name == "mexc":
            return await self._fetch_mexc_orderbook(formatted_pair)
        else:
            logger.error(f"Unsupported exchange: {self.connector_name}")
            return None
    
    async def _fetch_gateio_orderbook(self, formatted_pair: str) -> Optional[Dict]:
        """
        直接调用 Gate.io API 获取订单簿（包含 update_id）
        
        Args:
            formatted_pair: 格式化后的交易对（如 "BTC_USDT"）
        
        Returns:
            订单簿数据字典，包含 'id', 'bids', 'asks' 等字段
        """
        try:
            url = "https://api.gateio.ws/api/v4/spot/order_book"
            params = {
                "currency_pair": formatted_pair,
                "limit": self.depth_limit,
                "with_id": "true"  # 🔑 关键参数：返回 update_id
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status != 200:
                        text = await response.text()
                        logger.error(f"Gate.io API error {response.status}: {text}")
                        return None
                    
                    data = await response.json()
                    
                    # 验证返回数据
                    if 'id' not in data:
                        logger.warning(f"No 'id' field in response for {formatted_pair}")
                    
                    return data
                    
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching orderbook for {formatted_pair}")
            return None
        except Exception as e:
            logger.error(f"Error fetching orderbook for {formatted_pair}: {e}")
            return None
    
    async def _fetch_mexc_orderbook(self, formatted_pair: str) -> Optional[Dict]:
        """
        直接调用 MEXC API 获取订单簿（包含 update_id）
        
        MEXC API 文档: https://mexcdevelop.github.io/apidocs/spot_v3_en/#order-book
        
        Args:
            formatted_pair: 格式化后的交易对（如 "BTCUSDT"，MEXC 不使用下划线）
        
        Returns:
            订单簿数据字典，统一格式与 Gate.io 一致
        """
        try:
            url = "https://api.mexc.com/api/v3/depth"
            params = {
                "symbol": formatted_pair,
                "limit": self.depth_limit
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status != 200:
                        text = await response.text()
                        logger.error(f"MEXC API error {response.status}: {text}")
                        return None
                    
                    data = await response.json()
                    
                    # MEXC 返回格式：
                    # {
                    #   "lastUpdateId": 548631456,  # 相当于 Gate.io 的 'id'
                    #   "bids": [["19549.73", "0.342"], ...],
                    #   "asks": [["19549.74", "0.5"], ...]
                    # }
                    
                    # 统一格式为 Gate.io 风格
                    normalized_data = {
                        'id': data.get('lastUpdateId'),  # MEXC 的序列号
                        'bids': data.get('bids', []),
                        'asks': data.get('asks', [])
                    }
                    
                    if 'lastUpdateId' not in data:
                        logger.warning(f"No 'lastUpdateId' field in MEXC response for {formatted_pair}")
                    
                    return normalized_data
                    
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching orderbook for {formatted_pair}")
            return None
        except Exception as e:
            logger.error(f"Error fetching orderbook for {formatted_pair}: {e}")
            return None
    
    async def _save_snapshot(self, snapshot_data: Dict):
        """
        保存订单簿快照到 Parquet 文件
        
        策略：
        - 每天一个文件（按日期分区）
        - 增量追加模式
        - 使用 Parquet 压缩存储
        """
        try:
            # 生成文件名（按日期分区）
            date_str = snapshot_data['timestamp'].strftime('%Y%m%d')
            filename = f"{self.connector_name}_{snapshot_data['trading_pair']}_{date_str}.parquet"
            filepath = self.output_dir / filename
            
            # 转换为 DataFrame
            df_new = pd.DataFrame([snapshot_data])
            
            # 追加模式：如果文件已存在，读取并合并
            if filepath.exists():
                df_existing = pd.read_parquet(filepath)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df_combined = df_new
            
            # 保存
            df_combined.to_parquet(
                filepath,
                engine='pyarrow',
                compression='snappy',
                index=False
            )
            
        except Exception as e:
            logger.error(f"Failed to save snapshot: {e}")
            raise
    
    async def cleanup(self, context: TaskContext, result) -> None:
        """任务结束后的清理"""
        try:
            await super().cleanup(context, result)
            logger.info("OrderBookSnapshotTask cleanup completed")
        except Exception as e:
            logger.warning(f"Cleanup error: {e}")


# 辅助函数：读取历史订单簿数据
def load_orderbook_snapshots(
    connector_name: str,
    trading_pair: str,
    start_date: str = None,
    end_date: str = None
) -> pd.DataFrame:
    """
    读取历史订单簿快照数据
    
    Args:
        connector_name: 交易所名称
        trading_pair: 交易对
        start_date: 开始日期（格式：YYYYMMDD）
        end_date: 结束日期（格式：YYYYMMDD）
    
    Returns:
        DataFrame with orderbook snapshots
    
    Example:
        >>> df = load_orderbook_snapshots('gate_io', 'IRON-USDT', '20241101', '20241115')
        >>> print(df.head())
    """
    output_dir = data_paths.raw_dir / "orderbook_snapshots"
    
    if not output_dir.exists():
        logger.warning(f"Orderbook snapshots directory not found: {output_dir}")
        return pd.DataFrame()
    
    # 查找匹配的文件
    pattern = f"{connector_name}_{trading_pair}_*.parquet"
    files = list(output_dir.glob(pattern))
    
    if not files:
        logger.warning(f"No orderbook snapshots found for {connector_name} {trading_pair}")
        return pd.DataFrame()
    
    # 过滤日期范围
    if start_date or end_date:
        filtered_files = []
        for file in files:
            date_str = file.stem.split('_')[-1]  # 提取日期部分
            if start_date and date_str < start_date:
                continue
            if end_date and date_str > end_date:
                continue
            filtered_files.append(file)
        files = filtered_files
    
    # 读取并合并所有文件
    dfs = []
    for file in sorted(files):
        df = pd.read_parquet(file)
        dfs.append(df)
    
    if not dfs:
        return pd.DataFrame()
    
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # 按时间排序
    if 'timestamp' in combined_df.columns:
        combined_df = combined_df.sort_values('timestamp')
    
    logger.info(f"Loaded {len(combined_df)} orderbook snapshots from {len(files)} files")
    
    return combined_df


def validate_update_ids(df: pd.DataFrame) -> Dict[str, Any]:
    """
    验证订单簿数据的 update_id 完整性
    
    Args:
        df: 订单簿 DataFrame（必须包含 'update_id' 列）
    
    Returns:
        验证报告字典，包含：
        - total_records: 总记录数
        - null_count: update_id 为空的记录数
        - non_increasing: update_id 未递增的位置
        - duplicates: 重复的 update_id
        - quality_score: 数据质量评分 (0-100)
    
    Example:
        >>> df = load_orderbook_snapshots('gate_io', 'IRON-USDT')
        >>> report = validate_update_ids(df)
        >>> print(f"质量评分: {report['quality_score']:.1f}/100")
    """
    report = {
        'total_records': len(df),
        'null_count': 0,
        'non_increasing': [],
        'duplicates': [],
        'quality_score': 100.0
    }
    
    if 'update_id' not in df.columns:
        report['error'] = 'No update_id column found'
        report['quality_score'] = 0
        logger.error("❌ DataFrame does not contain 'update_id' column")
        return report
    
    # 检查 null 值
    null_count = df['update_id'].isna().sum()
    if null_count > 0:
        report['null_count'] = int(null_count)
        report['quality_score'] -= (null_count / len(df)) * 50
        logger.warning(f"⚠️ Found {null_count} null update_id values")
    
    # 过滤有效的 update_id
    df_valid = df.dropna(subset=['update_id']).copy()
    
    if len(df_valid) < 2:
        logger.warning("⚠️ Not enough valid records to validate")
        return report
    
    # 检查递增性（Gate.io REST API 的 update_id 应该递增但不一定连续）
    for i in range(1, len(df_valid)):
        current_id = df_valid.iloc[i]['update_id']
        prev_id = df_valid.iloc[i-1]['update_id']
        
        if current_id <= prev_id:
            issue_type = 'equal' if current_id == prev_id else 'decreasing'
            report['non_increasing'].append({
                'index': i,
                'timestamp': str(df_valid.iloc[i]['timestamp']),
                'prev_id': int(prev_id),
                'current_id': int(current_id),
                'issue': issue_type
            })
    
    # 检查重复
    duplicate_mask = df_valid.duplicated(subset=['update_id'], keep=False)
    if duplicate_mask.any():
        duplicates = df_valid[duplicate_mask][['timestamp', 'update_id', 'trading_pair']]
        report['duplicates'] = duplicates.to_dict('records')
        logger.warning(f"⚠️ Found {len(duplicates)} duplicate update_id values")
    
    # 计算质量评分
    issue_count = len(report['non_increasing']) + len(report['duplicates'])
    if issue_count > 0:
        penalty = min(50, (issue_count / len(df_valid)) * 100)
        report['quality_score'] -= penalty
        logger.warning(f"⚠️ Quality score: {report['quality_score']:.1f}/100 ({issue_count} issues)")
    else:
        logger.info(f"✅ Data quality excellent: {report['quality_score']:.1f}/100")
    
    return report

