# Migration notes and assumptions

This repository is meant as a *pattern* for moving from Excel to a proper
operational database, not as a one-size-fits-all tool. A few important
assumptions and design choices:

## 1. Excel workbook layout

We assume your workbook has:

- One sheet per logical entity (e.g., `customers`, `products`, `orders`).
- A header row with reasonably clear column names.
- Mostly tabular data (no heavily merged cells, complicated formulas, etc.).

If your workbook is more complex, consider:

- Creating a simplified export specifically for migration.
- Using a staging workbook where you standardise the structure.

## 2. Configuration-first

The YAML file in `config/config.yaml` is the authoritative description of:

- Where the Excel file lives (`excel_path`).
- Which database to target (`database_url`).
- How each sheet maps to a relational table (`sheets` → `table`, `index_column`, `dtypes`).

Changing the config is usually better than hard-coding logic in the Python
modules.

## 3. Data types and coercion

Type conversion is *best effort*:

- Non-convertible values become `NaN` / `NaT` / `None` via pandas.
- Integer columns use the nullable `Int64` dtype.
- Dates are parsed with `pd.to_datetime(errors="coerce")`.

You may want to tighten this for production by:

- Rejecting rows with invalid types.
- Logging or exporting "rejected" rows for manual review.

## 4. Loading and replacing data

By default, the loader uses `if_exists="replace"` with `DataFrame.to_sql`.
That means:

- Each run replaces the target table content.
- The schema is inferred by the underlying database and SQLAlchemy.

For more advanced usage, you might:

- Switch to `if_exists="append"` for incremental loads.
- Declare explicit SQLAlchemy models and use them to create the schema.
- Add migrations for schema evolution.

## 5. Validation strategy

We start with a simple validation strategy:

- Compare expected row counts (from the load step) with live counts in the DB.
- Optionally extend this to:
  - Foreign key checks.
  - Unique constraints.
  - Domain checks (allowed values, ranges).

Treat `src/validate_data.py` as a place to grow your own quality rules.

## 6. Operations and scheduling

This repo does **not** schedule or orchestrate the pipeline; it just exposes:

    python -m src.cli migrate --config config/config.yaml

You can connect this to:

- A cron job
- A CI pipeline
- A simple task scheduler

so that your Excel → DB migration becomes repeatable and predictable.
