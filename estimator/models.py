from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

@dataclass
class ProjectInfo:
    project_name: str
    customer: str = ""
    estimator: str = ""
    estimate_date: date = field(default_factory=date.today)
    county: str = ""
    state: str = ""
    project_type: str = "Retrofit"
    notes: str = ""

@dataclass
class MaterialLine:
    item: str
    option: str = ""
    supplier: str = ""
    part_number: str = ""
    quantity: float = 0.0
    unit_cost: float = 0.0
    multiplier: float = 1.0
    category: str = "Material"

    @property
    def adjusted_unit_cost(self) -> float:
        return self.unit_cost * self.multiplier

    @property
    def extended_cost(self) -> float:
        return self.quantity * self.adjusted_unit_cost

@dataclass
class LaborLine:
    category: str
    hours: float
    hourly_rate: float
    burden_multiplier: float = 1.0

    @property
    def extended_cost(self) -> float:
        return self.hours * self.hourly_rate * self.burden_multiplier

@dataclass
class EstimateSettings:
    tax_rate: float = 0.0
    material_markup: float = 0.0
    labor_markup: float = 0.0
    contingency: float = 0.0
    overhead: float = 0.0
    profit: float = 0.0
    crew_size: float = 1.0
    hours_per_day: float = 8.0

@dataclass
class EstimateResult:
    material_base: float
    material_markup: float
    taxable_material: float
    tax: float
    labor_base: float
    labor_markup: float
    contingency: float
    overhead: float
    profit: float
    grand_total: float
    total_labor_hours: float
    duration_days: float
