from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Tuple

import pandas as pd

from .config import load_config
from .extract_excel import extract_sheets
from .transform_clean import transform_all
from .load_database import create_db_engine, load_frames_to_db
from .validate_data import validate_row_counts, summarise_validation
from .schema_design import describe_schema


def run_pipeline(
    config_path: str | Path,
    dry_run: bool = False,
    intermediate_dir: str | Path | None = "data/intermediate",
) -> Dict[str, Any]:
    """
    Run the full Excel -> DB pipeline.

    Steps:
      1. Load YAML config
      2. Extract sheets into DataFrames
      3. Transform / clean
      4. (If not dry_run) load into database
      5. (If not dry_run) validate row counts

    Returns:
      A dictionary containing high-level stats and validation summary.
    """
    cfg = load_config(config_path)
    excel_path: Path = cfg["excel_path"]
    database_url: str = cfg["database_url"]
    sheets_cfg: Dict[str, Any] = cfg["sheets"]

    if intermediate_dir is not None:
        intermediate_dir = Path(intermediate_dir)

    # 1) Extract
    frames_raw: Dict[str, pd.DataFrame] = extract_sheets(excel_path, sheets_cfg)

    # 2) Transform / clean
    cleaned_frames, transform_stats = transform_all(
        frames_raw,
        sheets_cfg,
        intermediate_dir=intermediate_dir,
    )

    # 3) Optional dry-run exit before touching DB
    if dry_run:
        return {
            "mode": "dry_run",
            "excel_path": str(excel_path),
            "database_url": database_url,
            "schema": describe_schema(sheets_cfg),
            "transform_stats": transform_stats,
            "load_stats": {},
            "row_counts": {},
            "validation_summary": {},
        }

    # 4) Load into database
    engine = create_db_engine(database_url)
    load_stats = load_frames_to_db(cleaned_frames, sheets_cfg, engine)

    # 5) Validate row counts
    row_counts = validate_row_counts(engine, load_stats)
    validation_summary = summarise_validation(row_counts)

    return {
        "mode": "full",
        "excel_path": str(excel_path),
        "database_url": database_url,
        "schema": describe_schema(sheets_cfg),
        "transform_stats": transform_stats,
        "load_stats": load_stats,
        "row_counts": row_counts,
        "validation_summary": validation_summary,
    }
