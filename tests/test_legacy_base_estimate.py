import pytest
from estimator.legacy_base_estimate import LegacySystemInput, calculate_legacy_system
from estimator.legacy_templates import BASE_ESTIMATE_SYSTEMS


def test_vav_heat_matches_base_estimate_formulas():
    result = calculate_legacy_system(
        LegacySystemInput(BASE_ESTIMATE_SYSTEMS["VAV Boxes w Heat"], quantity=10)
    )
    assert result.total_points == 10
    assert result.electrical_allowance == 5500
    assert result.technician_hours == 10
    assert result.graphics_hours == 2.5
    assert result.programming_hours == 2.5
    assert result.controller_count == 10
    assert result.controller_points == 700
    assert round(sum(x.extended_cost for x in result.materials), 2) == 4332.57


def test_crc_supply_box_formula_family():
    result = calculate_legacy_system(
        LegacySystemInput(
            BASE_ESTIMATE_SYSTEMS["Supply Air Boxes - CRC/Phoenix LV Wiring and Integration"],
            quantity=4,
        )
    )
    assert result.total_points == 4
    assert result.electrical_allowance == 3000
    assert result.technician_hours == 4
    assert result.graphics_hours == 1
    assert result.programming_hours == 1

from estimator.legacy_large_templates import LARGE_EQUIPMENT_SYSTEMS


def test_vav_ahu_configurable_point_rows_match_header_formula():
    rule = LARGE_EQUIPMENT_SYSTEMS["VAV Air Handling Unit"]
    result = calculate_legacy_system(LegacySystemInput(
        rule,
        quantity=2,
        per_unit_overrides={47: 1, 52: 1, 57: 1, 58: 2},
    ))
    # Base Estimate N46 = SUM(I57:I73) + I52. Controller row 47 is material,
    # but it is not included in the point total.
    assert result.total_points == 8
    assert result.electrical_allowance == 2800
    assert result.technician_hours == 8
    assert result.graphics_hours == 8
    assert result.programming_hours == 12
    assert result.controller_count == 2
    assert result.controller_points == 140


def test_negative_component_quantity_is_rejected():
    rule = LARGE_EQUIPMENT_SYSTEMS["Chiller"]
    try:
        calculate_legacy_system(LegacySystemInput(rule, 1, {225: -1}))
    except ValueError as exc:
        assert "cannot be negative" in str(exc)
    else:
        raise AssertionError("Expected negative quantity validation")


def test_catalog_option_replacement_updates_exported_material():
    import pandas as pd
    from estimator.legacy_options import catalog_choices, replace_material_from_catalog, replace_rule_materials

    parts = pd.DataFrame([
        {"item": "Controller", "option": "VAV Choice A", "supplier": "Supplier A", "part_number": "A1", "price": 100.0, "multiplier": 1.1},
        {"item": "Controller", "option": "Nonmatching", "supplier": "Supplier B", "part_number": "B1", "price": 50.0, "multiplier": 1.0},
    ])
    choices = catalog_choices(parts, "Controller", keywords=("VAV",))
    assert choices["label"].tolist() == ["VAV Choice A | A1"]
    base = BASE_ESTIMATE_SYSTEMS["Cooling Only VAV Boxes"]
    replacement = replace_material_from_catalog(base.materials[0], choices.iloc[0])
    configured = replace_rule_materials(base, {0: replacement})
    result = calculate_legacy_system(LegacySystemInput(configured, 2))
    controller = result.materials[0]
    assert controller.option == "VAV Choice A"
    assert controller.part_number == "A1"
    assert controller.supplier == "Supplier A"
    assert controller.unit_cost == pytest.approx(110.0)
    assert controller.quantity == pytest.approx(2.0)


def test_vav_electrical_rate_override():
    rule = BASE_ESTIMATE_SYSTEMS["VAV Boxes w Heat"]
    result = calculate_legacy_system(LegacySystemInput(rule, 2, electrical_rate_override=625.0))
    assert result.total_points == 2
    assert result.electrical_allowance == 1250


def test_negative_electrical_rate_override_rejected():
    import pytest
    rule = BASE_ESTIMATE_SYSTEMS["VAV Boxes w Heat"]
    with pytest.raises(ValueError, match="Electrical cost per point"):
        calculate_legacy_system(LegacySystemInput(rule, 1, electrical_rate_override=-1.0))


def test_controller_choices_follow_materials_controller_category():
    import pandas as pd
    from estimator.legacy_options import catalog_choices_by_category

    parts = pd.DataFrame([
        {"item": "Controller", "option": "VAV Controller", "supplier": "A", "part_number": "C1", "price": 100.0, "multiplier": 1.1, "category": "Controller"},
        {"item": "Controller", "option": "Duplicate outside category", "supplier": "B", "part_number": "C2", "price": 50.0, "multiplier": 1.0, "category": "Miscellanous"},
        {"item": "Temp Sensor", "option": "Misfiled but in controller category", "supplier": "C", "part_number": "C3", "price": 25.0, "multiplier": 1.0, "category": "Controller"},
    ])
    choices = catalog_choices_by_category(parts, "Controller")
    assert set(choices["part_number"]) == {"C1", "C3"}
    assert choices.loc[choices["part_number"].eq("C1"), "unit_cost"].iloc[0] == pytest.approx(110.0)


def test_vav_electrical_cost_is_per_vav():
    rule = BASE_ESTIMATE_SYSTEMS["VAV Boxes w Heat"]
    result = calculate_legacy_system(
        LegacySystemInput(rule, 3, electrical_cost_per_unit_override=625.0)
    )
    assert result.electrical_allowance == pytest.approx(1875.0)


def test_negative_vav_electrical_cost_rejected():
    rule = BASE_ESTIMATE_SYSTEMS["VAV Boxes w Heat"]
    with pytest.raises(ValueError, match="Electrical cost per VAV"):
        calculate_legacy_system(
            LegacySystemInput(rule, 1, electrical_cost_per_unit_override=-1.0)
        )


def test_optimizer_library_excludes_siemens_and_includes_both_families():
    import pandas as pd
    from estimator.controller_library import build_optimizer_library

    parts = pd.DataFrame([
        {"category": "Controller", "item": "Controller", "option": "Optimizer VAV Cntr, 7 UIO, 5 SSR, Sylk", "supplier": "Honeywell", "part_number": "VAA-1", "price": 100, "multiplier": 1.1},
        {"category": "Controller", "item": "Controller", "option": "Optimizer Plant Cntr", "supplier": "Honeywell", "part_number": "N-ADV-1", "price": 200, "multiplier": 1.0},
        {"category": "Controller", "item": "Controller", "option": "Optimizer Siemens Controller", "supplier": "Siemens", "part_number": "S1", "price": 50, "multiplier": 1.0},
        {"category": "I/O Module", "item": "I/O Module", "option": "Optimzer Plant Cntr 16 Universal Input Module", "supplier": "Honeywell", "part_number": "IO-16UI-S-S", "price": 75, "multiplier": 1.0},
    ])
    library = build_optimizer_library(parts)
    assert "S1" not in set(library["part_number"])
    assert set(library["family"]) == {"Optimizer Unitary", "Optimizer Plant"}
    vav = library.loc[library["part_number"].eq("VAA-1")].iloc[0]
    assert vav["uio"] == 7
    assert vav["do"] == 5
    assert bool(vav["sylk_capable"])


def test_tr_sensors_are_sylk_devices_not_ai_ui_points():
    from estimator.controller_library import is_tr_sylk_sensor

    assert is_tr_sylk_sensor(option="TR100 Space with Temp/Humd/CO2 LCD", part_number="TR100-THC-G")
    assert is_tr_sylk_sensor(option="TR42 Space Sensor Only/LCD", part_number="TR42")
    assert not is_tr_sylk_sensor(option="Duct Insertion Sensor", part_number="C7041B2005")


def test_sylk_device_library_has_zero_ai_ui_and_one_device_count():
    import pandas as pd
    from estimator.sylk_device_library import build_sylk_device_library

    parts = pd.DataFrame([
        {"item": "Temp Sensor", "option": "TR42 Space Sensor Only/LCD", "supplier": "Honeywell", "part_number": "TR42", "price": 80.0, "multiplier": 1.1, "category": "Temp Sensor"},
        {"item": "Temp Sensor", "option": "Duct Sensor", "supplier": "Honeywell", "part_number": "C7041", "price": 30.0, "multiplier": 1.0, "category": "Temp Sensor"},
    ])
    library = build_sylk_device_library(parts)
    assert library["part_number"].tolist() == ["TR42"]
    row = library.iloc[0]
    assert row["ai_ui_points"] == 0
    assert row["sylk_device_count"] == 1
    assert not bool(row["consumes_ai_ui"])
    assert row["unit_cost"] == pytest.approx(88.0)


def test_selected_tr_sensor_is_excluded_from_material_point_total():
    from dataclasses import replace
    from estimator.legacy_base_estimate import LegacyMaterialRule, LegacySystemRule

    rule = LegacySystemRule(
        name="Sylk point test",
        points_from_materials=True,
        materials=(
            LegacyMaterialRule("Temp Sensor", "TR100 Space with LCD", 1, "TR100-T-G", 100, "Honeywell", contributes_to_points=True),
            LegacyMaterialRule("Damper End Switch", "Physical input", 1, "DI-1", 10, "Other", contributes_to_points=True),
        ),
    )
    result = calculate_legacy_system(LegacySystemInput(rule, quantity=3))
    assert result.total_points == 3
    assert result.sylk_devices == 3


def test_optimizer_spelling_is_normalized_in_controller_library():
    import pandas as pd
    from estimator.controller_library import build_optimizer_library

    parts = pd.DataFrame([
        {"category": "Controller", "item": "Controller", "option": "Optimzer Unitary Cntr, 8 UI", "supplier": "Honeywell", "part_number": "UN-1", "price": 100, "multiplier": 1},
    ])
    library = build_optimizer_library(parts)
    assert "Optimzer" not in library.iloc[0]["description"]
    assert "Optimizer" in library.iloc[0]["description"]
