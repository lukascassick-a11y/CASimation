from __future__ import annotations

import re
import pandas as pd

TR_SENSOR_PATTERN = re.compile(r"\bTR(?:21|23|40|42|100|120)(?:[-A-Z0-9]*)?\b", re.IGNORECASE)


def is_tr_sylk_sensor(*, option: str = "", part_number: str = "") -> bool:
    """Identify supported Honeywell TR-series sensors connected by Sylk bus."""
    return bool(TR_SENSOR_PATTERN.search(f"{option} {part_number}"))


def build_sylk_device_library(parts: pd.DataFrame) -> pd.DataFrame:
    """Build the estimating library for Sylk-connected TR sensor products.

    Sylk devices remain billable material, consume one Sylk device address each,
    and consume zero physical AI/UI points.
    """
    columns = [
        "label", "manufacturer", "product_family", "device_type", "description",
        "supplier", "part_number", "unit_cost", "uses_sylk_bus",
        "consumes_ai_ui", "ai_ui_points", "sylk_device_count", "catalog_status",
    ]
    if parts.empty:
        return pd.DataFrame(columns=columns)

    frame = parts.copy()
    for column in ("option", "part_number", "supplier", "item", "category"):
        if column not in frame:
            frame[column] = ""
        frame[column] = frame[column].fillna("").astype(str)

    mask = frame.apply(
        lambda row: is_tr_sylk_sensor(option=row["option"], part_number=row["part_number"]), axis=1
    )
    frame = frame.loc[mask].copy()
    frame["price"] = pd.to_numeric(frame.get("price"), errors="coerce")
    frame["multiplier"] = pd.to_numeric(frame.get("multiplier"), errors="coerce").fillna(1.0)
    frame = frame.dropna(subset=["price"])

    rows = []
    for _, row in frame.iterrows():
        description = row["option"]
        part_number = row["part_number"]
        status = "Discontinued" if "discontinued" in f"{description} {part_number}".casefold() else "Active"
        rows.append({
            "label": f"{description} | {part_number} | {row['supplier']}",
            "manufacturer": "Honeywell",
            "product_family": "TR Series",
            "device_type": "Sylk Sensor",
            "description": description,
            "supplier": row["supplier"],
            "part_number": part_number,
            "unit_cost": float(row["price"]) * float(row["multiplier"]),
            "uses_sylk_bus": True,
            "consumes_ai_ui": False,
            "ai_ui_points": 0,
            "sylk_device_count": 1,
            "catalog_status": status,
        })

    return (
        pd.DataFrame(rows, columns=columns)
        .drop_duplicates(subset=["part_number", "description"])
        .sort_values(["catalog_status", "description", "part_number"])
        .reset_index(drop=True)
    )


def sylk_device_count(*, option: str = "", part_number: str = "", quantity: float = 1.0) -> float:
    """Return the Sylk address count contributed by a selected material line."""
    return float(quantity) if is_tr_sylk_sensor(option=option, part_number=part_number) else 0.0
