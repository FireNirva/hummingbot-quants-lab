"""
Prometheus HTTP Exporter

暴露 /metrics HTTP端点供Prometheus抓取。

Author: Alice
Date: 2025-11-22
"""

from flask import Flask, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from typing import Optional
import logging
import threading

logger = logging.getLogger(__name__)


class MetricsExporter:
    """
    Prometheus指标HTTP导出器
    
    启动一个轻量级Flask服务器，暴露/metrics端点供Prometheus抓取。
    
    使用示例：
        exporter = MetricsExporter(port=8000)
        exporter.start()
        # ... 数据收集运行中 ...
        exporter.stop()
    """
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        """
        初始化指标导出器
        
        Args:
            host: 绑定地址 (默认: 0.0.0.0 监听所有网卡)
            port: HTTP端口 (默认: 8000)
        """
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.server_thread: Optional[threading.Thread] = None
        
        # 配置Flask日志
        flask_logger = logging.getLogger('werkzeug')
        flask_logger.setLevel(logging.WARNING)  # 减少Flask的verbose日志
        
        # 注册路由
        @self.app.route('/metrics')
        def metrics():
            """Prometheus指标端点"""
            return Response(
                generate_latest(),
                mimetype=CONTENT_TYPE_LATEST
            )
        
        @self.app.route('/health')
        def health():
            """健康检查端点"""
            return {"status": "healthy", "service": "orderbook-collector"}, 200
        
        @self.app.route('/')
        def index():
            """根路径说明"""
            return {
                "service": "Orderbook Collector Metrics Exporter",
                "endpoints": {
                    "/metrics": "Prometheus metrics (for scraping)",
                    "/health": "Health check"
                }
            }, 200
        
        logger.info(f"✅ Metrics exporter initialized on {host}:{port}")
    
    def start(self):
        """在后台线程中启动HTTP服务器"""
        if self.server_thread is not None and self.server_thread.is_alive():
            logger.warning("Metrics exporter already running")
            return
        
        self.server_thread = threading.Thread(
            target=self._run_server,
            daemon=True,
            name="MetricsExporter"
        )
        self.server_thread.start()
        logger.info(f"🚀 Metrics exporter started: http://{self.host}:{self.port}/metrics")
        logger.info(f"   Health check: http://{self.host}:{self.port}/health")
    
    def _run_server(self):
        """运行Flask服务器（内部方法）"""
        try:
            self.app.run(
                host=self.host,
                port=self.port,
                debug=False,
                use_reloader=False,
                threaded=True
            )
        except Exception as e:
            logger.error(f"Metrics exporter error: {e}")
    
    def stop(self):
        """停止HTTP服务器"""
        # 注意：Flask没有优雅停止的方法
        # 在生产环境中，考虑使用werkzeug.serving.make_server
        logger.info("Metrics exporter stopping...")
        self.server_thread = None


# 全局单例实例
_exporter_instance: Optional[MetricsExporter] = None
_exporter_lock = threading.Lock()


def get_exporter(port: int = 8000) -> MetricsExporter:
    """
    获取或创建全局导出器实例
    
    Args:
        port: HTTP端口
    
    Returns:
        MetricsExporter单例
    """
    global _exporter_instance
    
    if _exporter_instance is None:
        with _exporter_lock:
            if _exporter_instance is None:
                _exporter_instance = MetricsExporter(port=port)
                _exporter_instance.start()
                logger.info(f"Created and started global MetricsExporter on port {port}")
    
    return _exporter_instance

