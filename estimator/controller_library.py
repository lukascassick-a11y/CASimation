from __future__ import annotations

from dataclasses import dataclass
import re
import pandas as pd

from .sylk_device_library import is_tr_sylk_sensor


@dataclass(frozen=True)
class ControllerProduct:
    family: str
    product_type: str
    description: str
    supplier: str
    part_number: str
    unit_cost: float
    ui: int = 0
    di: int = 0
    ao: int = 0
    do: int = 0
    uio: int = 0
    sylk_capable: bool = False

    @property
    def label(self) -> str:
        return f"{self.description} | {self.part_number} | {self.supplier}"


def _text(row: pd.Series) -> str:
    return " ".join(str(row.get(col, "") or "") for col in ("option", "part_number", "supplier", "item", "category"))


def _parse_io(description: str) -> dict[str, int]:
    text = description.upper().replace("'S", "")
    values = {"ui": 0, "di": 0, "ao": 0, "do": 0, "uio": 0}
    aliases = (("uio", "UIO"), ("ui", "UI"), ("di", "DI"), ("ao", "AO"), ("do", "DO"), ("do", "SSR"), ("do", "RELAY"))
    for field, token in aliases:
        for match in re.finditer(rf"(\d+)\s*[- ]?{token}\b", text):
            values[field] += int(match.group(1))
    return values


def build_optimizer_library(parts: pd.DataFrame) -> pd.DataFrame:
    """Build the approved Optimizer controller and I/O-module library.

    Catalog rows may contain the legacy misspelling ``Optimzer``. Both forms are
    accepted. Siemens products are always excluded.
    """
    columns = [
        "label", "family", "product_type", "description", "supplier", "part_number",
        "unit_cost", "ui", "di", "ao", "do", "uio", "sylk_capable",
    ]
    if parts.empty:
        return pd.DataFrame(columns=columns)

    frame = parts.copy()
    text = frame.fillna("").astype(str).agg(" ".join, axis=1)
    optimizer = text.str.contains(r"Optimi[sz]er|Optimzer", case=False, regex=True)
    allowed_type = frame.get("category", "").fillna("").astype(str).str.casefold().isin({"controller", "i/o module"})
    not_siemens = ~text.str.contains("Siemens", case=False, regex=False)
    frame = frame.loc[optimizer & allowed_type & not_siemens].copy()
    frame["price"] = pd.to_numeric(frame["price"], errors="coerce")
    frame["multiplier"] = pd.to_numeric(frame["multiplier"], errors="coerce").fillna(1.0)
    frame = frame.dropna(subset=["price"])

    rows = []
    for _, row in frame.iterrows():
        description = str(row.get("option", "") or "").replace("Optimzer", "Optimizer").replace("optimzer", "Optimizer")
        combined = _text(row)
        if re.search(r"Plant Cntr|N-ADV|IO-\d|IOD-", combined, re.IGNORECASE):
            family = "Optimizer Plant"
        else:
            family = "Optimizer Unitary"
        product_type = "I/O Module" if str(row.get("category", "")).casefold() == "i/o module" else "Controller"
        io = _parse_io(description)
        supplier = str(row.get("supplier", "") or "")
        part_number = str(row.get("part_number", "") or "")
        unit_cost = float(row["price"]) * float(row["multiplier"])
        rows.append({
            "label": f"{description} | {part_number} | {supplier}",
            "family": family,
            "product_type": product_type,
            "description": description,
            "supplier": supplier,
            "part_number": part_number,
            "unit_cost": unit_cost,
            **io,
            "sylk_capable": "SYLK" in description.upper(),
        })
    return (
        pd.DataFrame(rows, columns=columns)
        .drop_duplicates(subset=["part_number", "description", "product_type"])
        .sort_values(["family", "product_type", "description", "part_number"])
        .reset_index(drop=True)
    )


def optimizer_controller_choices(parts: pd.DataFrame, family: str | None = None) -> pd.DataFrame:
    library = build_optimizer_library(parts)
    choices = library.loc[library["product_type"].eq("Controller")].copy()
    if family:
        choices = choices.loc[choices["family"].eq(family)].copy()
    return choices.reset_index(drop=True)


def default_optimizer_controller(choices: pd.DataFrame, family: str = "Optimizer Unitary") -> int:
    """Return the row index of the preferred default controller.

    For unitary equipment, prefer the Optimizer VAV controller when available;
    otherwise select the first active controller in the requested family.
    """
    if choices.empty:
        return 0
    candidates = choices.loc[choices["family"].eq(family)] if "family" in choices else choices
    if candidates.empty:
        candidates = choices
    if family == "Optimizer Unitary":
        preferred = candidates["description"].str.contains("VAV Cntr", case=False, na=False)
        if preferred.any():
            return int(candidates.index[preferred][0])
    return int(candidates.index[0])
