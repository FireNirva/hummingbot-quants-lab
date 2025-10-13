"""
DEX 数据补全工具

用于将稀疏的 DEX K线数据补全到连续时间轴，以便进行价差分析。

补全策略：
- 使用前一根蜡烛的 close 价格 forward-fill
- open/high/low/close 全部使用上一根的 close
- volume 设为 0
- 添加 is_filled 标记列
"""
import logging
from typing import Optional, Tuple
from datetime import datetime, timedelta, timezone

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def fill_missing_candles(
    dex_df: pd.DataFrame,
    interval: str,
    reference_index: Optional[pd.DatetimeIndex] = None
) -> pd.DataFrame:
    """
    补全 DEX 数据中缺失的蜡烛。
    
    Args:
        dex_df: DEX K线数据，索引为 DatetimeIndex
        interval: 时间间隔（如 "1m", "5m", "15m", "1h"）
        reference_index: 参考时间索引（如 CEX 的时间索引），如不提供则自动生成完整索引
    
    Returns:
        补全后的 DataFrame，包含 is_filled 标记列
    """
    if len(dex_df) == 0:
        logger.warning("DEX 数据为空，无法补全")
        return dex_df
    
    # 解析时间间隔
    freq = _parse_interval_to_freq(interval)
    
    # 确定完整的时间索引
    if reference_index is not None:
        # 使用参考索引（CEX 的时间轴）
        full_index = reference_index
    else:
        # 自动生成从第一根到最后一根的完整索引
        start_time = dex_df.index.min()
        end_time = dex_df.index.max()
        full_index = pd.date_range(start=start_time, end=end_time, freq=freq)
    
    logger.info(f"原始 DEX 数据: {len(dex_df)} 根蜡烛")
    logger.info(f"完整时间索引: {len(full_index)} 个时间点")
    logger.info(f"需要补全: {len(full_index) - len(dex_df)} 根蜡烛")
    
    # 创建完整的 DataFrame
    filled_df = pd.DataFrame(index=full_index)
    
    # 合并现有数据
    filled_df = filled_df.join(dex_df, how='left')
    
    # 添加 is_filled 标记列（在补全之前）
    filled_df['is_filled'] = filled_df['close'].isna()
    
    # Forward-fill 价格数据
    price_columns = ['open', 'high', 'low', 'close']
    for col in price_columns:
        if col in filled_df.columns:
            # 使用前一根的 close 填充所有价格列
            filled_df[col] = filled_df['close'].ffill()
    
    # Volume 和其他列设为 0
    volume_columns = ['volume', 'quote_asset_volume', 'n_trades', 
                     'taker_buy_base_volume', 'taker_buy_quote_volume']
    
    for col in volume_columns:
        if col in filled_df.columns:
            filled_df[col] = filled_df[col].fillna(0.0)
    
    # 统计补全情况
    n_filled = filled_df['is_filled'].sum()
    fill_rate = (n_filled / len(filled_df) * 100) if len(filled_df) > 0 else 0
    
    logger.info(f"补全完成: 新增 {n_filled} 根蜡烛 ({fill_rate:.2f}%)")
    
    return filled_df


def align_dex_to_cex(
    cex_df: pd.DataFrame,
    dex_df: pd.DataFrame,
    interval: str
) -> pd.DataFrame:
    """
    将 DEX 数据对齐到 CEX 的时间轴。
    
    Args:
        cex_df: CEX K线数据
        dex_df: DEX K线数据
        interval: 时间间隔
    
    Returns:
        对齐并补全后的 DEX 数据
    """
    logger.info("="*60)
    logger.info("开始 DEX-CEX 时间轴对齐")
    logger.info("="*60)
    
    # 使用 CEX 的时间索引作为参考
    filled_dex = fill_missing_candles(dex_df, interval, reference_index=cex_df.index)
    
    # 确保只保留 CEX 时间范围内的数据
    filled_dex = filled_dex.loc[cex_df.index]
    
    return filled_dex


def create_spread_dataframe(
    cex_df: pd.DataFrame,
    dex_df_filled: pd.DataFrame,
    fill_aware: bool = True
) -> pd.DataFrame:
    """
    创建价差分析 DataFrame。
    
    Args:
        cex_df: CEX K线数据
        dex_df_filled: 补全后的 DEX K线数据（包含 is_filled 列）
        fill_aware: 是否包含 is_filled 标记信息
    
    Returns:
        包含价差信息的 DataFrame
    """
    # 合并数据
    spread_df = pd.DataFrame(index=cex_df.index)
    
    # CEX 数据
    spread_df['cex_close'] = cex_df['close']
    spread_df['cex_volume'] = cex_df['volume']
    
    # DEX 数据
    spread_df['dex_close'] = dex_df_filled['close']
    spread_df['dex_volume'] = dex_df_filled['volume']
    
    # 补全标记
    if fill_aware and 'is_filled' in dex_df_filled.columns:
        spread_df['dex_is_filled'] = dex_df_filled['is_filled']
    else:
        spread_df['dex_is_filled'] = False
    
    # 计算价差
    spread_df['price_diff'] = spread_df['dex_close'] - spread_df['cex_close']
    spread_df['price_diff_pct'] = (spread_df['price_diff'] / spread_df['cex_close'] * 100)
    
    # 套利方向
    spread_df['arb_direction'] = 'neutral'
    spread_df.loc[spread_df['price_diff_pct'] > 0.5, 'arb_direction'] = 'cex_to_dex'  # CEX 买，DEX 卖
    spread_df.loc[spread_df['price_diff_pct'] < -0.5, 'arb_direction'] = 'dex_to_cex'  # DEX 买，CEX 卖
    
    # 可执行性标记（DEX 有实际成交量）
    spread_df['is_executable'] = (~spread_df['dex_is_filled']) & (spread_df['dex_volume'] > 0)
    
    return spread_df


def get_spread_statistics(
    spread_df: pd.DataFrame,
    include_filled: bool = True
) -> dict:
    """
    计算价差统计信息。
    
    Args:
        spread_df: 价差数据
        include_filled: 是否包含补全的数据点
    
    Returns:
        统计字典
    """
    if include_filled:
        data = spread_df
        label = "全部数据（含补全）"
    else:
        data = spread_df[~spread_df['dex_is_filled']]
        label = "仅实际交易"
    
    stats = {
        'label': label,
        'total_points': len(data),
        'mean_spread_pct': data['price_diff_pct'].mean(),
        'median_spread_pct': data['price_diff_pct'].median(),
        'std_spread_pct': data['price_diff_pct'].std(),
        'min_spread_pct': data['price_diff_pct'].min(),
        'max_spread_pct': data['price_diff_pct'].max(),
    }
    
    # 套利机会统计
    if include_filled:
        # 全部数据：名义套利机会
        stats['arb_opportunities'] = {
            'cex_to_dex': len(data[data['arb_direction'] == 'cex_to_dex']),
            'dex_to_cex': len(data[data['arb_direction'] == 'dex_to_cex']),
            'neutral': len(data[data['arb_direction'] == 'neutral']),
        }
    else:
        # 仅实际交易：可执行套利机会
        executable = data[data['is_executable']]
        stats['arb_opportunities'] = {
            'cex_to_dex': len(executable[executable['arb_direction'] == 'cex_to_dex']),
            'dex_to_cex': len(executable[executable['arb_direction'] == 'dex_to_cex']),
            'neutral': len(executable[executable['arb_direction'] == 'neutral']),
        }
        stats['executable_rate'] = len(executable) / len(data) * 100 if len(data) > 0 else 0
    
    return stats


def _parse_interval_to_freq(interval: str) -> str:
    """
    将时间间隔字符串转换为 pandas 频率字符串。
    
    Args:
        interval: "1m", "5m", "15m", "1h" 等
    
    Returns:
        pandas 频率字符串，如 "1min", "5min", "1H"
    """
    import re
    
    match = re.match(r'^(\d+)([mhd])$', interval.lower())
    if not match:
        raise ValueError(f"Invalid interval format: {interval}")
    
    number = match.group(1)
    unit = match.group(2)
    
    # 映射到 pandas 频率
    unit_map = {
        'm': 'min',  # minute
        'h': 'H',    # hour
        'd': 'D',    # day
    }
    
    return f"{number}{unit_map[unit]}"

