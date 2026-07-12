from __future__ import annotations

import re
import pandas as pd

HONEYWELL_DEFAULT_CONTROLLERS = {
    "VAV": "VAA-VA75MB24NMC",
    "Fan Coil": "UN-RS0844MS24NMC",
    "Unit Ventilator": "UN-RS0844MS24NMC",
    "Heat Pump": "UN-RS0844MS24NMC",
    "AHU": "UN-RL1644MS24NMC",
    "Boiler": "UN-RL1644MS24NMC",
    "Chiller": "UN-RL1644MS24NMC",
    "Pump": "UN-RL1644MS24NMC",
    "Other": "UN-RL1644MS24NMC",
}

JOHNSON_CONTROLS_DEFAULT_CONTROLLERS = {
    "VAV": "F4-CVM3050-0",
    "Fan Coil": "F4-CGM09090-0",
    "Unit Ventilator": "F4-CGM09090-0",
    "Heat Pump": "F4-CGM09090-0",
    "AHU": "F4-CGM09090-0",
    "Boiler": "F4-CGM09090-0",
    "Chiller": "F4-CGM09090-0",
    "Pump": "F4-CGM09090-0",
    "Other": "F4-CGM09090-0",
}

DEFAULT_CONTROLLERS = HONEYWELL_DEFAULT_CONTROLLERS
SUPPORTED_MANUFACTURERS = ("Honeywell", "Johnson Controls", "Phoenix Controls")


def normalize_manufacturer(value: str) -> str:
    text = str(value or "").strip()
    folded = text.casefold()
    if "honeywell" in folded:
        return "Honeywell"
    if folded in {"jci", "johnson controls", "johnson control"} or "johnson" in folded or re.search(r"\bjci\b", folded):
        return "Johnson Controls"
    if "phoenix" in folded:
        return "Phoenix Controls"
    return text


def normalize_optimizer(value: str) -> str:
    return re.sub(r"optimzer", "Optimizer", str(value or ""), flags=re.IGNORECASE)


def lifecycle_status(part_number: str, supplier: str, description: str) -> str:
    pn = str(part_number or "").upper()
    text = f"{supplier} {description} {pn}".upper()
    if "SIEMENS" in text:
        return "Removed"
    if pn.startswith("FX-"):
        return "Legacy"
    return "Active"


def build_controller_catalog(parts: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "manufacturer", "family", "description", "part_number", "supplier",
        "unit_cost", "catalog_status", "selectable", "default_for",
    ]
    if parts.empty:
        return pd.DataFrame(columns=columns)
    frame = parts.copy()
    category = frame.get("category", "").fillna("").astype(str).str.casefold()
    item = frame.get("item", "").fillna("").astype(str).str.casefold()
    frame = frame.loc[(category.eq("controller")) | (item.eq("controller"))].copy()
    frame["price"] = pd.to_numeric(frame["price"], errors="coerce")
    frame["multiplier"] = pd.to_numeric(frame["multiplier"], errors="coerce").fillna(1.0)
    frame = frame.dropna(subset=["price"])
    rows = []
    for _, row in frame.iterrows():
        description = normalize_optimizer(row.get("option", ""))
        part_number = str(row.get("part_number", "") or "").strip()
        supplier = str(row.get("supplier", "") or "").strip()
        manufacturer = normalize_manufacturer(f"{supplier} {description}")
        status = lifecycle_status(part_number, supplier, description)
        pn_upper = part_number.upper()
        if manufacturer == "Honeywell" and ("OPTIMIZER" in description.upper() or pn_upper.startswith(("VAA-", "UN-"))):
            family = "Optimizer"
        elif manufacturer == "Johnson Controls" and pn_upper.startswith("F4-"):
            family = "F4"
        elif manufacturer == "Johnson Controls" and pn_upper.startswith("FX-"):
            family = "FX"
        elif manufacturer == "Phoenix Controls":
            family = "Phoenix Controls"
        else:
            family = "Other"
        defaults = [name for name, pn in DEFAULT_CONTROLLERS.items() if pn_upper == pn.upper()]
        rows.append({
            "manufacturer": manufacturer,
            "family": family,
            "description": description,
            "part_number": part_number,
            "supplier": supplier,
            "unit_cost": float(row["price"]) * float(row["multiplier"]),
            "catalog_status": status,
            "selectable": status == "Active" and manufacturer in set(SUPPORTED_MANUFACTURERS),
            "default_for": ", ".join(defaults),
        })
    return (pd.DataFrame(rows, columns=columns)
            .drop_duplicates(subset=["part_number", "description", "supplier"])
            .sort_values(["manufacturer", "family", "description", "part_number"])
            .reset_index(drop=True))


def controller_choices(
    parts: pd.DataFrame,
    *,
    manufacturer: str | None = None,
    include_legacy: bool = False,
) -> pd.DataFrame:
    catalog = build_controller_catalog(parts)
    allowed = catalog["catalog_status"].eq("Active")
    if include_legacy:
        allowed |= catalog["catalog_status"].eq("Legacy")
    choices = catalog.loc[allowed & ~catalog["catalog_status"].eq("Removed")].copy()
    if manufacturer:
        choices = choices.loc[choices["manufacturer"].eq(manufacturer)].copy()
    choices["label"] = choices.apply(
        lambda r: f"{r['part_number']} — {r['description']} ({r['manufacturer']})", axis=1
    )
    choices["option"] = choices["description"]
    choices["item"] = "Controller"
    return choices.reset_index(drop=True)


def _equipment_key(equipment_name: str) -> str:
    name = str(equipment_name or "").casefold()
    if "vav" in name or "air valve" in name:
        return "VAV"
    if "fan coil" in name:
        return "Fan Coil"
    if "unit ventilator" in name:
        return "Unit Ventilator"
    if "heat pump" in name:
        return "Heat Pump"
    if "air handling" in name or "ahu" in name:
        return "AHU"
    if "boiler" in name:
        return "Boiler"
    if "chiller" in name:
        return "Chiller"
    if "pump" in name:
        return "Pump"
    return "Other"

def default_part_for_equipment(equipment_name: str, manufacturer: str = "Honeywell") -> str:
    key = _equipment_key(equipment_name)
    if manufacturer == "Johnson Controls":
        return JOHNSON_CONTROLS_DEFAULT_CONTROLLERS[key]
    if manufacturer == "Honeywell":
        return HONEYWELL_DEFAULT_CONTROLLERS[key]
    return ""
