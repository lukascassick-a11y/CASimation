from estimator.equipment_templates import equipment_template_for, option_template_for_item


def test_vav_template_defines_required_configurable_roles():
    template = equipment_template_for("VAV Boxes w Heat")
    assert template.key == "vav"
    roles = {option.role for option in template.options}
    assert roles == {"space_sensor", "duct_sensor", "current_switch", "relay"}


def test_vav_sensor_role_is_selected_from_material_option():
    template = equipment_template_for("Cooling Only VAV Boxes")
    assert option_template_for_item(template, "Temp Sensor", "TR100 Space").role == "space_sensor"
    assert option_template_for_item(template, "Temp Sensor", "Duct Insertion Sensor").role == "duct_sensor"
