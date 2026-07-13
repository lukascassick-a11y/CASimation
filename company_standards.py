from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

SUPPORTED_MANUFACTURERS = ("Honeywell", "Johnson Controls", "Phoenix Controls")


@dataclass(frozen=True)
class CompanyStandards:
    """Company-wide estimating defaults kept outside UI and formulas."""

    default_controller_manufacturer: str = "Honeywell"
    allow_legacy_controllers: bool = False
    excluded_manufacturers: tuple[str, ...] = ("Siemens",)
    manufacturer_aliases: Mapping[str, str] = field(
        default_factory=lambda: {
            "Honeywell": "Honeywell",
            "JCI": "Johnson Controls",
            "Johnson Control": "Johnson Controls",
            "Johnson Controls": "Johnson Controls",
            "Phoenix": "Phoenix Controls",
            "Phoenix Controls": "Phoenix Controls",
        }
    )
    controller_defaults: Mapping[str, Mapping[str, str]] = field(
        default_factory=lambda: {
            "Honeywell": {
                "VAV": "VAA-VA75MB24NMC",
                "Fan Coil": "UN-RS0844MS24NMC",
                "Unit Ventilator": "UN-RS0844MS24NMC",
                "Heat Pump": "UN-RS0844MS24NMC",
                "AHU": "UN-RL1644MS24NMC",
                "Boiler": "UN-RL1644MS24NMC",
                "Chiller": "UN-RL1644MS24NMC",
                "Pump": "UN-RL1644MS24NMC",
                "Other": "UN-RL1644MS24NMC",
            },
            "Johnson Controls": {
                "VAV": "F4-CVM3050-0",
                "Fan Coil": "F4-CGM09090-0",
                "Unit Ventilator": "F4-CGM09090-0",
                "Heat Pump": "F4-CGM09090-0",
                "AHU": "F4-CGM09090-0",
                "Boiler": "F4-CGM09090-0",
                "Chiller": "F4-CGM09090-0",
                "Pump": "F4-CGM09090-0",
                "Other": "F4-CGM09090-0",
            },
            "Phoenix Controls": {},
        }
    )
    default_electrical_cost_per_vav: float = 550.0

    def normalized_manufacturer(self, value: str) -> str:
        text = str(value or "").strip()
        folded = text.casefold()
        for alias, canonical in self.manufacturer_aliases.items():
            if alias.casefold() == folded:
                return canonical
        if "honeywell" in folded:
            return "Honeywell"
        if "johnson" in folded or folded == "jci":
            return "Johnson Controls"
        if "phoenix" in folded:
            return "Phoenix Controls"
        return text

    def default_controller(self, equipment_key: str, manufacturer: str | None = None) -> str:
        manufacturer = self.normalized_manufacturer(
            manufacturer or self.default_controller_manufacturer
        )
        defaults = self.controller_defaults.get(manufacturer, {})
        return defaults.get(equipment_key, defaults.get("Other", ""))


DEFAULT_COMPANY_STANDARDS = CompanyStandards()
