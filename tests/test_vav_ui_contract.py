from pathlib import Path

from estimator.legacy_base_estimate import LegacySystemInput, calculate_legacy_system
from estimator.legacy_templates import BASE_ESTIMATE_SYSTEMS


ROOT = Path(__file__).resolve().parents[1]
VAV_UI = (ROOT / "ui" / "vav_page.py").read_text()
APP = (ROOT / "app.py").read_text()


def test_vav_ui_is_extracted_from_app_module():
    assert "from ui.vav_page import render_vav_air_box_sections" in APP
    assert "render_vav_air_box_sections(" in APP
    assert "Electrical cost per VAV" not in APP


def test_vav_electrical_ui_is_direct_editable_input():
    assert '"Electrical cost per VAV"' in VAV_UI
    assert 'key=f"vav_electrical_cost_{idx}"' in VAV_UI
    assert "electrical_cost_per_unit_override=electrical_cost_per_vav" in VAV_UI


def test_vav_sensor_and_accessory_controls_are_visible():
    assert '"Space sensor type"' in VAV_UI
    assert '"Duct sensor type"' in VAV_UI
    assert '"Current switch type"' in VAV_UI
    assert '"Relay type"' in VAV_UI
    assert 'material.item in {"Temp Sensor", "Current Sw", "Relay"}' in VAV_UI
    assert 'key=f"vav_include_{idx}_{material_index}"' in VAV_UI
    assert 'key=f"vav_qty_per_unit_{idx}_{material_index}"' in VAV_UI


def test_manufacturer_standards_are_connected_to_vav_ui():
    assert 'key=f"vav_controller_manufacturer_{idx}"' in VAV_UI
    assert "default_part_for_equipment(system_name, controller_manufacturer)" in VAV_UI


def test_per_vav_electrical_override_changes_calculation():
    rule = BASE_ESTIMATE_SYSTEMS["VAV Boxes w Heat"]
    result = calculate_legacy_system(
        LegacySystemInput(rule, 3, electrical_cost_per_unit_override=425.0)
    )
    assert result.electrical_allowance == 1275.0


def test_current_switch_and_relay_quantities_flow_to_materials():
    rule = BASE_ESTIMATE_SYSTEMS["VAV Boxes w Heat"]
    current_switch = next(m for m in rule.materials if m.item == "Current Sw")
    relay = next(m for m in rule.materials if m.item == "Relay")
    result = calculate_legacy_system(
        LegacySystemInput(
            rule,
            4,
            per_unit_overrides={current_switch.source_row: 1.0, relay.source_row: 2.0},
        )
    )
    current_line = next(m for m in result.materials if m.item == "Current Sw")
    relay_line = next(m for m in result.materials if m.item == "Relay")
    assert current_line.quantity == 4.0
    assert relay_line.quantity == 8.0
