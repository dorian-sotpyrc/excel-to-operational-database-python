from __future__ import annotations

from sqlalchemy import text

from src.load_database import create_db_engine
from src.validate_data import validate_row_counts, summarise_validation


def test_validate_row_counts_and_summary(tmp_path):
    db_path = tmp_path / "test.db"
    engine = create_db_engine(f"sqlite:///{db_path}")

    # Create simple table and insert 3 rows
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE demo (id INTEGER PRIMARY KEY, value TEXT)"))
        conn.execute(text("INSERT INTO demo (value) VALUES ('a'), ('b'), ('c')"))

    expected = {"demo": 3}
    rc = validate_row_counts(engine, expected)
    assert rc["demo"]["match"] is True
    summary = summarise_validation(rc)
    assert summary["all_match"] is True
    assert summary["total_tables"] == 1
    assert summary["matching_tables"] == 1
