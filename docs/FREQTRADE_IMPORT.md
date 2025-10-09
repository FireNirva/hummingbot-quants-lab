# Freqtrade Data Import Guide

## Overview

This guide explains how to import historical market data using Freqtrade and convert it to QuantsLab's Parquet format.

**Why use Freqtrade for data import?**
- Gate.io API limits requests to 10,000 data points per call
- For 1-minute data: 10,000 points ≈ 6.94 days
- For 5-minute data: 10,000 points ≈ 34.7 days
- Freqtrade handles pagination and rate limiting automatically
- Base ecosystem tokens have limited history (~8 days available)

## Quick Start

### Prerequisites

1. **Freqtrade environment** with Python 3.11+
2. **QuantsLab environment** for validation
3. Trading pairs configured in `config/base_ecosystem_downloader_full.yml`

### Basic Usage

```bash
# Download 6 days of 1m data (maximum for 1m interval)
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 6 \
  --timeframe 1m

# Download 7 days of 5m data (recommended for Base ecosystem tokens)
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 7 \
  --timeframe 5m
```

## Workflow

### Step 1: Configure Trading Pairs

Edit your config file to specify which pairs to download:

```yaml
# config/base_ecosystem_downloader_full.yml
tasks:
  gateio_base_ecosystem_downloader:
    config:
      trading_pairs:
        - "VIRTUAL-USDT"
        - "BRETT-USDT"
        - "AERO-USDT"
        # Add more pairs...
```

### Step 2: Run Import

```bash
# Initial download: 6 days of 1m data (exchange from config)
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 6 \
  --timeframe 1m

# Download with different exchange (override config)
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 30 \
  --timeframe 5m \
  --exchange binance

# Prepend older historical data (add data before existing)
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 6 \
  --timeframe 1m \
  --prepend
```

### Step 3: Verify Data

```bash
# View converted data
python scripts/view_parquet.py --all

# View specific pair
python scripts/view_parquet.py "app/data/cache/candles/gate_io|VIRTUAL-USDT|1m.parquet"
```

### Step 4: Test Incremental Updates

```bash
# Switch to QuantsLab environment
conda activate quants-lab

# Test that QuantsLab can append new data
python cli.py run-tasks --config config/base_ecosystem_downloader_full.yml
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Parse Config                                             │
│    Extract trading_pairs from YAML                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Download from Freqtrade                                  │
│    freqtrade download-data --exchange gateio ...            │
│    → user_data/data/gateio/BTC_USDT-1m.feather            │
│    (Freqtrade standard directory structure)                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Convert to QuantsLab Format                              │
│    • Read Feather file                                      │
│    • Convert date → timestamp (Unix seconds)                │
│    • Add missing columns (fill with 0)                      │
│    • Set DatetimeIndex                                      │
│    → app/data/cache/candles/gate_io|BTC-USDT|1m.parquet   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Backup & Validate                                        │
│    • Copy raw data to app/data/raw/freqtrade/gateio/       │
│    • Validate: columns, timestamps, NaN check              │
│    • Generate summary report                                │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

The script follows Freqtrade's standard directory structure:

```
quants-lab/
├── user_data/                        # Freqtrade root directory
│   └── data/                         # Data directory (auto-created)
│       ├── gateio/                   # Exchange directory (auto-created)
│       │   ├── VIRTUAL_USDT-1m.feather
│       │   ├── BRETT_USDT-1m.feather
│       │   └── ...
│       ├── binance/                  # Other exchanges (if used)
│       └── okx/
│
└── app/data/
    ├── raw/freqtrade/                # Backup of raw data
    │   └── gateio/
    │       └── *.feather
    └── cache/candles/                # QuantsLab format
        ├── gate_io|VIRTUAL-USDT|1m.parquet
        ├── gate_io|BRETT-USDT|1m.parquet
        └── ...
```

**Key Points:**
- Freqtrade automatically creates `user_data/data/{exchange}/` when no `--datadir` is specified
- This is the standard structure used by all Freqtrade tools
- Multiple exchanges are isolated in separate subdirectories
- Data is backed up to `app/data/raw/freqtrade/` for safety
- Both directories are ignored by Git (in `.gitignore`)

## Data Format Mappings

### Freqtrade Feather Format

```
Columns: date, open, high, low, close, volume
Types:   datetime64[ns, UTC], float64, float64, float64, float64, float64
Index:   RangeIndex
```

### QuantsLab Parquet Format

```
Index:   DatetimeIndex named 'timestamp' (datetime64[ns], UTC)
Columns: timestamp, open, high, low, close, volume,
         quote_asset_volume, n_trades, 
         taker_buy_base_volume, taker_buy_quote_volume
Types:   All float64
```

### Conversion Details

| Freqtrade | QuantsLab | Transformation |
|-----------|-----------|----------------|
| `date` (datetime) | Index `timestamp` | Set as DatetimeIndex |
| `date` (datetime) | Column `timestamp` | Convert to Unix seconds (float) |
| `open` | `open` | Direct copy |
| `high` | `high` | Direct copy |
| `low` | `low` | Direct copy |
| `close` | `close` | Direct copy |
| `volume` | `volume` | Direct copy |
| N/A | `quote_asset_volume` | Fill with 0.0 |
| N/A | `n_trades` | Fill with 0.0 |
| N/A | `taker_buy_base_volume` | Fill with 0.0 |
| N/A | `taker_buy_quote_volume` | Fill with 0.0 |

## File Structure

```
quants-lab/
├── user_data/                          # Freqtrade download location
│   └── BTC_USDT-1m.feather            # Raw Freqtrade data
│
├── app/data/
│   ├── raw/freqtrade/gateio/          # Backup of raw data
│   │   └── BTC_USDT-1m.feather
│   │
│   └── cache/candles/                  # Converted QuantsLab format
│       └── gate_io|BTC-USDT|1m.parquet
│
└── scripts/
    └── import_freqtrade_data.py        # Import script
```

## Command-Line Arguments

### Required Arguments

- `--config`: Path to QuantsLab config YAML file
- `--days`: Number of days of historical data to download

### Optional Arguments

- `--timeframe`: Timeframe/interval (default: `1m`)
  - Common values: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`

## Examples

### Example 1: Initial Download for Base Ecosystem Tokens

```bash
# Download 6 days of 1m data (maximum for Gate.io 1m interval)
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 6 \
  --timeframe 1m
  
# Download 7 days of 5m data (recommended)
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 7 \
  --timeframe 5m
```

### Example 2: Test with Single Pair

```bash
# Edit config to have only one pair
# trading_pairs: ["VIRTUAL-USDT"]

# Download 7 days for testing
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 7 \
  --timeframe 1m
```

### Example 3: Incremental Historical Data with --prepend

```bash
# Step 1: Initial download (6 days)
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 6 \
  --timeframe 1m

# Step 2: Add older data (another 6 days before existing)
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 6 \
  --timeframe 1m \
  --prepend

# Result: Now you have ~12 days of data (if available on exchange)
```

### Example 4: Multi-Exchange Support

```bash
# Download from Gate.io (from config)
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 6 \
  --timeframe 1m

# Override to download from Binance
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 30 \
  --timeframe 5m \
  --exchange binance
```

## Troubleshooting

### Issue: "Config file not found"

**Solution**: Use absolute path or ensure you're in the project root:
```bash
cd /path/to/quants-lab
python scripts/import_freqtrade_data.py --config config/...
```

### Issue: "No trading_pairs found in config"

**Solution**: Ensure your config has the correct structure:
```yaml
tasks:
  task_name:
    config:
      trading_pairs:
        - "PAIR1-USDT"
```

### Issue: "Freqtrade file not found"

**Possible causes**:
1. Download failed (check network connection)
2. Wrong pair format (should be `BTC_USDT-1m.feather`)
3. Freqtrade couldn't find the pair on the exchange

**Solution**: Check Freqtrade output for errors

### Issue: "Validation failed: Contains NaN"

**Solution**: This indicates missing data from the exchange. Options:
1. Re-download the data
2. Accept the gaps (script will still convert)
3. Use data cleaning methods in QuantsLab

### Issue: "conda: command not found"

**Solution**: The script uses `conda run -n freqtrade`. Ensure:
1. Conda is installed
2. Freqtrade environment exists: `conda env list`
3. Run directly: `freqtrade download-data ...` (activate environment first)

## Data Validation

After import, the script validates:

1. **Column completeness**: All required columns present
2. **Data types**: All columns are float64
3. **Index format**: DatetimeIndex with correct timezone
4. **Timestamp continuity**: Data is sorted chronologically
5. **NaN detection**: Reports any missing values

## Integration with QuantsLab

After importing historical data:

1. **Test incremental update**:
   ```bash
   conda activate quants-lab
   python cli.py run-tasks --config config/base_ecosystem_downloader_full.yml
   ```

2. **Verify data is appended** (not replaced):
   ```bash
   python scripts/view_parquet.py "app/data/cache/candles/gate_io|VIRTUAL-USDT|1m.parquet"
   ```

3. **Set up scheduled updates**:
   - QuantsLab tasks will automatically fetch new data
   - No need to re-run Freqtrade import

## Performance Notes

- **Download time**: ~1-2 minutes per pair per 180 days (1m data)
- **Conversion time**: ~1-5 seconds per pair
- **Disk space**: ~50-100 KB per pair per 180 days (1m data, Parquet compressed)

## Best Practices

1. **Test first**: Start with 7 days and 1 pair to verify workflow
2. **Backup data**: Original Feather files are preserved in `app/data/raw/freqtrade/`
3. **Monitor disk space**: 25 pairs × 180 days ≈ 2-3 MB total
4. **Schedule regular imports**: For >180 days, re-run periodically
5. **Version control**: Don't commit data files (already in `.gitignore`)

## Adding More Historical Data

### Option 1: Use --prepend (Recommended)

Add older data before your existing data:

```bash
# Prepend another 6 days of data
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 6 \
  --timeframe 1m \
  --prepend

# Freqtrade will automatically:
# 1. Detect existing data's start date
# 2. Download data before that date
# 3. Merge seamlessly
```

### Option 2: Fresh Download

Delete existing files and redownload:

```bash
# Delete Freqtrade raw data
rm -rf user_data/data/gateio/*.feather

# Delete QuantsLab cache
rm -f app/data/cache/candles/gate_io*.parquet

# Redownload
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 6 \
  --timeframe 1m
```

## Automation (Optional)

Create a shell script for convenience:

```bash
#!/bin/bash
# scripts/full_import.sh

set -e

echo "=== Freqtrade Historical Data Import ==="
echo

# Activate freqtrade environment and download
conda run -n freqtrade python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 180 \
  --timeframe 1m

echo
echo "=== Testing QuantsLab Integration ==="
echo

# Test incremental update
conda run -n quants-lab python cli.py run-tasks \
  --config config/base_ecosystem_downloader_full.yml

echo
echo "✓ Import complete!"
```

Make executable: `chmod +x scripts/full_import.sh`

## Support

For issues or questions:
1. Check logs in the terminal output
2. Verify data with `scripts/view_parquet.py`
3. Review this documentation
4. Check Freqtrade documentation: https://www.freqtrade.io/

## Changelog

- **2025-10-09**: Initial implementation
  - Feather format support
  - Automatic conversion to QuantsLab format
  - Data validation and backup

