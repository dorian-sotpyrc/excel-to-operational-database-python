Absolutely — here is the full, clean **README.md**, without commentary, without wrappers, exactly as a copy-paste GitHub file.

---

# Excel to Operational Database with Python

Turn a messy Excel workbook into a clean, relational SQLite database using Python, pandas, and SQLAlchemy — with repeatable ETL steps and built-in validation.

## Why this project exists

Spreadsheets are excellent for quick modelling — but fragile as a source of truth:

* Conflicting versions in email drives
* Hidden formula errors
* No foreign keys, no constraints
* Difficult collaboration and auditing

This project provides a **practical, production-ready pattern** for migrating an Excel workbook into a proper database. It is intentionally lightweight, readable, and focused on real-world migration steps you can adapt to your own data.

This repository accompanies the PLEX article:

> **Migrating an Excel Spreadsheet into a Fully Fledged Operational Database with Python**
> [https://plexdata.online/post/migrating-excel-to-database-python](https://plexdata.online/post/migrating-excel-to-database-python) *(placeholder)*

---

## Features

* **End-to-end ETL pipeline:** Extract → Transform → Load → Validate
* **Python-native workflow** using `pandas` and `SQLAlchemy`
* **Relational schema** with primary keys and foreign key relationships
* **Config-driven** (YAML): map Excel sheets to tables with types
* **Repeatable migrations** with dry-run mode
* **Intermediate data dumps** for debugging
* **Tests included** for cleaning and validation
* **Easily switch target DB** (SQLite → PostgreSQL → MySQL → SQL Server)

---

## Architecture overview

```
            ┌───────────────────┐
            │   Excel workbook   │
            │   (multi-sheet)    │
            └─────────┬─────────┘
                      │
                      ▼
            Extract with pandas.read_excel
                      │
                      ▼
              ┌───────────────┐
              │  DataFrames   │
              │   (staging)   │
              └──────┬────────┘
                     │
          Transform / Clean (types, columns, NULLs)
                     │
                     ▼
              ┌───────────────┐
              │ Normalised     │
              │ DataFrames     │
              └──────┬────────┘
                     │
                     ▼
            Load with SQLAlchemy / to_sql
                     │
                     ▼
              ┌───────────────┐
              │   SQLite DB   │
              │    app.db     │
              └──────┬────────┘
                     │
                     ▼
              Validation (FKs, row counts, nulls)
```

---

## Project structure

```
excel-to-operational-database-python/
├── src/
│   ├── cli.py
│   ├── config.py
│   ├── extract_excel.py
│   ├── transform_clean.py
│   ├── load_database.py
│   ├── validate_data.py
│   ├── models.py
│   ├── schema_design.py
│   └── pipeline.py
├── data/
│   ├── raw/
│   │   └── sample_workbook.xlsx
│   ├── intermediate/
│   │   ├── customers_clean.csv
│   │   ├── products_clean.csv
│   │   └── orders_clean.csv
│   └── db/
│       └── app.db
├── config/
│   └── config.example.yaml
├── docs/
│   ├── schema-diagram.md
│   └── migration-notes.md
├── notebooks/
│   └── 01_exploratory_excel.ipynb
├── tests/
│   ├── test_transform_clean.py
│   └── test_validate_data.py
├── .gitignore
├── requirements.txt or pyproject.toml
├── README.md
└── LICENSE
```

---

## Installation

### 1. Clone and enter the project

```bash
git clone https://github.com/YOUR-USER/excel-to-operational-database-python.git
cd excel-to-operational-database-python
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Copy the example config:

```bash
cp config/config.example.yaml config/config.yaml
```

Open the new file and adjust:

* Path to your Excel workbook
* Target database URL
* Sheet → table mappings
* Explicit or inferred data types
* Index/primary key columns

### Example config

```yaml
excel_path: "data/raw/sample_workbook.xlsx"
database_url: "sqlite:///data/db/app.db"

sheets:
  customers:
    table: customers
    index_column: customer_id
    dtypes:
      customer_id: int
      name: string
      email: string
      joined_date: date

  products:
    table: products
    index_column: product_id
    dtypes:
      product_id: int
      name: string
      category: string
      unit_price: decimal

  orders:
    table: orders
    index_column: order_id
    dtypes:
      order_id: int
      customer_id: int
      product_id: int
      order_date: date
      quantity: int
```

---

## Running the migration

### Basic run

```bash
python -m src.cli migrate --config config/config.yaml
```

This runs the entire pipeline:

1. **Extract** sheets from Excel into pandas DataFrames
2. **Transform** (clean, normalise, convert types)
3. **Load** into SQLite via SQLAlchemy
4. **Validate** (row counts, foreign keys, null rules)

### Dry run (no database writes)

```bash
python -m src.cli migrate --config config/config.yaml --dry-run
```

### Rebuild the database

```bash
rm -f data/db/app.db
python -m src.cli migrate --config config/config.yaml
```

---

## Key Python modules

### `extract_excel.py`

* Reads sheets via `pandas.read_excel`
* Returns a `{sheet_name: DataFrame}` mapping
* Writes optional staging CSVs for debugging

### `transform_clean.py`

Handles:

* Column name normalisation
* Data type conversion
* Trimming strings
* Dropping empty rows
* Simple domain cleaning (e.g., category mapping)

### `load_database.py`

* Connects via SQLAlchemy
* Creates tables if missing
* Bulk-loads DataFrames via `to_sql` or typed inserts
* Supports multiple RDBMS engines

### `validate_data.py`

* Row count checks
* Foreign key consistency
* Null constraints
* Optional custom checks per table

### `pipeline.py`

The orchestrator for:

```
extract → transform → load → validate
```

Used by the CLI and tests.

---

## Extending to other databases

Swap out the SQLAlchemy URL:

**PostgreSQL:**

```
postgresql+psycopg2://user:pass@localhost:5432/mydb
```

**MySQL/MariaDB:**

```
mysql+pymysql://user:pass@localhost:3306/mydb
```

**SQL Server:**

```
mssql+pyodbc://user:pass@dsn_name
```

If the driver is installed, the pipeline works the same.

---

## Relationship to the PLEX article

This repository contains:

* The exact folder structure described in the tutorial
* Sample Excel data
* Matching Python scripts
* Example config and validation rules

Readers of the PLEX article can clone this repo and **run the migration themselves** without rebuilding everything from scratch.
---

## License

Released under the **MIT License**.

