# Data Refresh Guide

This guide explains how to update the Materials Priority Tool with new data when updated reports become available.

## Data Sources

| Source | Update Frequency | URL |
|--------|------------------|-----|
| USGS Mineral Commodity Summaries | Annual (January) | https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries |
| DOE Critical Materials Assessment | Every 2-3 years | https://www.energy.gov/eere/vehicles/articles/critical-materials-assessment |
| World Bank Pink Sheet | Monthly | https://www.worldbank.org/en/research/commodity-markets |

## File Locations

All data files are located in the `data/` directory:

```
data/
├── raw/                    # Downloaded source files (gitignored)
│   ├── usgs/              # USGS Excel files
│   ├── worldbank/         # World Bank price data
│   └── doe/               # DOE assessment PDFs/data
├── processed/             # Generated outputs
│   ├── materials_master.csv    # Main scored dataset
│   ├── scoring_inputs.csv      # Intermediate values
│   └── price_history.csv       # Historical prices
└── reference/             # Manually curated data
    ├── materials_baseline.csv  # Core metrics per material
    ├── doe_criticality.csv     # DOE importance/risk scores
    └── kc_logistics.csv        # KC advantage factors
```

## Refresh Workflow

### Step 1: Update Reference Data

The primary file to update is `data/reference/materials_baseline.csv`. This contains the core metrics for each material.

**Columns to update:**

| Column | Source | Notes |
|--------|--------|-------|
| `import_reliance_pct` | USGS MCS, "Import Sources" section | Net import reliance as % of consumption |
| `top_producer` | USGS MCS, "World Production" table | Country with highest production |
| `top_producer_share_pct` | USGS MCS, "World Production" table | % of global production |
| `us_production_exists` | USGS MCS | True/False |
| `price_2024_usd` | USGS MCS, "Prices" section | Update year in column name |
| `5yr_price_change_pct` | Calculate from historical prices | (current - 5yr ago) / 5yr ago * 100 |
| `demand_growth_pct` | Industry reports, IEA forecasts | Projected annual growth |
| `market_size_bn` | Industry reports | Global market in $B |
| `technology_readiness` | Subjective 1-10 | Based on US production maturity |
| `capex_intensity` | Industry reports | 1-10 scale, higher = more capital intensive |

### Step 2: Update DOE Criticality (if new assessment released)

Edit `data/reference/doe_criticality.csv`:

| Column | Source |
|--------|--------|
| `importance_short` | DOE Assessment, short-term importance (1-4) |
| `risk_short` | DOE Assessment, short-term supply risk (1-4) |
| `importance_medium` | DOE Assessment, medium-term importance (1-4) |
| `risk_medium` | DOE Assessment, medium-term supply risk (1-4) |
| `criticality_category` | Derived: Critical, Near-Critical, or Lower-Risk |

### Step 3: Update KC Logistics (rarely changes)

Edit `data/reference/kc_logistics.csv` only if KC infrastructure changes significantly.

### Step 4: Regenerate Processed Data

Run the data processor to recalculate scores:

```bash
python -m src.data_processor
```

This will:
1. Load all reference CSVs
2. Calculate 5-factor scores
3. Generate composite scores and rankings
4. Write to `data/processed/materials_master.csv`

### Step 5: Verify and Deploy

1. **Test locally:**
   ```bash
   streamlit run app.py
   ```

2. **Run tests:**
   ```bash
   python -m pytest tests/ -v
   ```

3. **Commit and push:**
   ```bash
   git add data/reference/*.csv data/processed/*.csv
   git commit -m "Update data: [describe changes]"
   git push
   ```

4. Streamlit Cloud will auto-deploy.

## Adding Price History

To update the World Bank price history:

1. Download the latest Pink Sheet from World Bank
2. Save to `data/raw/worldbank/CMO-Historical-Data-Monthly.xlsx`
3. Run the data processor (it will extract relevant commodity prices)

## Troubleshooting

### Scores don't look right
- Check that `materials_baseline.csv` values are in correct units
- Verify percentages are 0-100, not decimals
- Run `python -m src.data_processor` to regenerate

### New material not appearing
- Ensure the material is added to all three reference files
- Material name must match exactly across files

### Tests failing after update
- Check that scores are still in 1-10 range
- Verify all 6 materials have data

## Version History

Track data updates in the commit messages:
- `Update data: USGS MCS 2025` — Annual USGS refresh
- `Update data: DOE Critical Materials 2025` — New DOE assessment
- `Update data: Q1 2025 prices` — Quarterly price update
