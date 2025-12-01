from __future__ import annotations

from typing import Dict, Any

from sqlalchemy import text
from sqlalchemy.engine import Engine


def validate_row_counts(
    engine: Engine,
    expected_rows: Dict[str, int],
) -> Dict[str, Any]:
    """
    Compare expected row counts against those in the database.

    expected_rows is a mapping of table_name -> expected_row_count.
    """
    results: Dict[str, Any] = {}
    with engine.connect() as conn:
        for table_name, expected in expected_rows.items():
            count = conn.execute(
                text(f"SELECT COUNT(*) FROM {table_name}")
            ).scalar_one()
            results[table_name] = {
                "expected": int(expected),
                "actual": int(count),
                "match": int(count) == int(expected),
            }
    return results


def summarise_validation(row_count_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Produce a simple summary from row count validation results.
    """
    total_tables = len(row_count_results)
    matching = sum(1 for r in row_count_results.values() if r["match"])
    return {
        "total_tables": total_tables,
        "matching_tables": matching,
        "all_match": matching == total_tables,
    }
