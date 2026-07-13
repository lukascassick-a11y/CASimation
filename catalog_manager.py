from __future__ import annotations

from dataclasses import dataclass
import re
import pandas as pd

from .company_standards import CompanyStandards, DEFAULT_COMPANY_STANDARDS


CHOICE_COLUMNS = ["label", "item", "option", "supplier", "part_number", "unit_cost", "category"]


@dataclass
class CatalogManager:
    parts: pd.DataFrame
    standards: CompanyStandards = DEFAULT_COMPANY_STANDARDS

    def __post_init__(self) -> None:
        self.parts = self._normalize(self.parts)

    def _normalize(self, parts: pd.DataFrame) -> pd.DataFrame:
        frame = parts.copy() if parts is not None else pd.DataFrame()
        for column in ["item", "option", "supplier", "part_number", "category"]:
            if column not in frame.columns:
                frame[column] = ""
            frame[column] = frame[column].fillna("").astype(str)
        for column in ["price", "multiplier"]:
            if column not in frame.columns:
                frame[column] = 0.0 if column == "price" else 1.0
        frame["price"] = pd.to_numeric(frame["price"], errors="coerce")
        frame["multiplier"] = pd.to_numeric(frame["multiplier"], errors="coerce").fillna(1.0)
        frame["option"] = frame["option"].str.replace("Optimzer", "Optimizer", case=False, regex=False)
        frame["manufacturer"] = frame.apply(
            lambda row: self.standards.normalized_manufacturer(
                f"{row.get('supplier', '')} {row.get('option', '')}"
            ),
            axis=1,
        )
        frame["unit_cost"] = frame["price"] * frame["multiplier"]
        frame["catalog_status"] = frame.apply(self._catalog_status, axis=1)
        return frame

    def _catalog_status(self, row: pd.Series) -> str:
        part = str(row.get("part_number", "")).upper()
        text = " ".join(str(row.get(name, "")) for name in ("supplier", "option", "part_number")).upper()
        if any(name.upper() in text for name in self.standards.excluded_manufacturers):
            return "Removed"
        if part.startswith("FX-"):
            return "Legacy"
        return "Active"

    @staticmethod
    def _label(row: pd.Series) -> str:
        option = str(row.get("option", ""))
        part = str(row.get("part_number", ""))
        supplier = str(row.get("supplier", ""))
        return " | ".join(value for value in (option, part, supplier) if value)

    def choices(
        self,
        *,
        item: str | None = None,
        category: str | None = None,
        keywords: tuple[str, ...] = (),
        manufacturer: str | None = None,
        include_legacy: bool = False,
    ) -> pd.DataFrame:
        frame = self.parts.copy()
        if item:
            frame = frame.loc[frame["item"].str.casefold().eq(item.casefold())]
        if category:
            frame = frame.loc[frame["category"].str.casefold().eq(category.casefold())]
        if manufacturer:
            canonical = self.standards.normalized_manufacturer(manufacturer)
            frame = frame.loc[frame["manufacturer"].eq(canonical)]
        allowed = frame["catalog_status"].eq("Active")
        if include_legacy:
            allowed |= frame["catalog_status"].eq("Legacy")
        frame = frame.loc[allowed & frame["price"].notna()].copy()
        if keywords:
            text = frame[["option", "part_number"]].agg(" ".join, axis=1)
            mask = pd.Series(False, index=frame.index)
            for keyword in keywords:
                mask |= text.str.contains(re.escape(keyword), case=False, regex=True)
            frame = frame.loc[mask]
        frame["label"] = frame.apply(self._label, axis=1)
        return (
            frame[CHOICE_COLUMNS]
            .drop_duplicates(subset=["part_number", "option", "supplier"])
            .sort_values(["supplier", "option", "part_number"])
            .reset_index(drop=True)
        )

    def controllers(self, manufacturer: str | None = None, *, include_legacy: bool = False) -> pd.DataFrame:
        return self.choices(
            category="Controller",
            manufacturer=manufacturer,
            include_legacy=include_legacy,
        )

    def sensors(self, *, keywords: tuple[str, ...] = ()) -> pd.DataFrame:
        return self.choices(item="Temp Sensor", keywords=keywords)

    def current_switches(self) -> pd.DataFrame:
        return self.choices(category="Current Sw")

    def relays(self) -> pd.DataFrame:
        return self.choices(category="Relay")
