from __future__ import annotations
import math
from .models import MaterialLine, LaborLine, EstimateSettings, EstimateResult
from .validation import validate_materials, validate_labor, validate_settings

def calculate_estimate(
    materials: list[MaterialLine],
    labor: list[LaborLine],
    settings: EstimateSettings,
) -> EstimateResult:
    validate_materials(materials)
    validate_labor(labor)
    validate_settings(settings)

    material_base = sum(line.extended_cost for line in materials)
    material_markup = material_base * settings.material_markup
    taxable_material = material_base + material_markup
    tax = taxable_material * settings.tax_rate

    labor_base = sum(line.extended_cost for line in labor)
    labor_markup = labor_base * settings.labor_markup
    direct_total = taxable_material + tax + labor_base + labor_markup

    contingency = direct_total * settings.contingency
    subtotal_with_contingency = direct_total + contingency
    overhead = subtotal_with_contingency * settings.overhead
    subtotal_with_overhead = subtotal_with_contingency + overhead
    profit = subtotal_with_overhead * settings.profit
    grand_total = subtotal_with_overhead + profit

    total_labor_hours = sum(line.hours for line in labor)
    duration_days = total_labor_hours / (settings.crew_size * settings.hours_per_day)

    return EstimateResult(
        material_base=round(material_base, 2),
        material_markup=round(material_markup, 2),
        taxable_material=round(taxable_material, 2),
        tax=round(tax, 2),
        labor_base=round(labor_base, 2),
        labor_markup=round(labor_markup, 2),
        contingency=round(contingency, 2),
        overhead=round(overhead, 2),
        profit=round(profit, 2),
        grand_total=round(grand_total, 2),
        total_labor_hours=round(total_labor_hours, 2),
        duration_days=round(duration_days, 2),
    )
