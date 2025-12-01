from __future__ import annotations

import pandas as pd

from src.transform_clean import clean_single_sheet


def test_clean_single_sheet_normalises_columns_and_drops_empty_rows():
    raw = pd.DataFrame(
        {
            "Customer ID": [1, 2, None],
            "Name": [" Alice ", "Bob", None],
            "Email": ["a@example.com", "b@example.com", None],
        }
    )

    cfg = {
        "index_column": "customer_id",
        "dtypes": {
            "customer_id": "int",
            "name": "string",
            "email": "string",
        },
    }

    cleaned, stats = clean_single_sheet(raw, "customers", cfg)

    # Column names normalised
    assert list(cleaned.columns) == ["customer_id", "name", "email"]
    # Empty row dropped
    assert len(cleaned) == 2
    # Stats reflect clean rows
    assert stats["rows_clean"] == 2
