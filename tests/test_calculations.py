from estimator import MaterialLine, LaborLine, EstimateSettings, calculate_estimate

def test_estimate_math():
    result = calculate_estimate(
        [MaterialLine("Controller", quantity=2, unit_cost=100, multiplier=1.1)],
        [LaborLine("Installation", hours=10, hourly_rate=50)],
        EstimateSettings(tax_rate=.08, material_markup=.10, contingency=.05, overhead=.10, profit=.10, crew_size=2, hours_per_day=8),
    )
    assert result.material_base == 220.00
    assert result.total_labor_hours == 10
    assert result.duration_days == .62
    assert result.grand_total > 0
