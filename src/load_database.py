from __future__ import annotations

from typing import Dict, Any

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def create_db_engine(database_url: str) -> Engine:
    """
    Create an SQLAlchemy engine from a database URL.
    """
    return create_engine(database_url, future=True)


def load_frames_to_db(
    frames: Dict[str, pd.DataFrame],
    sheets_cfg: Dict[str, Any],
    engine: Engine,
    if_exists: str = "replace",
) -> Dict[str, int]:
    """
    Write cleaned DataFrames into database tables.

    Parameters
    ----------
    frames:
        Mapping of sheet_name -> cleaned DataFrame.
    sheets_cfg:
        Mapping of sheet_name -> sheet_config; used to determine target table names.
    engine:
        SQLAlchemy Engine instance.
    if_exists:
        Passed through to DataFrame.to_sql (default 'replace').

    Returns
    -------
    dict:
        Mapping of table_name -> row_count_inserted
    """
    inserted_counts: Dict[str, int] = {}

    for sheet_name, df in frames.items():
        cfg = sheets_cfg.get(sheet_name, {})
        table_name = cfg.get("table", sheet_name)

        df.to_sql(
            table_name,
            engine,
            if_exists=if_exists,
            index=False,
        )
        inserted_counts[table_name] = len(df)

    return inserted_counts
