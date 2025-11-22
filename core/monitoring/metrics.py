"""
Prometheus Metrics Registry for Orderbook Collection

提供统一的指标注册和管理，支持数据收集任务的监控。

Author: Alice
Date: 2025-11-22
"""

from prometheus_client import Counter, Gauge, Histogram, CollectorRegistry, REGISTRY
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class OrderbookMetrics:
    """
    Orderbook数据收集的指标注册表
    
    提供统一的Prometheus指标定义和辅助方法。
    
    使用示例：
        metrics = get_metrics()
        metrics.increment_messages_received("gate_io", "BTC-USDT", "diff")
        metrics.observe_processing_latency("gate_io", "BTC-USDT", 0.005)
    """
    
    def __init__(self, registry: Optional[CollectorRegistry] = None):
        """
        初始化指标注册表
        
        Args:
            registry: 自定义注册表（默认使用全局默认注册表）
        """
        # 如果没有指定registry，使用全局默认REGISTRY
        if registry is None:
            registry = REGISTRY
        self.registry = registry
        
        # === 数据收集指标 ===
        
        self.messages_received = Counter(
            'orderbook_collector_messages_received_total',
            'WebSocket接收的消息总数',
            ['exchange', 'symbol', 'message_type'],
            registry=registry
        )
        
        self.messages_processed = Counter(
            'orderbook_collector_messages_processed_total',
            '成功处理的消息总数',
            ['exchange', 'symbol'],
            registry=registry
        )
        
        self.messages_failed = Counter(
            'orderbook_collector_messages_failed_total',
            '处理失败的消息总数',
            ['exchange', 'symbol', 'error_type'],
            registry=registry
        )
        
        self.sequence_gaps = Counter(
            'orderbook_collector_sequence_gaps_total',
            '检测到的序列号间隙总数',
            ['exchange', 'symbol', 'gap_size_bucket'],
            registry=registry
        )
        
        self.ticks_written = Counter(
            'orderbook_collector_ticks_written_total',
            '写入存储的tick总数',
            ['exchange', 'symbol'],
            registry=registry
        )
        
        self.files_written = Counter(
            'orderbook_collector_files_written_total',
            '写入的Parquet文件总数',
            ['exchange', 'symbol'],
            registry=registry
        )
        
        # === 连接状态指标 ===
        
        self.connection_status = Gauge(
            'orderbook_collector_connection_status',
            'WebSocket连接状态 (0=断开, 1=已连接, 2=重连中)',
            ['exchange', 'symbol'],
            registry=registry
        )
        
        self.last_message_timestamp = Gauge(
            'orderbook_collector_last_message_timestamp',
            '最后一条成功消息的Unix时间戳',
            ['exchange', 'symbol'],
            registry=registry
        )
        
        self.disconnections = Counter(
            'orderbook_collector_disconnections_total',
            'WebSocket断开连接总次数',
            ['exchange', 'symbol', 'reason'],
            registry=registry
        )
        
        self.reconnections = Counter(
            'orderbook_collector_reconnections_total',
            '重连尝试总次数',
            ['exchange', 'symbol'],
            registry=registry
        )
        
        # === 性能指标 ===
        
        self.message_processing_latency = Histogram(
            'orderbook_collector_message_processing_seconds',
            '消息处理延迟（秒）',
            ['exchange', 'symbol'],
            buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0],
            registry=registry
        )
        
        self.buffer_size = Gauge(
            'orderbook_collector_buffer_size',
            '当前缓冲区中的项目数',
            ['exchange', 'symbol'],
            registry=registry
        )
        
        self.file_write_latency = Histogram(
            'orderbook_collector_file_write_seconds',
            'Parquet文件写入延迟（秒）',
            ['exchange', 'symbol'],
            buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0],
            registry=registry
        )
        
        # === 数据质量指标 ===
        
        self.data_freshness = Gauge(
            'orderbook_collector_data_freshness_seconds',
            '距离最后一次数据更新的秒数',
            ['exchange', 'symbol'],
            registry=registry
        )
        
        self.corrupted_files = Gauge(
            'orderbook_collector_corrupted_files',
            '检测到的损坏Parquet文件数',
            ['exchange', 'symbol'],
            registry=registry
        )
        
        self.disk_usage = Gauge(
            'orderbook_collector_disk_usage_bytes',
            '收集数据使用的磁盘空间（字节）',
            ['exchange'],
            registry=registry
        )
        
        logger.info("✅ Prometheus metrics registry initialized")
    
    # === 辅助方法 ===
    
    def increment_messages_received(self, exchange: str, symbol: str, message_type: str):
        """记录接收到的消息"""
        self.messages_received.labels(
            exchange=exchange,
            symbol=symbol,
            message_type=message_type
        ).inc()
    
    def increment_messages_processed(self, exchange: str, symbol: str):
        """记录成功处理的消息"""
        self.messages_processed.labels(
            exchange=exchange,
            symbol=symbol
        ).inc()
    
    def increment_messages_failed(self, exchange: str, symbol: str, error_type: str):
        """记录处理失败的消息"""
        self.messages_failed.labels(
            exchange=exchange,
            symbol=symbol,
            error_type=error_type
        ).inc()
    
    def record_sequence_gap(self, exchange: str, symbol: str, gap_size: int):
        """
        记录序列号间隙
        
        Args:
            exchange: 交易所名称
            symbol: 交易对
            gap_size: 间隙大小
        """
        # 将间隙大小分桶
        if gap_size <= 10:
            bucket = "small"
        elif gap_size <= 50:
            bucket = "medium"
        elif gap_size <= 100:
            bucket = "large"
        else:
            bucket = "critical"
        
        self.sequence_gaps.labels(
            exchange=exchange,
            symbol=symbol,
            gap_size_bucket=bucket
        ).inc()
    
    def set_connection_status(self, exchange: str, symbol: str, status: int):
        """
        设置连接状态
        
        Args:
            exchange: 交易所名称
            symbol: 交易对
            status: 状态值 (0=断开, 1=已连接, 2=重连中)
        """
        self.connection_status.labels(
            exchange=exchange,
            symbol=symbol
        ).set(status)
    
    def update_last_message_time(self, exchange: str, symbol: str, timestamp: float):
        """更新最后消息时间戳"""
        self.last_message_timestamp.labels(
            exchange=exchange,
            symbol=symbol
        ).set(timestamp)
    
    def record_disconnection(self, exchange: str, symbol: str, reason: str):
        """记录断开连接事件"""
        self.disconnections.labels(
            exchange=exchange,
            symbol=symbol,
            reason=reason
        ).inc()
    
    def record_reconnection(self, exchange: str, symbol: str):
        """记录重连尝试"""
        self.reconnections.labels(
            exchange=exchange,
            symbol=symbol
        ).inc()
    
    def observe_processing_latency(self, exchange: str, symbol: str, seconds: float):
        """记录消息处理延迟"""
        self.message_processing_latency.labels(
            exchange=exchange,
            symbol=symbol
        ).observe(seconds)
    
    def set_buffer_size(self, exchange: str, symbol: str, size: int):
        """更新缓冲区大小"""
        self.buffer_size.labels(
            exchange=exchange,
            symbol=symbol
        ).set(size)
    
    def observe_file_write_latency(self, exchange: str, symbol: str, seconds: float):
        """记录文件写入延迟"""
        self.file_write_latency.labels(
            exchange=exchange,
            symbol=symbol
        ).observe(seconds)
    
    def increment_ticks_written(self, exchange: str, symbol: str, count: int = 1):
        """记录写入的tick数量"""
        self.ticks_written.labels(
            exchange=exchange,
            symbol=symbol
        ).inc(count)
    
    def increment_files_written(self, exchange: str, symbol: str):
        """记录写入的文件数"""
        self.files_written.labels(
            exchange=exchange,
            symbol=symbol
        ).inc()
    
    def update_data_freshness(self, exchange: str, symbol: str, seconds: float):
        """更新数据新鲜度"""
        self.data_freshness.labels(
            exchange=exchange,
            symbol=symbol
        ).set(seconds)
    
    def set_corrupted_files(self, exchange: str, symbol: str, count: int):
        """设置损坏文件数"""
        self.corrupted_files.labels(
            exchange=exchange,
            symbol=symbol
        ).set(count)
    
    def update_disk_usage(self, exchange: str, bytes_used: int):
        """更新磁盘使用量"""
        self.disk_usage.labels(
            exchange=exchange
        ).set(bytes_used)


# 全局单例实例
_metrics_instance: Optional[OrderbookMetrics] = None


def get_metrics() -> OrderbookMetrics:
    """
    获取或创建全局指标实例
    
    Returns:
        OrderbookMetrics单例
    """
    global _metrics_instance
    if _metrics_instance is None:
        _metrics_instance = OrderbookMetrics()
        logger.info("Created global OrderbookMetrics instance")
    return _metrics_instance

