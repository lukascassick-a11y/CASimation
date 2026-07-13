from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class EquipmentOptionTemplate:
    role: str
    item: str
    label: str
    category: str | None = None
    keywords: tuple[str, ...] = ()
    optional: bool = True
    default_quantity_per_unit: float = 0.0
    counts_as_physical_io: bool = False
    tracks_sylk: bool = False


@dataclass(frozen=True)
class EquipmentTemplate:
    key: str
    display_name: str
    aliases: tuple[str, ...]
    controller_equipment_key: str
    options: tuple[EquipmentOptionTemplate, ...] = ()
    metadata: Mapping[str, object] = field(default_factory=dict)


VAV_TEMPLATE = EquipmentTemplate(
    key="vav",
    display_name="VAV Box",
    aliases=("vav", "air valve", "vav boxes w heat", "cooling only vav boxes"),
    controller_equipment_key="VAV",
    options=(
        EquipmentOptionTemplate(
            role="space_sensor",
            item="Temp Sensor",
            label="Space sensor type",
            keywords=("Space", "TR21", "TR23", "TR40", "TR42", "TR50", "TR71", "TR75", "TR100", "TR120"),
            optional=True,
            default_quantity_per_unit=1.0,
            tracks_sylk=True,
        ),
        EquipmentOptionTemplate(
            role="duct_sensor",
            item="Temp Sensor",
            label="Duct sensor type",
            keywords=("Duct", "Insertion", "Averaging"),
            optional=True,
            default_quantity_per_unit=1.0,
            counts_as_physical_io=True,
        ),
        EquipmentOptionTemplate(
            role="current_switch",
            item="Current Sw",
            label="Current switch type",
            category="Current Sw",
            optional=True,
            default_quantity_per_unit=0.0,
            counts_as_physical_io=True,
        ),
        EquipmentOptionTemplate(
            role="relay",
            item="Relay",
            label="Relay type",
            category="Relay",
            optional=True,
            default_quantity_per_unit=0.0,
            counts_as_physical_io=True,
        ),
    ),
    metadata={"electrical_basis": "per_unit"},
)

EQUIPMENT_TEMPLATES: tuple[EquipmentTemplate, ...] = (
    VAV_TEMPLATE,
    EquipmentTemplate("fan_coil", "Fan Coil", ("fan coil",), "Fan Coil"),
    EquipmentTemplate("unit_ventilator", "Unit Ventilator", ("unit ventilator",), "Unit Ventilator"),
    EquipmentTemplate("heat_pump", "Heat Pump", ("heat pump",), "Heat Pump"),
    EquipmentTemplate("ahu", "Air Handling Unit", ("air handling", "ahu"), "AHU"),
    EquipmentTemplate("boiler", "Boiler", ("boiler",), "Boiler"),
    EquipmentTemplate("chiller", "Chiller", ("chiller",), "Chiller"),
    EquipmentTemplate("pump", "Pump System", ("pump",), "Pump"),
)


def equipment_template_for(name: str) -> EquipmentTemplate:
    folded = str(name or "").casefold()
    for template in EQUIPMENT_TEMPLATES:
        if any(alias in folded for alias in template.aliases):
            return template
    return EquipmentTemplate("other", str(name or "Other"), (), "Other")


def option_template_for_item(equipment: EquipmentTemplate, item: str, option: str = "") -> EquipmentOptionTemplate | None:
    item_folded = str(item or "").casefold()
    option_folded = str(option or "").casefold()
    candidates = [entry for entry in equipment.options if entry.item.casefold() == item_folded]
    if not candidates:
        return None
    if item_folded == "temp sensor":
        if "duct" in option_folded:
            return next((entry for entry in candidates if entry.role == "duct_sensor"), candidates[0])
        return next((entry for entry in candidates if entry.role == "space_sensor"), candidates[0])
    return candidates[0]
