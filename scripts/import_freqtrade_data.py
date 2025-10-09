#!/usr/bin/env python3
"""
Freqtrade to QuantsLab Data Import Script

Downloads historical data using Freqtrade and converts it to QuantsLab's Parquet format.

Usage:
    python scripts/import_freqtrade_data.py \
        --config config/base_ecosystem_downloader_full.yml \
        --days 180 \
        --timeframe 1m
"""

import argparse
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

import pandas as pd
import yaml

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FreqtradeDataImporter:
    """Import historical data from Freqtrade to QuantsLab format."""
    
    def __init__(self, config_path: str, days: int, timeframe: str = "1m", prepend: bool = False, exchange: str = None):
        self.config_path = config_path
        self.days = days
        self.timeframe = timeframe
        self.prepend = prepend  # Prepend historical data to existing data
        
        # Paths
        self.project_root = Path.cwd()
        self.user_data_dir = self.project_root / "user_data"
        
        # Exchange will be set from config or command line
        self._exchange_override = exchange  # Store command line override
        self.exchange = None  # Will be set in parse_config()
        
        # These will be set after exchange is determined
        self.freqtrade_data_dir = None
        self.freqtrade_backup_dir = None
        self.quantslab_candles_dir = None
        
        # Statistics
        self.stats = {
            'total_pairs': 0,
            'successful': 0,
            'failed': 0,
            'failed_pairs': []
        }
        
    def parse_config(self) -> List[str]:
        """Parse YAML config to extract trading pairs and exchange."""
        logger.info(f"Parsing config: {self.config_path}")
        
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Navigate to trading_pairs
            tasks = config.get('tasks', {})
            task_config = None
            
            # Find the first task with trading_pairs
            for task_name, task_data in tasks.items():
                if 'config' in task_data and 'trading_pairs' in task_data['config']:
                    task_config = task_data['config']
                    break
            
            if not task_config:
                raise ValueError("No trading_pairs found in config")
            
            # Get exchange from config or command line
            if self._exchange_override:
                self.exchange = self._exchange_override
                logger.info(f"Using exchange from command line: {self.exchange}")
            else:
                # Get connector_name from config (e.g., "gate_io")
                connector_name = task_config.get('connector_name', 'gate_io')
                # Convert to Freqtrade format: gate_io -> gateio
                self.exchange = connector_name.replace('_', '')
                logger.info(f"Using exchange from config: {self.exchange} (connector: {connector_name})")
            
            # Now set up directory paths
            self.freqtrade_data_dir = self.user_data_dir / "data" / self.exchange
            self.freqtrade_backup_dir = self.project_root / "app" / "data" / "raw" / "freqtrade" / self.exchange
            self.quantslab_candles_dir = self.project_root / "app" / "data" / "cache" / "candles"
            
            trading_pairs = task_config.get('trading_pairs', [])
            
            # Filter out commented pairs
            active_pairs = [pair for pair in trading_pairs if isinstance(pair, str)]
            
            logger.info(f"Found {len(active_pairs)} trading pairs")
            return active_pairs
            
        except Exception as e:
            logger.error(f"Error parsing config: {e}")
            raise
    
    def ensure_directories(self):
        """Create necessary directories."""
        logger.info("Creating directory structure...")
        
        directories = [
            self.user_data_dir,
            self.freqtrade_data_dir,      # Freqtrade standard: user_data/data/gateio/
            self.freqtrade_backup_dir,
            self.quantslab_candles_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"  ✓ {directory}")
    
    def convert_pair_format(self, pair: str, to_freqtrade: bool = True) -> str:
        """
        Convert pair format between QuantsLab and Freqtrade.
        
        Args:
            pair: Trading pair
            to_freqtrade: If True, convert USDT-XXX to XXX/USDT, else reverse
        """
        if to_freqtrade:
            # VIRTUAL-USDT → VIRTUAL/USDT
            return pair.replace('-', '/')
        else:
            # VIRTUAL/USDT → VIRTUAL-USDT
            return pair.replace('/', '-')
    
    def download_freqtrade_data(self, pairs: List[str]) -> bool:
        """Download data using Freqtrade."""
        logger.info(f"\n{'='*80}")
        logger.info(f"Downloading {len(pairs)} pairs from Freqtrade")
        logger.info(f"{'='*80}\n")
        
        # Convert pairs to Freqtrade format
        freqtrade_pairs = [self.convert_pair_format(p, to_freqtrade=True) for p in pairs]
        
        # Build command
        # Note: Don't specify --datadir, let Freqtrade use default structure
        # Freqtrade will automatically save to: user_data/data/{exchange}/
        cmd = [
            "freqtrade", "download-data",
            "--exchange", self.exchange,
            "--timeframe", self.timeframe,
            "--days", str(self.days)
        ]
        
        # Add --prepend flag if requested
        if self.prepend:
            cmd.append("--prepend")
            logger.info("📥 --prepend flag enabled: Will add historical data before existing data")
        
        cmd.extend(["--pairs"] + freqtrade_pairs)
        
        logger.info(f"Command: {' '.join(cmd)}")
        
        try:
            # Run in freqtrade conda environment
            result = subprocess.run(
                ["conda", "run", "-n", "freqtrade"] + cmd,
                capture_output=True,
                text=True,
                check=False  # Don't raise on non-zero exit
            )
            
            logger.info("Download process completed")
            
            # Show stdout (always useful)
            if result.stdout:
                logger.info("Freqtrade output:")
                for line in result.stdout.splitlines()[-20:]:  # Last 20 lines
                    logger.info(f"  {line}")
            
            # Show stderr if there were errors
            if result.stderr:
                logger.warning("Freqtrade warnings/errors:")
                for line in result.stderr.splitlines()[-20:]:
                    logger.warning(f"  {line}")
            
            # List actually downloaded files (from Freqtrade standard directory)
            downloaded_files = list(self.freqtrade_data_dir.glob("*.feather"))
            logger.info(f"\n✓ Actually downloaded {len(downloaded_files)} files:")
            for f in downloaded_files:
                logger.info(f"  - {f.name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Download failed with exception: {e}")
            return False
    
    def convert_feather_to_parquet(self, pair: str) -> Tuple[bool, str]:
        """
        Convert single Freqtrade Feather file to QuantsLab Parquet format.
        
        Args:
            pair: Trading pair in QuantsLab format (e.g., VIRTUAL-USDT)
            
        Returns:
            Tuple of (success, message)
        """
        # Freqtrade file naming: BTC_USDT-1m.feather
        freqtrade_filename = f"{pair.replace('-', '_')}-{self.timeframe}.feather"
        freqtrade_path = self.freqtrade_data_dir / freqtrade_filename
        
        # QuantsLab file naming: gate_io|BTC-USDT|1m.parquet
        quantslab_filename = f"gate_io|{pair}|{self.timeframe}.parquet"
        quantslab_path = self.quantslab_candles_dir / quantslab_filename
        
        if not freqtrade_path.exists():
            return False, f"Freqtrade file not found: {freqtrade_path}"
        
        try:
            # Read Freqtrade Feather file
            df = pd.read_feather(freqtrade_path)
            
            logger.info(f"  Read {len(df)} rows from {freqtrade_filename}")
            
            # Convert to QuantsLab format
            # 1. Convert date to Unix seconds
            df['timestamp'] = df['date'].astype('int64') / 1e9
            
            # 2. Set date as index
            df.index = df['date']
            df.index.name = 'timestamp'
            
            # 3. Drop original date column
            df = df.drop('date', axis=1)
            
            # 4. Add missing columns with 0.0
            missing_columns = [
                'quote_asset_volume',
                'n_trades',
                'taker_buy_base_volume',
                'taker_buy_quote_volume'
            ]
            
            for col in missing_columns:
                if col not in df.columns:
                    df[col] = 0.0
            
            # 5. Ensure all columns are float64
            for col in df.columns:
                df[col] = df[col].astype('float64')
            
            # 6. Reorder columns to match QuantsLab format
            column_order = [
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'quote_asset_volume', 'n_trades', 
                'taker_buy_base_volume', 'taker_buy_quote_volume'
            ]
            df = df[column_order]
            
            # 7. Data validation
            if df.isnull().any().any():
                null_counts = df.isnull().sum()
                logger.warning(f"  Found NaN values: {null_counts[null_counts > 0]}")
            
            # 8. Save to Parquet
            df.to_parquet(
                quantslab_path,
                engine='pyarrow',
                compression='snappy',
                index=True
            )
            
            # Get file size
            file_size = quantslab_path.stat().st_size / 1024  # KB
            
            # 9. Backup original Feather file
            backup_path = self.freqtrade_backup_dir / freqtrade_filename
            shutil.copy2(freqtrade_path, backup_path)
            
            time_range = f"{df.index.min()} to {df.index.max()}"
            message = f"Converted {len(df)} rows, {file_size:.2f} KB, Range: {time_range}"
            
            return True, message
            
        except Exception as e:
            return False, f"Conversion error: {str(e)}"
    
    def validate_parquet(self, pair: str) -> Tuple[bool, str]:
        """Validate converted Parquet file."""
        quantslab_filename = f"gate_io|{pair}|{self.timeframe}.parquet"
        quantslab_path = self.quantslab_candles_dir / quantslab_filename
        
        if not quantslab_path.exists():
            return False, "Output file not found"
        
        try:
            df = pd.read_parquet(quantslab_path)
            
            # Check required columns
            required_columns = [
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'quote_asset_volume', 'n_trades', 
                'taker_buy_base_volume', 'taker_buy_quote_volume'
            ]
            
            missing = [col for col in required_columns if col not in df.columns]
            if missing:
                return False, f"Missing columns: {missing}"
            
            # Check index
            if not isinstance(df.index, pd.DatetimeIndex):
                return False, "Index is not DatetimeIndex"
            
            if df.index.name != 'timestamp':
                return False, f"Index name is '{df.index.name}', expected 'timestamp'"
            
            # Check for NaN
            if df.isnull().any().any():
                null_counts = df.isnull().sum()
                return False, f"Contains NaN: {null_counts[null_counts > 0].to_dict()}"
            
            # Check timestamp continuity (should be sorted)
            if not df.index.is_monotonic_increasing:
                return False, "Timestamps are not sorted"
            
            return True, "✓ Validation passed"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def process_pairs(self, pairs: List[str]):
        """Process all trading pairs that were actually downloaded."""
        # Find actually downloaded files (from Freqtrade standard directory)
        downloaded_files = list(self.freqtrade_data_dir.glob(f"*-{self.timeframe}.feather"))
        
        # Extract pair names from downloaded files
        # File format: VIRTUAL_USDT-1m.feather -> VIRTUAL-USDT
        downloaded_pairs = []
        for file in downloaded_files:
            # Remove timeframe and extension: VIRTUAL_USDT-1m.feather -> VIRTUAL_USDT
            pair_name = file.stem.replace(f"-{self.timeframe}", "")
            # Convert to QuantsLab format: VIRTUAL_USDT -> VIRTUAL-USDT
            pair_name = pair_name.replace("_", "-")
            downloaded_pairs.append(pair_name)
        
        # Update stats
        self.stats['total_pairs'] = len(pairs)
        requested_pairs = set(pairs)
        actually_downloaded = set(downloaded_pairs)
        
        # Report missing pairs
        missing_pairs = requested_pairs - actually_downloaded
        if missing_pairs:
            logger.warning(f"\n⚠️  {len(missing_pairs)} pairs were NOT downloaded by Freqtrade:")
            for pair in sorted(missing_pairs):
                logger.warning(f"  - {pair} (may not exist on Gate.io or insufficient data)")
                self.stats['failed'] += 1
                self.stats['failed_pairs'].append(pair)
        
        if not downloaded_pairs:
            logger.error("No files were downloaded! Aborting conversion.")
            return
        
        logger.info(f"\n{'='*80}")
        logger.info(f"Converting {len(downloaded_pairs)} successfully downloaded pairs")
        logger.info(f"{'='*80}\n")
        
        for i, pair in enumerate(downloaded_pairs, 1):
            logger.info(f"[{i}/{len(downloaded_pairs)}] Processing {pair}...")
            
            # Convert
            success, message = self.convert_feather_to_parquet(pair)
            
            if success:
                logger.info(f"  ✓ {message}")
                
                # Validate
                valid, val_message = self.validate_parquet(pair)
                if valid:
                    logger.info(f"  {val_message}")
                    self.stats['successful'] += 1
                else:
                    logger.warning(f"  ⚠ Validation warning: {val_message}")
                    self.stats['successful'] += 1  # Still count as successful
            else:
                logger.error(f"  ✗ {message}")
                self.stats['failed'] += 1
                self.stats['failed_pairs'].append(pair)
    
    def print_summary(self):
        """Print summary report."""
        logger.info(f"\n{'='*80}")
        logger.info("IMPORT SUMMARY")
        logger.info(f"{'='*80}")
        logger.info(f"Total pairs:      {self.stats['total_pairs']}")
        logger.info(f"Successful:       {self.stats['successful']}")
        logger.info(f"Failed:           {self.stats['failed']}")
        
        if self.stats['failed_pairs']:
            logger.info(f"\nFailed pairs:")
            for pair in self.stats['failed_pairs']:
                logger.info(f"  - {pair}")
        
        logger.info(f"\n{'='*80}")
        logger.info(f"Data locations:")
        logger.info(f"  Freqtrade raw:  {self.freqtrade_data_dir}")
        logger.info(f"  Backup:         {self.freqtrade_backup_dir}")
        logger.info(f"  QuantsLab:      {self.quantslab_candles_dir}")
        logger.info(f"{'='*80}\n")
    
    def run(self):
        """Main execution flow."""
        try:
            # 1. Parse config
            pairs = self.parse_config()
            
            # 2. Ensure directories exist
            self.ensure_directories()
            
            # 3. Download data from Freqtrade
            if not self.download_freqtrade_data(pairs):
                logger.error("Download failed, aborting")
                return False
            
            # 4. Convert all pairs
            self.process_pairs(pairs)
            
            # 5. Print summary
            self.print_summary()
            
            return self.stats['failed'] == 0
            
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            return False


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Import historical data from Freqtrade to QuantsLab',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initial download: 6 days of 1m data (exchange from config)
  python scripts/import_freqtrade_data.py \\
      --config config/base_ecosystem_downloader_full.yml \\
      --days 6 \\
      --timeframe 1m
  
  # Override exchange from command line
  python scripts/import_freqtrade_data.py \\
      --config config/base_ecosystem_downloader_full.yml \\
      --days 6 \\
      --timeframe 1m \\
      --exchange binance
  
  # Prepend more historical data (download older data before existing)
  python scripts/import_freqtrade_data.py \\
      --config config/base_ecosystem_downloader_full.yml \\
      --days 6 \\
      --timeframe 1m \\
      --prepend
  
  # Download 7 days of 5m data
  python scripts/import_freqtrade_data.py \\
      --config config/base_ecosystem_downloader_full.yml \\
      --days 7 \\
      --timeframe 5m
        """
    )
    
    parser.add_argument(
        '--config',
        required=True,
        help='Path to QuantsLab config YAML file'
    )
    
    parser.add_argument(
        '--days',
        type=int,
        required=True,
        help='Number of days of historical data to download'
    )
    
    parser.add_argument(
        '--timeframe',
        default='1m',
        help='Timeframe/interval (default: 1m)'
    )
    
    parser.add_argument(
        '--prepend',
        action='store_true',
        help='Prepend historical data to existing data (download older data, default: False)'
    )
    
    parser.add_argument(
        '--exchange',
        default=None,
        help='Exchange name (overrides config file, e.g., gateio, binance)'
    )
    
    args = parser.parse_args()
    
    # Validate config file exists
    if not os.path.exists(args.config):
        logger.error(f"Config file not found: {args.config}")
        sys.exit(1)
    
    # Run importer
    importer = FreqtradeDataImporter(
        config_path=args.config,
        days=args.days,
        timeframe=args.timeframe,
        prepend=args.prepend,
        exchange=args.exchange
    )
    
    success = importer.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

