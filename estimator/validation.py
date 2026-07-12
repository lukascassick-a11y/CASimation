from __future__ import annotations
from .models import ProjectInfo, MaterialLine, LaborLine, EstimateSettings

class ValidationError(ValueError):
    pass

def validate_project(project: ProjectInfo) -> None:
    if not project.project_name.strip():
        raise ValidationError("Project name is required.")

def validate_materials(lines: list[MaterialLine]) -> None:
    for index, line in enumerate(lines, start=1):
        if line.quantity < 0:
            raise ValidationError(f"Material row {index}: quantity cannot be negative.")
        if line.unit_cost < 0:
            raise ValidationError(f"Material row {index}: unit cost cannot be negative.")
        if line.multiplier < 0:
            raise ValidationError(f"Material row {index}: multiplier cannot be negative.")

def validate_labor(lines: list[LaborLine]) -> None:
    for index, line in enumerate(lines, start=1):
        if line.hours < 0 or line.hourly_rate < 0 or line.burden_multiplier < 0:
            raise ValidationError(f"Labor row {index}: hours, rate, and burden must be nonnegative.")

def validate_settings(settings: EstimateSettings) -> None:
    percentage_fields = {
        "tax_rate": settings.tax_rate,
        "material_markup": settings.material_markup,
        "labor_markup": settings.labor_markup,
        "contingency": settings.contingency,
        "overhead": settings.overhead,
        "profit": settings.profit,
    }
    for name, value in percentage_fields.items():
        if not 0 <= value <= 1:
            raise ValidationError(f"{name} must be between 0 and 1.")
    if settings.crew_size <= 0 or settings.hours_per_day <= 0:
        raise ValidationError("Crew size and hours per day must be greater than zero.")
