from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .models import MaterialLine, LaborLine
from .sylk_device_library import is_tr_sylk_sensor, sylk_device_count


@dataclass(frozen=True)
class LegacyMaterialRule:
    item: str
    option: str = ""
    per_unit: float = 0.0
    part_number: str = ""
    unit_cost: float = 0.0
    supplier: str = ""
    category: str = "Material"
    source_row: int = 0
    contributes_to_points: bool = False
    controller_points_each: float = 0.0


@dataclass(frozen=True)
class LegacySystemRule:
    name: str
    points_per_unit: float = 0.0
    electrical_rate_per_point: float = 0.0
    technician_hours_per_point: float = 0.0
    graphics_hours_per_unit: float = 0.0
    programming_hours_per_unit: float = 0.0
    controller_points_each: float = 0.0
    materials: tuple[LegacyMaterialRule, ...] = field(default_factory=tuple)
    points_from_materials: bool = False


@dataclass(frozen=True)
class LegacySystemInput:
    rule: LegacySystemRule
    quantity: float
    per_unit_overrides: dict[int, float] = field(default_factory=dict)
    electrical_rate_override: float | None = None
    electrical_cost_per_unit_override: float | None = None


@dataclass(frozen=True)
class LegacySystemResult:
    name: str
    quantity: float
    total_points: float
    electrical_allowance: float
    technician_hours: float
    graphics_hours: float
    programming_hours: float
    controller_count: float
    controller_points: float
    sylk_devices: float
    materials: tuple[MaterialLine, ...]


def calculate_legacy_system(system: LegacySystemInput) -> LegacySystemResult:
    """Replicate the common Base Estimate section formulas.

    Excel equivalents:
    - line quantity = system quantity * per-unit quantity
    - material extension = line quantity * catalog price
    - total points = system quantity * points per unit
    - electrical allowance = total points * electrical rate
    - technician hours = total points * technician hours per point
    - graphics/programming hours = system quantity * hours per unit
    """
    qty = float(system.quantity)
    if qty < 0:
        raise ValueError("System quantity cannot be negative")

    rule = system.rule
    material_lines: list[MaterialLine] = []
    controller_count = 0.0
    controller_points = 0.0
    selected_points_per_unit = 0.0
    total_sylk_devices = 0.0
    for material in rule.materials:
        per_unit = float(system.per_unit_overrides.get(material.source_row, material.per_unit))
        if per_unit < 0:
            raise ValueError(f"Per-unit quantity cannot be negative for row {material.source_row}")
        line_qty = qty * per_unit
        line = MaterialLine(
            item=material.item,
            option=material.option,
            supplier=material.supplier,
            part_number=material.part_number,
            quantity=line_qty,
            unit_cost=float(material.unit_cost),
            multiplier=1.0,
            category=material.category,
        )
        material_lines.append(line)
        is_sylk = is_tr_sylk_sensor(option=material.option, part_number=material.part_number)
        total_sylk_devices += sylk_device_count(option=material.option, part_number=material.part_number, quantity=line_qty)
        if material.contributes_to_points and not is_sylk:
            selected_points_per_unit += per_unit
        if material.item.strip().casefold() == "controller":
            controller_count += line_qty
        if material.controller_points_each:
            controller_points += line_qty * float(material.controller_points_each)

    points_per_unit = selected_points_per_unit if rule.points_from_materials else float(rule.points_per_unit)
    total_points = qty * points_per_unit
    electrical_rate = (
        float(system.electrical_rate_override)
        if system.electrical_rate_override is not None
        else float(rule.electrical_rate_per_point)
    )
    if electrical_rate < 0:
        raise ValueError("Electrical cost per point cannot be negative")
    electrical_cost_per_unit = system.electrical_cost_per_unit_override
    if electrical_cost_per_unit is not None and float(electrical_cost_per_unit) < 0:
        raise ValueError("Electrical cost per VAV cannot be negative")
    electrical_allowance = (
        qty * float(electrical_cost_per_unit)
        if electrical_cost_per_unit is not None
        else total_points * electrical_rate
    )
    return LegacySystemResult(
        name=rule.name,
        quantity=qty,
        total_points=total_points,
        electrical_allowance=electrical_allowance,
        technician_hours=total_points * float(rule.technician_hours_per_point),
        graphics_hours=qty * float(rule.graphics_hours_per_unit),
        programming_hours=qty * float(rule.programming_hours_per_unit),
        controller_count=controller_count,
        controller_points=controller_points or (controller_count * float(rule.controller_points_each)),
        sylk_devices=total_sylk_devices,
        materials=tuple(material_lines),
    )


def combine_legacy_results(
    results: Iterable[LegacySystemResult],
    labor_rates: dict[str, float] | None = None,
) -> tuple[list[MaterialLine], list[LaborLine], float]:
    """Convert legacy section results into the estimator's existing models."""
    rates = {
        "Technician": 95.0,
        "Graphics": 110.0,
        "Programming": 125.0,
        **(labor_rates or {}),
    }
    results = list(results)
    materials = [line for result in results for line in result.materials if line.quantity]
    labor = [
        LaborLine("Technician", sum(r.technician_hours for r in results), rates["Technician"]),
        LaborLine("Graphics", sum(r.graphics_hours for r in results), rates["Graphics"]),
        LaborLine("Programming", sum(r.programming_hours for r in results), rates["Programming"]),
    ]
    electrical_allowance = sum(r.electrical_allowance for r in results)
    return materials, labor, electrical_allowance
