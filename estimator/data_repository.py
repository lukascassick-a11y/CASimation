from __future__ import annotations

from pathlib import Path

import pandas as pd


class DataRepository:
    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)
        self._parts_cache: pd.DataFrame | None = None
        self._taxes_cache: pd.DataFrame | None = None

    def clear_cache(self) -> None:
        self._parts_cache = None
        self._taxes_cache = None

    def load_parts(self, *, refresh: bool = False) -> pd.DataFrame:
        if self._parts_cache is not None and not refresh:
            return self._parts_cache.copy()
        path = self.data_dir / "parts.csv"
        columns = ["item", "option", "supplier", "part_number", "price", "multiplier", "category"]
        if not path.exists():
            self._parts_cache = pd.DataFrame(columns=columns)
            return self._parts_cache.copy()
        frame = pd.read_csv(path).fillna("")
        for column in columns:
            if column not in frame.columns:
                frame[column] = ""
        for column in ("price", "multiplier"):
            frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0 if column == "price" else 1)
        self._parts_cache = frame
        return frame.copy()

    def load_taxes(self, *, refresh: bool = False) -> pd.DataFrame:
        if self._taxes_cache is not None and not refresh:
            return self._taxes_cache.copy()
        path = self.data_dir / "taxes.csv"
        if not path.exists():
            self._taxes_cache = pd.DataFrame(columns=["county", "tax_rate"])
            return self._taxes_cache.copy()
        frame = pd.read_csv(path).fillna("")
        if "county" not in frame.columns:
            frame["county"] = ""
        if "tax_rate" not in frame.columns:
            frame["tax_rate"] = 0.0
        frame["tax_rate"] = pd.to_numeric(frame["tax_rate"], errors="coerce").fillna(0)
        self._taxes_cache = frame
        return frame.copy()

    def tax_rate_for(self, county: str) -> float:
        taxes = self.load_taxes()
        if taxes.empty or not county:
            return 0.0
        match = taxes[taxes["county"].astype(str).str.casefold() == county.casefold()]
        return float(match.iloc[0]["tax_rate"]) if not match.empty else 0.0
