from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Tuple

import pandas as pd


def _normalise_column_name(name: str) -> str:
    """
    Normalise Excel column headers:
    - strip spaces
    - lowercase
    - replace spaces and dashes with underscores
    """
    return (
        str(name)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def _apply_type(df: pd.DataFrame, column: str, kind: str) -> pd.Series:
    """
    Convert a column to the configured datatype. Unknown types are left unchanged.
    """
    kind = kind.lower()
    series = df[column]

    if kind in {"int", "integer"}:
        series = pd.to_numeric(series, errors="coerce").astype("Int64")
    elif kind in {"float", "decimal", "number"}:
        series = pd.to_numeric(series, errors="coerce")
    elif kind in {"string", "str", "text"}:
        series = series.astype("string").str.strip()
    elif kind in {"bool", "boolean"}:
        series = series.astype("boolean")
    elif kind in {"date", "datetime"}:
        series = pd.to_datetime(series, errors="coerce")
    elif kind in {"category", "categorical"}:
        series = series.astype("category")
    # else: leave unchanged

    return series


def clean_single_sheet(
    df_raw: pd.DataFrame,
    sheet_name: str,
    cfg: Dict[str, Any],
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Clean a single sheet according to configuration.

    Steps:
    - Normalise column names
    - Restrict to declared columns (optional)
    - Convert types
    - Drop fully empty rows
    """
    df = df_raw.copy()

    # 1) Normalise column names
    df.columns = [_normalise_column_name(c) for c in df.columns]

    # 2) Apply dtype conversions
    dtypes_cfg: Dict[str, str] = cfg.get("dtypes", {}) or {}
    if dtypes_cfg:
        missing = [c for c in dtypes_cfg.keys() if c not in df.columns]
        if missing:
            raise ValueError(
                f"Sheet '{sheet_name}' missing expected columns: {missing}"
            )

        # Restrict to configured columns
        df = df[list(dtypes_cfg.keys())]

        # Convert types
        for col, kind in dtypes_cfg.items():
            df[col] = _apply_type(df, col, kind)

    # 3) Drop fully empty rows
    df = df.dropna(how="all").reset_index(drop=True)

    # 4) Validate index column presence
    index_col = cfg.get("index_column")
    if index_col and index_col not in df.columns:
        raise ValueError(
            f"index_column '{index_col}' not found in cleaned sheet '{sheet_name}'"
        )

    return df, {"rows_clean": len(df)}


def transform_all(
    frames: Dict[str, pd.DataFrame],
    sheets_cfg: Dict[str, Any],
    intermediate_dir: Path | None = None,
) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Dict[str, Any]]]:
    """
    Apply cleaning to all sheets and optionally write intermediate CSVs.

    Returns:
        cleaned_frames: sheet_name -> cleaned DataFrame
        stats: sheet_name -> stats dict
    """
    cleaned: Dict[str, pd.DataFrame] = {}
    stats: Dict[str, Dict[str, Any]] = {}

    if intermediate_dir is not None:
        intermediate_dir.mkdir(parents=True, exist_ok=True)

    for sheet_name, df in frames.items():
        cfg = sheets_cfg.get(sheet_name, {})
        clean_df, sheet_stats = clean_single_sheet(df, sheet_name, cfg)
        cleaned[sheet_name] = clean_df
        stats[sheet_name] = sheet_stats

        if intermediate_dir is not None:
            out_path = intermediate_dir / f"{sheet_name}_clean.csv"
            clean_df.to_csv(out_path, index=False)

    return cleaned, stats
