from pathlib import Path


def test_vav_electrical_ui_is_direct_editable_input():
    app = (Path(__file__).resolve().parents[1] / "app.py").read_text()
    assert '"Electrical cost per VAV"' in app
    assert 'key=f"vav_electrical_cost_{idx}"' in app
    assert 'electrical_cost_per_unit_override = electrical_col.number_input' in app
    assert 'float(qty) * electrical_cost_per_unit_override' in app
    assert 'electrical_cost_per_unit_override=electrical_cost_per_unit_override' in app


def test_vav_sensor_selectors_are_in_actual_configuration_ui():
    app = (Path(__file__).resolve().parents[1] / "app.py").read_text()
    assert 'st.markdown("#### Controller and sensor selections")' in app
    assert '"Duct sensor type" if "Duct" in material.option else "Space sensor type"' in app
    assert 'key=f"vav_option_{idx}_{material_index}"' in app
    assert 'replace_material_from_catalog(material, selected_row)' in app
    assert 'TR-series Sylk sensors remain billable material but count as 0 AI/UI points.' in app


def test_manufacturer_standards_are_connected_to_equipment_ui():
    app = (Path(__file__).resolve().parents[1] / "app.py").read_text()
    assert '"Default controller manufacturer"' in app
    assert 'key=f"vav_controller_manufacturer_{idx}"' in app
    assert 'key=f"large_controller_manufacturer_{system_name}"' in app
    assert 'default_part_for_equipment(system_name, controller_manufacturer)' in app
