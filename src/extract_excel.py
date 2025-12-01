from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def extract_sheets(
    excel_path: Path,
    sheets_cfg: dict,
) -> Dict[str, pd.DataFrame]:
    """
    Read the configured sheets from an Excel workbook.

    Parameters
    ----------
    excel_path:
        Path to the Excel file.
    sheets_cfg:
        Mapping of sheet_name -> sheet_config.

    Returns
    -------
    dict:
        Mapping of sheet_name -> DataFrame
    """
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")

    frames: Dict[str, pd.DataFrame] = {}

    for sheet_name in sheets_cfg.keys():
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        frames[sheet_name] = df

    return frames
