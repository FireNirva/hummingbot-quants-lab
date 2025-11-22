#!/usr/bin/env python3
"""
Prometheus监控测试脚本

测试指标收集和HTTP导出功能。

Usage:
    python scripts/test_prometheus_monitoring.py
"""

import time
import logging
import random
from core.monitoring.metrics import get_metrics
from core.monitoring.exporter import get_exporter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def simulate_data_collection():
    """模拟数据收集过程"""
    
    # 获取指标实例
    metrics = get_metrics()
    
    # 获取并启动导出器
    exporter = get_exporter(port=8000)
    
    logger.info("="*80)
    logger.info("🧪 Prometheus Monitoring Test")
    logger.info("="*80)
    logger.info("")
    logger.info("📊 Metrics endpoint: http://localhost:8000/metrics")
    logger.info("💚 Health check: http://localhost:8000/health")
    logger.info("")
    logger.info("Starting simulation...")
    logger.info("")
    
    # 模拟交易对
    exchanges = ["gate_io", "mexc"]
    symbols = {
        "gate_io": ["VIRTUAL-USDT", "IRON-USDT", "LMTS-USDT"],
        "mexc": ["AUKIUSDT", "IRONUSDT", "SERVUSDT"]
    }
    
    # 初始化连接状态
    for exchange in exchanges:
        for symbol in symbols[exchange]:
            metrics.set_connection_status(exchange, symbol, 1)  # 已连接
    
    try:
        iteration = 0
        while True:
            iteration += 1
            logger.info(f"--- Iteration {iteration} ---")
            
            for exchange in exchanges:
                for symbol in symbols[exchange]:
                    # 模拟接收消息
                    num_messages = random.randint(50, 200)
                    for _ in range(num_messages):
                        message_type = random.choice(["update", "snapshot"])
                        metrics.increment_messages_received(exchange, symbol, message_type)
                    
                    # 模拟处理成功
                    success_count = int(num_messages * 0.98)  # 98%成功率
                    for _ in range(success_count):
                        metrics.increment_messages_processed(exchange, symbol)
                        
                        # 模拟处理延迟
                        latency = random.uniform(0.001, 0.05)
                        metrics.observe_processing_latency(exchange, symbol, latency)
                    
                    # 模拟处理失败
                    failed_count = num_messages - success_count
                    if failed_count > 0:
                        error_types = ["parse_error", "validation_error", "timeout"]
                        for _ in range(failed_count):
                            error_type = random.choice(error_types)
                            metrics.increment_messages_failed(exchange, symbol, error_type)
                    
                    # 模拟序列号间隙
                    if random.random() < 0.1:  # 10%概率出现间隙
                        gap_size = random.choice([5, 15, 60, 120])
                        metrics.record_sequence_gap(exchange, symbol, gap_size)
                    
                    # 模拟缓冲区大小
                    buffer_size = random.randint(50, 150)
                    metrics.set_buffer_size(exchange, symbol, buffer_size)
                    
                    # 模拟写入tick
                    if buffer_size > 100 or (iteration % 10 == 0):
                        ticks_count = buffer_size
                        metrics.increment_ticks_written(exchange, symbol, ticks_count)
                        
                        # 模拟文件写入
                        if random.random() < 0.3:  # 30%概率写入新文件
                            metrics.increment_files_written(exchange, symbol)
                            write_latency = random.uniform(0.1, 1.0)
                            metrics.observe_file_write_latency(exchange, symbol, write_latency)
                    
                    # 更新最后消息时间
                    metrics.update_last_message_time(exchange, symbol, time.time())
                    
                    # 更新数据新鲜度
                    freshness = random.uniform(0, 5)
                    metrics.update_data_freshness(exchange, symbol, freshness)
                    
                    # 偶尔模拟连接问题
                    if random.random() < 0.01:  # 1%概率断开
                        logger.warning(f"⚠️  Simulating disconnection: {exchange} {symbol}")
                        metrics.set_connection_status(exchange, symbol, 0)
                        metrics.record_disconnection(exchange, symbol, "connection_lost")
                        time.sleep(2)
                        
                        # 重连
                        logger.info(f"🔄 Reconnecting: {exchange} {symbol}")
                        metrics.set_connection_status(exchange, symbol, 2)
                        metrics.record_reconnection(exchange, symbol)
                        time.sleep(1)
                        
                        metrics.set_connection_status(exchange, symbol, 1)
            
            # 模拟磁盘使用量
            for exchange in exchanges:
                disk_usage = random.randint(9 * 1024 * 1024, 12 * 1024 * 1024)  # 9-12 MB
                metrics.update_disk_usage(exchange, disk_usage)
            
            logger.info(f"✅ Simulated metrics for {len(exchanges)} exchanges")
            logger.info(f"   Check metrics at: http://localhost:8000/metrics")
            logger.info("")
            
            # 等待下一轮
            time.sleep(5)
    
    except KeyboardInterrupt:
        logger.info("\n\n⏸️  Simulation stopped")
        logger.info("Metrics endpoint remains available for a few more seconds...")


if __name__ == "__main__":
    try:
        simulate_data_collection()
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)

