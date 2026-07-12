"""One-time converter from the original workbook to independent CSV reference tables."""
from pathlib import Path
import sys
import pandas as pd

SOURCE = Path(sys.argv[1] if len(sys.argv) > 1 else "Estimate Tool VER-8.6.xlsx")
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "data")
OUT.mkdir(parents=True, exist_ok=True)

parts_raw = pd.read_excel(SOURCE, sheet_name="Parts List", header=None)
header_row = next(i for i, row in parts_raw.iterrows() if "Item" in row.astype(str).tolist())
parts = pd.read_excel(SOURCE, sheet_name="Parts List", header=header_row)
parts = parts.rename(columns={"Item":"item", "Option ":"option", "Supplier":"supplier", "Part #":"part_number", "Price":"price", "Multiplier":"multiplier"})
parts = parts[[c for c in ["item","option","supplier","part_number","price","multiplier"] if c in parts.columns]].copy()
parts["category"] = parts.get("item", "").astype(str).str.extract(r"^([A-Za-z /&-]+)", expand=False).fillna("Material").str.strip()
parts = parts[parts["item"].notna() & (parts["item"].astype(str).str.strip() != "")]
parts.to_csv(OUT / "parts.csv", index=False)

taxes_raw = pd.read_excel(SOURCE, sheet_name="State Taxes", header=None)
taxes = taxes_raw.iloc[:,1:3].copy(); taxes.columns=["county","tax_rate"]
taxes["tax_rate"] = pd.to_numeric(taxes["tax_rate"], errors="coerce")
taxes = taxes[taxes["county"].notna() & taxes["tax_rate"].notna()]
taxes.to_csv(OUT / "taxes.csv", index=False)
print(f"Extracted {len(parts):,} parts and {len(taxes):,} tax rows to {OUT.resolve()}")
