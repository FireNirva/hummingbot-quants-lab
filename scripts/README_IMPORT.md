# Quick Import Guide

## Quick Start

### Download 180 days for all configured pairs

```bash
conda activate freqtrade
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 180 \
  --timeframe 1m
```

### Test with one pair first

```bash
conda activate freqtrade
python scripts/import_freqtrade_data.py \
  --config config/test_import.yml \
  --days 7 \
  --timeframe 1m
```

### Verify imported data

```bash
python scripts/view_parquet.py --all
```

### Test QuantsLab integration

```bash
conda activate quants-lab
python cli.py run-tasks --config config/base_ecosystem_downloader_full.yml
```

## Files Created

- **Raw data**: `user_data/*.feather` (Freqtrade format)
- **Backup**: `app/data/raw/freqtrade/gateio/*.feather`
- **Converted**: `app/data/cache/candles/gate_io|*|1m.parquet`

## Full Documentation

See `docs/FREQTRADE_IMPORT.md` for complete documentation.

## Troubleshooting

If download fails, check:
1. Freqtrade environment is activated
2. Network connection
3. Pair exists on Gate.io

If conversion fails:
1. Check Freqtrade downloaded the data (`ls user_data/*.feather`)
2. Verify file format matches expected structure
3. Check logs for specific error messages

