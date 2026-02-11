# Data Sources Documentation

This document provides complete provenance for all data used in the Materials Priority Tool.

**Last Updated:** 2026-02-10

---

## Data Integrity Standards

All data in this project must meet one of these standards:

1. **Directly Citable:** Source document, page/table reference, anyone can look it up
2. **Reproducible Calculation:** Formula + inputs documented, anyone can redo and get same result
3. **Clearly Labeled Estimate:** Methodology documented, marked as "estimate" in data

Data that cannot meet these standards has been removed or flagged for remediation.

---

## Source Documents Inventory

### USGS Sources (Primary)

| Document | Local File | Downloaded |
|----------|------------|------------|
| Mineral Commodity Summaries 2024 (Full) | `data/raw/usgs/mcs2024-full.pdf` | ✅ 2026-02-10 |
| Mineral Commodity Summaries 2025 (Full) | `data/raw/usgs/mcs2025-full.pdf` | ✅ 2026-02-10 |
| MCS 2024 - Lithium | `data/raw/usgs/mcs2024-lithium.pdf` | ✅ 2026-02-10 |
| MCS 2024 - Cobalt | `data/raw/usgs/mcs2024-cobalt.pdf` | ✅ 2026-02-10 |
| MCS 2024 - Nickel | `data/raw/usgs/mcs2024-nickel.pdf` | ✅ 2026-02-10 |
| MCS 2024 - Graphite | `data/raw/usgs/mcs2024-graphite.pdf` | ✅ 2026-02-10 |
| MCS 2024 - Manganese | `data/raw/usgs/mcs2024-manganese.pdf` | ✅ 2026-02-10 |
| MCS 2024 - Rare Earths | `data/raw/usgs/mcs2024-rare-earths.pdf` | ✅ 2026-02-10 |
| MCS 2024 - Copper | `data/raw/usgs/mcs2024-copper.pdf` | ✅ 2026-02-10 |
| MCS 2024 - Platinum Group | `data/raw/usgs/mcs2024-platinum-group.pdf` | ✅ 2026-02-10 |
| MCS 2024 - Gallium | `data/raw/usgs/mcs2024-gallium.pdf` | ✅ 2026-02-10 |
| MCS 2024 - Vanadium | `data/raw/usgs/mcs2024-vanadium.pdf` | ✅ 2026-02-10 |
| MCS 2024 - Tin | `data/raw/usgs/mcs2024-tin.pdf` | ✅ 2026-02-10 |
| MCS 2024 - Tungsten | `data/raw/usgs/mcs2024-tungsten.pdf` | ✅ 2026-02-10 |
| MCS 2024 - Zinc | `data/raw/usgs/mcs2024-zinc.pdf` | ✅ 2026-02-10 |
| Minerals Yearbook 2022 - Lithium | `data/raw/usgs/lithium_myb2022.xlsx` | ✅ |
| Minerals Yearbook 2022 - Cobalt | `data/raw/usgs/cobalt_myb2022.xlsx` | ✅ |
| Minerals Yearbook 2022 - Nickel | `data/raw/usgs/nickel_myb2022.xlsx` | ✅ |
| Minerals Yearbook 2022 - Graphite | `data/raw/usgs/graphite_myb2022.xlsx` | ✅ |
| Minerals Yearbook 2022 - Manganese | `data/raw/usgs/manganese_myb2022.xlsx` | ✅ |
| Minerals Yearbook 2022 - Rare Earths | `data/raw/usgs/rareearths_myb2022.xlsx` | ✅ |

### DOE Sources

| Document | Local File | Downloaded |
|----------|------------|------------|
| Critical Materials Assessment 2023 | `data/raw/doe/doe-critical-materials-assessment-2023.pdf` | ✅ 2026-02-10 |

### KC Infrastructure Sources

| Document | Local File | Downloaded |
|----------|------------|------------|
| MoDOT Freight Railroads | `data/raw/sources/modot/freight-railroads.html` | ✅ 2026-02-10 |
| FHWA Highway Statistics 2023 | `data/raw/sources/fhwa/hm81-highway-statistics-2023.html` | ✅ 2026-02-10 |
| Port KC Investment (KSHB) | `data/raw/sources/port_kc/kshb-port-kc-37million-2023.html` | ✅ 2026-02-10 |
| Port KC Investment (Marine Log) | `data/raw/sources/port_kc/marinelog-port-kc-2023.html` | ✅ 2026-02-10 |

### Market Data Sources

| Document | Local File | Downloaded |
|----------|------------|------------|
| World Bank CMO Historical Data | `data/raw/worldbank/CMO-Historical-Data-Monthly.xlsx` | ✅ |

**Note:** World Bank data covers Nickel, Copper, Aluminum, Iron ore. Does NOT include Lithium, Cobalt, Graphite, Rare Earths.

---

## Verified Data Files

### `data/reference/materials_baseline_verified.csv` (NEW)

Extracted from USGS MCS 2024 PDFs with full source attribution.

| Field | Source | Status |
|-------|--------|--------|
| `material` | Definition | ✅ Verified |
| `import_reliance_pct` | USGS MCS 2024 | ✅ Verified |
| `top_producer` | USGS MCS 2024 | ✅ Verified |
| `top_producer_share_pct` | USGS MCS 2024 | ✅ Verified |
| `us_production_exists` | USGS MCS 2024 | ✅ Verified |

### `data/reference/usgs_import_reliance_2024.csv` (NEW)

Import reliance data extracted from individual USGS MCS 2024 PDFs.

| Material | Import Reliance (2023) | Source PDF |
|----------|------------------------|------------|
| Lithium | >25% | mcs2024-lithium.pdf |
| Cobalt | 67% | mcs2024-cobalt.pdf |
| Nickel | 49% | mcs2024-nickel.pdf |
| Graphite | 100% | mcs2024-graphite.pdf |
| Manganese | 100% | mcs2024-manganese.pdf |
| Rare Earths | >95% | mcs2024-rare-earths.pdf |
| Copper | 46% | mcs2024-copper.pdf |
| Platinum Group | 83% | mcs2024-platinum-group.pdf |
| Gallium | 100% | mcs2024-gallium.pdf |
| Vanadium | 58% | mcs2024-vanadium.pdf |
| Tin | 74% | mcs2024-tin.pdf |
| Tungsten | >50% | mcs2024-tungsten.pdf |
| Zinc | 77% | mcs2024-zinc.pdf |

### `data/reference/doe_criticality_verified.csv` (NEW)

Criticality categories from DOE Critical Materials Assessment 2023.

| Material | Short-Term (2020-2025) | Medium-Term (2025-2035) |
|----------|------------------------|-------------------------|
| Lithium | Near-Critical | Critical |
| Cobalt | Critical | Critical |
| Nickel | Near-Critical | Critical |
| Graphite | Critical | Critical |
| Rare Earths | Critical | Critical |
| Copper | Not-Critical | Near-Critical |
| Platinum Group | Near-Critical | Critical |
| Gallium | Critical | Critical |
| Manganese | Not-Evaluated | Not-Evaluated |
| Vanadium | Not-Evaluated | Not-Evaluated |
| Tin | Not-Evaluated | Not-Evaluated |
| Tungsten | Not-Evaluated | Not-Evaluated |
| Zinc | Not-Evaluated | Not-Evaluated |

**Note:** DOE evaluated 23 of 38 materials. Manganese, Vanadium, Tin, Tungsten, Zinc were not in the top 23.

### `data/reference/kc_infrastructure.csv` (NEW)

Factual KC infrastructure data with source attribution.

| Category | Metric | Value | Source |
|----------|--------|-------|--------|
| Rail | KC rail hub national rank | 2nd | MoDOT |
| Rail | Missouri state track miles | 3,800 | MoDOT |
| Rail | Missouri freight tonnage rank | 4th nationally | MoDOT |
| Highway | Missouri state highway miles | 33,811 | FHWA |
| Highway | Missouri highway ranking | ~6th nationally | FHWA |
| Waterway | KC Midwest port rank | 2nd (behind Chicago) | KSHB |
| Waterway | Port KC investment (FY2024) | $37 million | KSHB |
| Waterway | Total project investment | $550 million | KSHB |

---

## Deprecated/Unverified Files

### `data/reference/materials_baseline.csv` (ORIGINAL)

**Status:** ⚠️ DEPRECATED - Contains unverified data

| Field | Status | Issue |
|-------|--------|-------|
| `price_2024_usd` | ❌ Unverified | No source documented |
| `5yr_price_change_pct` | ❌ Unverified | No source documented |
| `demand_growth_pct` | ❌ Unverified | No source documented |
| `market_size_bn` | ❌ Unverified | No source documented |
| `technology_readiness` | ❌ Remove | Subjective, no methodology |
| `capex_intensity` | ❌ Remove | Subjective, no methodology |

### `data/reference/doe_criticality.csv` (ORIGINAL)

**Status:** ⚠️ DEPRECATED - Replace with `doe_criticality_verified.csv`

The original file used numeric 1-4 scores. DOE actually uses categorical designations (Critical, Near-Critical, Not-Critical).

### `data/reference/kc_logistics.csv` (ORIGINAL)

**Status:** ❌ DEPRECATED - Subjective 1-10 scores without methodology

Replace with `kc_infrastructure.csv` which contains only verifiable facts.

---

## Remaining Data Gaps

### Price Data
- USGS MCS 2024 contains price data in PDFs (e.g., Lithium carbonate $46,000/ton in 2023)
- World Bank covers: Nickel, Copper, Aluminum (not Lithium, Cobalt, Graphite)
- **Recommendation:** Extract prices from USGS MCS 2024 PDFs and document

### Demand Growth Forecasts
- Not available from government sources
- Would require IEA, BloombergNEF, or industry reports
- **Recommendation:** Remove from scoring or clearly mark as industry estimate

### Market Size
- Not available from government sources
- Would require market research reports
- **Recommendation:** Remove from scoring or clearly mark as industry estimate

---

## Remediation Checklist

- [x] Download USGS MCS 2024 PDFs for all 13 materials
- [x] Download USGS MCS 2025 full report
- [x] Download DOE Critical Materials Assessment 2023 PDF
- [x] Download KC infrastructure source documents
- [x] Extract import reliance data from USGS MCS 2024
- [x] Create verified materials baseline file
- [x] Create verified DOE criticality file
- [x] Create verified KC infrastructure file
- [x] Remove technology_readiness and capex_intensity from scoring
- [x] Update data_processor.py to use verified files
- [x] Update dashboard pages to reflect new data structure
- [x] Decide on handling of demand_growth_pct and market_size_bn (REMOVED - unverifiable)
- [ ] Extract price data from USGS MCS 2024 PDFs (optional - for future enhancement)
