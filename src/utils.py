"""Utility functions for Materials Priority Tool."""

import io
from pathlib import Path
from typing import Any
from datetime import datetime

import pandas as pd


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists, create if not.

    Args:
        path: Directory path

    Returns:
        The path (created if needed)
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format a decimal as percentage string.

    Args:
        value: Value to format (0-100 scale or 0-1 scale)
        decimals: Number of decimal places

    Returns:
        Formatted percentage string
    """
    if value <= 1:
        value = value * 100
    return f"{value:.{decimals}f}%"


def format_currency(value: float, prefix: str = "$", suffix: str = "") -> str:
    """Format number as currency.

    Args:
        value: Value to format
        prefix: Currency prefix (default: $)
        suffix: Optional suffix (e.g., 'B' for billions)

    Returns:
        Formatted currency string
    """
    if value >= 1e9:
        return f"{prefix}{value/1e9:.1f}B{suffix}"
    elif value >= 1e6:
        return f"{prefix}{value/1e6:.1f}M{suffix}"
    elif value >= 1e3:
        return f"{prefix}{value/1e3:.1f}K{suffix}"
    else:
        return f"{prefix}{value:.2f}{suffix}"


def normalize_score(value: float, min_val: float, max_val: float, target_min: float = 1, target_max: float = 10) -> float:
    """Normalize a value to target score range.

    Args:
        value: Value to normalize
        min_val: Minimum value in original range
        max_val: Maximum value in original range
        target_min: Minimum of target range (default: 1)
        target_max: Maximum of target range (default: 10)

    Returns:
        Normalized value in target range
    """
    if max_val == min_val:
        return (target_min + target_max) / 2

    normalized = (value - min_val) / (max_val - min_val)
    scaled = normalized * (target_max - target_min) + target_min
    return max(target_min, min(target_max, scaled))


def calculate_yoy_change(df: pd.DataFrame, value_col: str, date_col: str = "date") -> float:
    """Calculate year-over-year change percentage.

    Args:
        df: DataFrame with time series data
        value_col: Column name for values
        date_col: Column name for dates

    Returns:
        YoY change as percentage
    """
    df = df.sort_values(date_col)
    if len(df) < 2:
        return 0.0

    latest = df[value_col].iloc[-1]
    year_ago_idx = len(df) - 13 if len(df) > 12 else 0  # ~12 months ago
    year_ago = df[value_col].iloc[year_ago_idx]

    if year_ago == 0:
        return 0.0

    return ((latest - year_ago) / year_ago) * 100


def calculate_volatility(df: pd.DataFrame, value_col: str) -> dict[str, float]:
    """Calculate volatility metrics for a time series.

    Args:
        df: DataFrame with time series data
        value_col: Column name for values

    Returns:
        Dictionary with std, cv (coefficient of variation), and range
    """
    values = df[value_col].dropna()
    if len(values) < 2:
        return {"std": 0, "cv": 0, "range": 0}

    std = values.std()
    mean = values.mean()
    cv = (std / mean * 100) if mean != 0 else 0
    value_range = values.max() - values.min()

    return {
        "std": round(std, 2),
        "cv": round(cv, 2),
        "range": round(value_range, 2),
    }


def get_color_for_score(score: float) -> str:
    """Get color code based on score value.

    Args:
        score: Score value (1-10)

    Returns:
        Hex color code
    """
    if score >= 7:
        return "#2ca02c"  # Green - high priority
    elif score >= 4:
        return "#ff7f0e"  # Orange - medium priority
    else:
        return "#d62728"  # Red - lower priority


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text with ellipsis if too long.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def export_to_csv(df: pd.DataFrame) -> bytes:
    """Export DataFrame to CSV bytes.

    Args:
        df: DataFrame to export

    Returns:
        CSV data as bytes
    """
    return df.to_csv(index=False).encode('utf-8')


def export_to_excel(df: pd.DataFrame, sheet_name: str = "Materials Data") -> bytes:
    """Export DataFrame to Excel bytes.

    Args:
        df: DataFrame to export
        sheet_name: Name for the Excel sheet

    Returns:
        Excel data as bytes
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    return output.getvalue()


def generate_pdf_report(df: pd.DataFrame, title: str = "Materials Priority Report") -> bytes:
    """Generate a PDF report from materials data.

    Args:
        df: DataFrame with materials data
        title: Report title

    Returns:
        PDF data as bytes
    """
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(5)

    # Date
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
    pdf.ln(10)

    # Executive Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Priority Rankings", ln=True)
    pdf.ln(2)

    # Rankings table
    pdf.set_font("Helvetica", "B", 9)
    col_widths = [15, 35, 25, 25, 25, 30, 35]
    headers = ["Rank", "Material", "Score", "Supply Risk", "Market Opp.", "KC Advantage", "Criticality"]

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    for _, row in df.iterrows():
        pdf.cell(col_widths[0], 8, str(int(row.get('rank', 0))), border=1, align="C")
        pdf.cell(col_widths[1], 8, str(row.get('material', '')), border=1)
        pdf.cell(col_widths[2], 8, f"{row.get('composite_score', 0):.2f}", border=1, align="C")
        pdf.cell(col_widths[3], 8, f"{row.get('supply_risk_score', 0):.1f}", border=1, align="C")
        pdf.cell(col_widths[4], 8, f"{row.get('market_opportunity_score', 0):.1f}", border=1, align="C")
        pdf.cell(col_widths[5], 8, f"{row.get('kc_advantage_score', 0):.1f}", border=1, align="C")
        pdf.cell(col_widths[6], 8, str(row.get('criticality_category', '')), border=1, align="C")
        pdf.ln()

    pdf.ln(10)

    # Key Findings
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Key Findings", ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 10)
    top_material = df.iloc[0] if len(df) > 0 else None
    if top_material is not None:
        pdf.multi_cell(0, 6, f"1. Top Priority: {top_material['material']} with composite score of {top_material['composite_score']:.2f}")
        pdf.ln(2)

    # Count critical materials
    critical_count = len(df[df['criticality_category'] == 'Critical']) if 'criticality_category' in df.columns else 0
    pdf.multi_cell(0, 6, f"2. {critical_count} materials rated as 'Critical' by DOE assessment")
    pdf.ln(2)

    # High import reliance
    high_import = df[df['import_reliance_pct'] >= 75] if 'import_reliance_pct' in df.columns else pd.DataFrame()
    if len(high_import) > 0:
        materials_list = ", ".join(high_import['material'].tolist())
        pdf.multi_cell(0, 6, f"3. High import reliance (>=75%): {materials_list}")

    pdf.ln(10)

    # Footer
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(0, 10, "Data sources: USGS Mineral Commodity Summaries, DOE Critical Materials Assessment", ln=True)

    return bytes(pdf.output())
