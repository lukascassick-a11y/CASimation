from __future__ import annotations

from dataclasses import replace
from typing import Iterable

import pandas as pd

from .legacy_base_estimate import LegacyMaterialRule, LegacySystemRule


def catalog_choices(parts: pd.DataFrame, item: str, *, keywords: Iterable[str] = ()) -> pd.DataFrame:
    """Return clean, uniquely-labelled catalog choices for a legacy material row."""
    if parts.empty:
        return pd.DataFrame(columns=["label", "item", "option", "supplier", "part_number", "unit_cost"])

    frame = parts.copy()
    mask = frame["item"].astype(str).str.casefold().eq(item.casefold())
    frame = frame.loc[mask].copy()
    words = [str(word).strip() for word in keywords if str(word).strip()]
    if words:
        text = frame[["option", "part_number"]].fillna("").astype(str).agg(" ".join, axis=1)
        keyword_mask = pd.Series(False, index=frame.index)
        for word in words:
            keyword_mask |= text.str.contains(word, case=False, regex=False)
        frame = frame.loc[keyword_mask].copy()

    frame["price"] = pd.to_numeric(frame["price"], errors="coerce")
    frame["multiplier"] = pd.to_numeric(frame["multiplier"], errors="coerce").fillna(1.0)
    frame = frame.dropna(subset=["price"])
    frame["unit_cost"] = frame["price"] * frame["multiplier"]
    frame["option"] = frame["option"].fillna("").astype(str)
    frame["part_number"] = frame["part_number"].fillna("").astype(str)
    frame["supplier"] = frame["supplier"].fillna("").astype(str)
    frame["label"] = frame.apply(
        lambda row: f"{row['option']} | {row['part_number']}" if row["part_number"] else row["option"], axis=1
    )
    return (
        frame[["label", "item", "option", "supplier", "part_number", "unit_cost"]]
        .drop_duplicates(subset=["label"])
        .sort_values(["option", "part_number"])
        .reset_index(drop=True)
    )



def catalog_choices_by_category(parts: pd.DataFrame, category: str) -> pd.DataFrame:
    """Return priced catalog choices from a Materials category.

    This powers dropdowns that should follow the workbook's Materials category
    list rather than a keyword-filtered subset.
    """
    if parts.empty or "category" not in parts.columns:
        return pd.DataFrame(columns=["label", "item", "option", "supplier", "part_number", "unit_cost", "category"])

    frame = parts.copy()
    frame = frame.loc[
        frame["category"].fillna("").astype(str).str.strip().str.casefold().eq(category.strip().casefold())
    ].copy()
    frame["price"] = pd.to_numeric(frame["price"], errors="coerce")
    frame["multiplier"] = pd.to_numeric(frame["multiplier"], errors="coerce").fillna(1.0)
    frame = frame.dropna(subset=["price"])
    frame["unit_cost"] = frame["price"] * frame["multiplier"]
    for column in ["item", "option", "supplier", "part_number", "category"]:
        frame[column] = frame[column].fillna("").astype(str)
    frame["label"] = frame.apply(
        lambda row: f"{row['option']} | {row['part_number']} | {row['supplier']}", axis=1
    )
    return (
        frame[["label", "item", "option", "supplier", "part_number", "unit_cost", "category"]]
        .drop_duplicates(subset=["part_number", "option", "supplier"])
        .sort_values(["supplier", "option", "part_number"])
        .reset_index(drop=True)
    )

def replace_material_from_catalog(material: LegacyMaterialRule, choice: pd.Series | dict) -> LegacyMaterialRule:
    """Create a legacy material rule using the selected catalog option."""
    return replace(
        material,
        option=str(choice.get("option", "")),
        supplier=str(choice.get("supplier", "")),
        part_number=str(choice.get("part_number", "")),
        unit_cost=float(choice.get("unit_cost", 0.0) or 0.0),
    )


def replace_rule_materials(rule: LegacySystemRule, replacements: dict[int, LegacyMaterialRule]) -> LegacySystemRule:
    """Replace selected material rows while preserving all legacy formulas."""
    materials = tuple(replacements.get(index, material) for index, material in enumerate(rule.materials))
    return replace(rule, materials=materials)
