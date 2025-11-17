"""
CEX交易对到DEX池子的映射服务

这个模块提供核心功能来：
1. 从candles目录自动检测交易对
2. 使用GeckoTerminal API搜索对应的DEX池子
3. 保存原始API响应和处理后的映射数据
4. 支持CEX-DEX token名称映射（处理wrapped tokens等）
"""
import asyncio
import json
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional
from datetime import datetime, timezone

import pandas as pd
import yaml
from geckoterminal_py import GeckoTerminalAsyncClient

from core.data_paths import data_paths

logger = logging.getLogger(__name__)


class PoolMappingService:
    """CEX交易对到DEX池子的映射服务"""
    
    def __init__(self, token_mapping_file: Optional[str] = None):
        """
        初始化服务
        
        Args:
            token_mapping_file: Token映射配置文件路径（可选）
                               默认使用 config/token_mapping.yml
        """
        self.gt_client = None
        self.token_mapping = self._load_token_mapping(token_mapping_file)
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.gt_client = GeckoTerminalAsyncClient()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        # GeckoTerminalAsyncClient没有close方法，无需清理
        pass
    
    def _load_token_mapping(self, token_mapping_file: Optional[str] = None) -> Dict[str, str]:
        """
        加载CEX-DEX token名称映射配置
        
        Args:
            token_mapping_file: 映射配置文件路径（相对于项目根目录）
        
        Returns:
            映射字典 {CEX_TOKEN: DEX_TOKEN}
        """
        if token_mapping_file is None:
            # 默认使用项目根目录下的配置文件
            project_root = Path(__file__).parent.parent.parent
            token_mapping_file = project_root / "config" / "token_mapping.yml"
        else:
            token_mapping_file = Path(token_mapping_file)
        
        if not token_mapping_file.exists():
            logger.warning(f"Token mapping file not found: {token_mapping_file}, using empty mapping")
            return {}
        
        try:
            with open(token_mapping_file, 'r', encoding='utf-8') as f:
                mapping = yaml.safe_load(f)
                if mapping is None:
                    return {}
                if not isinstance(mapping, dict):
                    logger.warning(f"Invalid token mapping format in {token_mapping_file}")
                    return {}
                logger.info(f"Loaded {len(mapping)} token mappings from {token_mapping_file}")
                return mapping
        except Exception as e:
            logger.error(f"Failed to load token mapping from {token_mapping_file}: {e}")
            return {}
    
    def get_dex_token_name(self, cex_token: str) -> str:
        """
        获取DEX上的token名称（处理wrapped tokens等）
        
        Args:
            cex_token: CEX上的token符号（如 "IRON"）
        
        Returns:
            DEX上的token符号（如 "wIRON"），如果没有映射则返回原token
        """
        dex_token = self.token_mapping.get(cex_token, cex_token)
        if dex_token != cex_token:
            logger.info(f"Token mapping: {cex_token} -> {dex_token}")
        return dex_token
    
    def parse_trading_pairs_from_candles(
        self, 
        candles_dir: Path, 
        connector: str = "gate_io"
    ) -> List[str]:
        """
        从candles目录扫描并提取交易对列表
        
        Args:
            candles_dir: Candles数据目录
            connector: CEX连接器名称（如gate_io）
            
        Returns:
            唯一交易对列表（如：['AERO-USDT', 'BRETT-USDT']）
        """
        if not candles_dir.exists():
            logger.warning(f"Candles directory does not exist: {candles_dir}")
            return []
        
        # 扫描parquet文件
        pattern = f"{connector}|*|*.parquet"
        files = list(candles_dir.glob(pattern))
        
        if not files:
            logger.warning(f"No candles files found for connector: {connector}")
            return []
        
        # 提取交易对（格式：connector|PAIR|interval.parquet）
        pairs = set()
        for file in files:
            parts = file.stem.split('|')
            if len(parts) == 3:
                pairs.add(parts[1])  # PAIR部分
        
        pairs_list = sorted(list(pairs))
        logger.info(f"Found {len(pairs_list)} trading pairs for {connector}")
        
        return pairs_list
    
    async def search_pool_for_pair(
        self, 
        token_symbol: str, 
        network: str,
        top_n: int = 3
    ) -> List[Dict[str, Any]]:
        """
        搜索特定代币的池子并返回top N个
        
        Args:
            token_symbol: 代币符号（如AERO或IRON）
            network: 网络ID（如base）
            top_n: 返回池子数量
            
        Returns:
            池子信息列表，按流动性降序排列
        """
        if not self.gt_client:
            self.gt_client = GeckoTerminalAsyncClient()
        
        try:
            # 获取DEX上的token名称（处理wrapped tokens等）
            dex_token = self.get_dex_token_name(token_symbol)
            
            # 调用GeckoTerminal API (使用api_request直接调用endpoint)
            params = {
                'query': dex_token,  # 使用映射后的DEX token名称搜索
                'network': network,
                'page': 1
            }
            response = await self.gt_client.api_request('GET', '/search/pools', params=params)
            
            # 检查响应
            if not response or 'data' not in response:
                logger.warning(f"No pools found for {token_symbol} on {network}")
                return []
            
            pools_data = response['data']
            if not pools_data:
                logger.warning(f"Empty pool data for {token_symbol} on {network}")
                return []
            
            # 解析池子数据
            pools = []
            for pool_item in pools_data:
                try:
                    attrs = pool_item.get('attributes', {})
                    relationships = pool_item.get('relationships', {})
                    
                    # 提取池子名称（用于过滤）
                    pool_name = attrs.get('name', '')
                    
                    # 过滤：只保留base token与查询代币匹配的池子
                    # 池子名称格式通常是 "BASE / QUOTE" 或 "BASE / QUOTE 0.3%"
                    if pool_name:
                        # 提取base token（取第一个'/'前的部分，去除空格）
                        base_token_in_name = pool_name.split('/')[0].strip().upper()
                        # 使用DEX token名称进行匹配（而非CEX token名称）
                        dex_token_upper = dex_token.upper()
                        
                        # 如果base token不匹配，跳过这个池子
                        if base_token_in_name != dex_token_upper:
                            logger.debug(f"Skipping pool '{pool_name}' - base token '{base_token_in_name}' != query '{dex_token_upper}' (CEX: {token_symbol})")
                            continue
                    
                    # 提取DEX ID
                    dex_id = ''
                    if 'dex' in relationships:
                        dex_data = relationships['dex'].get('data', {})
                        if dex_data:
                            dex_id = dex_data.get('id', '')
                    
                    # 提取池子信息
                    pool_info = {
                        'pool_address': attrs.get('address', ''),
                        'name': pool_name,
                        'dex_id': dex_id,
                        'reserve_usd': float(attrs.get('reserve_in_usd', 0) or 0),
                        'volume_usd_h24': float(attrs.get('volume_usd', {}).get('h24', 0) or 0),
                        'pool_created_at': attrs.get('pool_created_at', ''),
                        'base_token_address': '',
                        'quote_token_address': ''
                    }
                    
                    # 提取token地址
                    if 'base_token' in relationships:
                        base_token_data = relationships['base_token'].get('data', {})
                        if base_token_data:
                            pool_info['base_token_address'] = base_token_data.get('id', '').split('_')[-1] if '_' in base_token_data.get('id', '') else ''
                    
                    if 'quote_token' in relationships:
                        quote_token_data = relationships['quote_token'].get('data', {})
                        if quote_token_data:
                            pool_info['quote_token_address'] = quote_token_data.get('id', '').split('_')[-1] if '_' in quote_token_data.get('id', '') else ''
                    
                    pools.append(pool_info)
                    
                except Exception as e:
                    logger.warning(f"Error parsing pool data: {e}")
                    continue
            
            # 按流动性排序
            pools.sort(key=lambda x: x['reserve_usd'], reverse=True)
            
            # 返回top N
            result = pools[:top_n]
            logger.info(f"Found {len(result)} pools for {token_symbol} (total: {len(pools)})")
            
            return result
            
        except Exception as e:
            logger.error(f"Error searching pools for {token_symbol}: {e}")
            return []
    
    async def build_mapping(
        self,
        trading_pairs: List[str],
        network: str,
        connector: str,
        top_n: int = 3
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        为交易对列表构建完整的池子映射
        
        Args:
            trading_pairs: 交易对列表
            network: 网络ID
            connector: CEX连接器名称
            top_n: 每个交易对保留的池子数量
            
        Returns:
            (DataFrame, raw_responses字典)
        """
        logger.info(f"Building pool mapping for {len(trading_pairs)} pairs")
        
        all_mappings = []
        raw_responses = {}
        
        for idx, pair in enumerate(trading_pairs, 1):
            # 提取base token（如AERO-USDT -> AERO）
            base_token = pair.split('-')[0]
            
            logger.info(f"Processing {pair} ({idx}/{len(trading_pairs)})")
            
            try:
                # 搜索池子
                pools = await self.search_pool_for_pair(base_token, network, top_n)
                
                # 保存原始响应（用于后续保存）
                raw_responses[pair] = {
                    'query': base_token,
                    'network': network,
                    'pools_found': len(pools),
                    'pools': pools,
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
                
                # 转换为DataFrame行
                if pools:
                    for rank, pool in enumerate(pools, 1):
                        mapping_row = {
                            'connector': connector,
                            'trading_pair': pair,
                            'network_id': network,
                            'dex_id': pool['dex_id'],
                            'pool_address': pool['pool_address'],
                            'base_token_address': pool['base_token_address'],
                            'quote_token_address': pool['quote_token_address'],
                            'reserve_usd': pool['reserve_usd'],
                            'volume_usd_h24': pool['volume_usd_h24'],
                            'pool_created_at': pool['pool_created_at'],
                            'rank': rank,
                            'updated_at': datetime.now(timezone.utc)
                        }
                        all_mappings.append(mapping_row)
                else:
                    logger.warning(f"No pools found for {pair}")
                
                # API限流：延迟0.5秒
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error processing {pair}: {e}")
                raw_responses[pair] = {
                    'query': base_token,
                    'network': network,
                    'error': str(e),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
                continue
        
        # 创建DataFrame
        if all_mappings:
            df = pd.DataFrame(all_mappings)
            logger.info(f"Created mapping with {len(df)} pool records")
        else:
            # 空DataFrame with schema
            df = pd.DataFrame(columns=[
                'connector', 'trading_pair', 'network_id', 'dex_id',
                'pool_address', 'base_token_address', 'quote_token_address',
                'reserve_usd', 'volume_usd_h24', 'pool_created_at',
                'rank', 'updated_at'
            ])
            logger.warning("No mappings created")
        
        return df, raw_responses
    
    def save_raw_responses(
        self, 
        responses: Dict[str, Any], 
        network: str
    ) -> None:
        """
        保存原始API响应到JSON文件
        
        Args:
            responses: 原始响应字典 {pair: response_data}
            network: 网络ID
        """
        # 使用data_paths构建路径
        output_dir = data_paths.raw_dir / 'geckoterminal' / 'search_pools' / network
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Saving raw responses to {output_dir}")
        
        for pair, response_data in responses.items():
            # 文件名：使用交易对作为文件名
            filename = output_dir / f"{pair}.json"
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(response_data, f, indent=2, ensure_ascii=False, default=str)
                logger.debug(f"Saved raw response for {pair}")
            except Exception as e:
                logger.error(f"Error saving raw response for {pair}: {e}")
        
        logger.info(f"Saved {len(responses)} raw response files")
    
    def save_mapping(
        self,
        df: pd.DataFrame,
        network: str,
        connector: str
    ) -> Path:
        """
        保存处理后的映射数据到Parquet文件
        
        Args:
            df: 映射DataFrame
            network: 网络ID
            connector: CEX连接器名称
            
        Returns:
            保存的文件路径
        """
        # 使用data_paths构建路径
        output_dir = data_paths.processed_dir / 'pool_mappings'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 文件名格式：{network}_{connector}_pool_map.parquet
        filename = output_dir / f"{network}_{connector}_pool_map.parquet"
        
        logger.info(f"Saving mapping to {filename}")
        
        try:
            df.to_parquet(
                filename,
                engine='pyarrow',
                compression='snappy',
                index=False
            )
            logger.info(f"Saved mapping with {len(df)} records")
            return filename
        except Exception as e:
            logger.error(f"Error saving mapping: {e}")
            raise

