"""
CEX交易对到DEX池子的映射任务

这个任务自动将CEX交易对映射到DEX的高流动性池子，使用GeckoTerminal API搜索。
"""
import logging
from typing import Dict, Any
from datetime import datetime, timezone

from core.tasks import BaseTask, TaskContext
from core.services.pool_mapping import PoolMappingService
from core.data_paths import data_paths

logging.basicConfig(level=logging.INFO)


class PoolMappingTask(BaseTask):
    """CEX交易对到DEX池子的映射任务"""
    
    def __init__(self, config):
        super().__init__(config)
        
        # 从config读取参数（使用.get()提供默认值）
        task_config = self.config.config
        self.network = task_config.get("network", "base")
        self.connector = task_config.get("connector", "gate_io")
        self.trading_pairs = task_config.get("trading_pairs", None)  # None=自动检测
        self.top_n = task_config.get("top_n", 3)
        self.output_path = task_config.get("output_path", None)  # None=使用默认
        
        # 服务实例（在setup中初始化）
        self.service = None
        
    async def setup(self, context: TaskContext) -> None:
        """任务初始化"""
        await super().setup(context)
        
        # 初始化服务
        self.service = PoolMappingService()
        
        # 验证配置
        if not self.network:
            raise RuntimeError("network not configured")
        if not self.connector:
            raise RuntimeError("connector not configured")
            
        logging.info(f"Setup completed for {context.task_name}")
        logging.info(f"Network: {self.network}")
        logging.info(f"Connector: {self.connector}")
        logging.info(f"Top N: {self.top_n}")
        
    async def cleanup(self, context: TaskContext, result) -> None:
        """资源清理"""
        await super().cleanup(context, result)
        logging.info(f"Cleanup completed for {context.task_name}")
        
    async def execute(self, context: TaskContext) -> Dict[str, Any]:
        """主执行逻辑"""
        start_time = datetime.now(timezone.utc)
        logging.info(f"Starting pool mapping for {self.connector} on {self.network}")
        
        try:
            # 1. 获取交易对列表
            if self.trading_pairs:
                pairs = self.trading_pairs
                logging.info(f"Using configured pairs: {len(pairs)} pairs")
            else:
                pairs = self.service.parse_trading_pairs_from_candles(
                    data_paths.candles_dir,
                    connector=self.connector
                )
                logging.info(f"Auto-detected pairs: {len(pairs)} pairs")
            
            if not pairs:
                raise RuntimeError(f"No trading pairs found for {self.connector}")
            
            # 2. 构建映射
            df, raw_responses = await self.service.build_mapping(
                pairs, self.network, self.connector, self.top_n
            )
            
            # 3. 保存结果（使用data_paths）
            self.service.save_raw_responses(raw_responses, self.network)
            output_file = self.service.save_mapping(df, self.network, self.connector)
            
            # 4. 统计信息
            pools_found = len(df)
            pairs_with_pools = df['trading_pair'].nunique() if not df.empty else 0
            pairs_failed = len(pairs) - pairs_with_pools
            
            # 5. 准备返回结果
            duration = datetime.now(timezone.utc) - start_time
            result = {
                "status": "completed",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "execution_id": context.execution_id,
                "network": self.network,
                "connector": self.connector,
                "output_file": str(output_file),
                "stats": {
                    "pairs_total": len(pairs),
                    "pairs_with_pools": pairs_with_pools,
                    "pairs_failed": pairs_failed,
                    "pools_found": pools_found,
                    "top_n": self.top_n
                },
                "duration_seconds": duration.total_seconds()
            }
            
            logging.info(f"Pool mapping completed: {result['stats']}")
            return result
            
        except Exception as e:
            logging.error(f"Error executing pool mapping task: {e}")
            raise
    
    async def on_success(self, context: TaskContext, result) -> None:
        """成功回调"""
        stats = result.result_data.get("stats", {})
        logging.info(f"✓ PoolMappingTask succeeded in {result.duration_seconds:.2f}s")
        logging.info(f"  - Pairs: {stats.get('pairs_with_pools', 0)}/{stats.get('pairs_total', 0)}")
        logging.info(f"  - Pools found: {stats.get('pools_found', 0)}")
    
    async def on_failure(self, context: TaskContext, result) -> None:
        """失败回调"""
        logging.error(f"✗ PoolMappingTask failed: {result.error_message}")
        logging.error(f"  Execution ID: {context.execution_id}")
    
    async def on_retry(self, context: TaskContext, attempt: int, error: Exception) -> None:
        """重试回调"""
        logging.warning(f"🔄 PoolMappingTask retry attempt {attempt}: {error}")

