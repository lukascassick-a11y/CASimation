from __future__ import annotations
from pathlib import Path
import pandas as pd

class DataRepository:
    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)

    def load_parts(self) -> pd.DataFrame:
        path = self.data_dir / "parts.csv"
        columns = ["item", "option", "supplier", "part_number", "price", "multiplier", "category"]
        if not path.exists():
            return pd.DataFrame(columns=columns)
        df = pd.read_csv(path).fillna("")
        for col in ("price", "multiplier"):
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0 if col == "price" else 1)
        return df

    def load_taxes(self) -> pd.DataFrame:
        path = self.data_dir / "taxes.csv"
        if not path.exists():
            return pd.DataFrame(columns=["county", "tax_rate"])
        df = pd.read_csv(path).fillna("")
        df["tax_rate"] = pd.to_numeric(df["tax_rate"], errors="coerce").fillna(0)
        return df

    def tax_rate_for(self, county: str) -> float:
        taxes = self.load_taxes()
        if taxes.empty or not county:
            return 0.0
        match = taxes[taxes["county"].str.casefold() == county.casefold()]
        return float(match.iloc[0]["tax_rate"]) if not match.empty else 0.0
