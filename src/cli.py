from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import run_pipeline


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Migrate an Excel workbook into a relational database using Python."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    migrate = subparsers.add_parser(
        "migrate",
        help="Run the Excel -> DB migration pipeline.",
    )
    migrate.add_argument(
        "--config",
        "-c",
        type=str,
        default="config/config.yaml",
        help="Path to the YAML configuration file (default: config/config.yaml).",
    )
    migrate.add_argument(
        "--dry-run",
        action="store_true",
        help="Run extract/transform only, without writing to the database.",
    )
    migrate.add_argument(
        "--json",
        action="store_true",
        help="Print a JSON summary instead of human-readable text.",
    )

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "migrate":
        result = run_pipeline(args.config, dry_run=args.dry_run)

        if args.json:
            print(json.dumps(result, indent=2, default=str))
            return

        # Human-readable summary
        print(f"Mode: {result['mode']}")
        print(f"Excel: {result['excel_path']}")
        print(f"Database: {result['database_url']}")
        print()
        print("Configured schema:")
        print(result["schema"])
        print("Transform stats:")
        for sheet, stats in result["transform_stats"].items():
            print(f"  - {sheet}: {stats}")

        if result["mode"] == "dry_run":
            print("\nDry-run complete (no changes written to the database).")
            return

        print("\nLoad stats:")
        for table, count in result["load_stats"].items():
            print(f"  - {table}: inserted {count} rows")

        print("\nRow count validation:")
        for table, rc in result["row_counts"].items():
            status = "OK" if rc["match"] else "MISMATCH"
            print(
                f"  - {table}: expected={rc['expected']} "
                f"actual={rc['actual']} [{status}]"
            )

        summary = result["validation_summary"]
        print(
            f"\nValidation summary: {summary['matching_tables']} / "
            f"{summary['total_tables']} tables match."
        )
        if summary["all_match"]:
            print("All table row counts match expected values.")
        else:
            print("Some tables do not match expected row counts.")
    else:
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
