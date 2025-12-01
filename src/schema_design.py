from __future__ import annotations

from typing import Dict, Any


def describe_schema(sheets_cfg: Dict[str, Any]) -> str:
    """
    Produce a simple human-readable description of the configured schema.

    This is useful for logging and for explaining the structure in documentation.
    """
    lines: list[str] = []
    for sheet_name, cfg in sheets_cfg.items():
        table = cfg.get("table", sheet_name)
        index_column = cfg.get("index_column", "<none>")
        dtypes = cfg.get("dtypes", {}) or {}

        lines.append(f"Table: {table}")
        lines.append(f"  Source sheet: {sheet_name}")
        lines.append(f"  Index column: {index_column}")

        if dtypes:
            lines.append("  Columns:")
            for col, kind in dtypes.items():
                lines.append(f"    - {col}: {kind}")
        lines.append("")

    return "\n".join(lines)
