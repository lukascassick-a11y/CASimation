from __future__ import annotations

import pandas as pd
import streamlit as st

from estimator.catalog_manager import CatalogManager
from estimator.company_standards import CompanyStandards, DEFAULT_COMPANY_STANDARDS, SUPPORTED_MANUFACTURERS
from estimator.equipment_templates import equipment_template_for, option_template_for_item
from estimator.legacy_base_estimate import (
    LegacyMaterialRule,
    LegacySystemInput,
    calculate_legacy_system,
)
from estimator.legacy_options import replace_material_from_catalog, replace_rule_materials
from estimator.legacy_templates import BASE_ESTIMATE_SYSTEMS
from estimator.sylk_device_library import is_tr_sylk_sensor


def _default_choice_index(choices: pd.DataFrame, part_number: str) -> int:
    matches = choices.index[choices["part_number"].astype(str).eq(str(part_number))].tolist()
    return int(matches[0]) if matches else 0


def _material_choices(
    catalog: CatalogManager,
    material: LegacyMaterialRule,
    *,
    system_name: str,
    controller_manufacturer: str,
    show_legacy_controllers: bool,
) -> pd.DataFrame:
    template = equipment_template_for(system_name)
    if material.item == "Controller":
        return catalog.controllers(
            controller_manufacturer,
            include_legacy=show_legacy_controllers,
        )
    option_template = option_template_for_item(template, material.item, material.option)
    if option_template is None:
        return pd.DataFrame()
    if option_template.role in {"space_sensor", "duct_sensor"}:
        return catalog.sensors(keywords=option_template.keywords)
    if option_template.role == "current_switch":
        return catalog.current_switches()
    if option_template.role == "relay":
        return catalog.relays()
    return pd.DataFrame()


def _selection_label(material: LegacyMaterialRule) -> str:
    if material.item == "Controller":
        return "Controller type (Materials → Controllers)"
    if material.item == "Current Sw":
        return "Current switch type"
    if material.item == "Relay":
        return "Relay type"
    if material.item == "Temp Sensor":
        return "Duct sensor type" if "Duct" in material.option else "Space sensor type"
    return material.item


def render_vav_air_box_sections(
    parts: pd.DataFrame,
    *,
    default_controller_manufacturer: str,
    show_legacy_controllers: bool,
    catalog: CatalogManager | None = None,
    standards: CompanyStandards = DEFAULT_COMPANY_STANDARDS,
) -> list[LegacySystemInput]:
    """Render the migrated VAV/air-box workflow and return calculation inputs.

    This module owns the visible VAV configuration controls. Business formulas
    remain in ``estimator.legacy_base_estimate`` so UI changes do not alter the
    calculation engine.
    """
    st.caption(
        "VAV and CRC/Phoenix air-valve formulas. Controller, sensor, current-switch, "
        "and relay selections are linked to the Parts List catalog."
    )
    st.markdown("### VAV configuration")
    st.caption(
        "Open a VAV section to edit quantity, electrical cost per VAV, controller, "
        "sensors, current switch, and relay. Changes flow into totals and exports."
    )

    legacy_inputs: list[LegacySystemInput] = []
    catalog = catalog or CatalogManager(parts, standards)
    manufacturers = list(SUPPORTED_MANUFACTURERS)
    manufacturer_index = (
        manufacturers.index(default_controller_manufacturer)
        if default_controller_manufacturer in manufacturers
        else 0
    )

    for idx, (system_name, rule) in enumerate(BASE_ESTIMATE_SYSTEMS.items()):
        is_vav = "VAV Boxes" in system_name
        with st.expander(system_name, expanded=is_vav):
            if not is_vav:
                qty = st.number_input(
                    "Number of boxes / valves",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                    key=f"legacy_basic_{idx}",
                )
                if qty:
                    legacy_inputs.append(LegacySystemInput(rule, qty))
                continue

            qty_col, electrical_col, allowance_col = st.columns(3)
            qty = qty_col.number_input(
                "Number of VAVs",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key=f"legacy_basic_{idx}",
            )
            electrical_cost_per_vav = electrical_col.number_input(
                "Electrical cost per VAV",
                min_value=0.0,
                value=float(rule.electrical_rate_per_point),
                step=25.0,
                format="%.2f",
                key=f"vav_electrical_cost_{idx}",
                help="Editable electrical allowance applied once for each VAV.",
            )
            allowance_col.metric(
                "Electrical allowance",
                f"${float(qty) * electrical_cost_per_vav:,.2f}",
                help=f"{float(qty):,.0f} VAVs × ${electrical_cost_per_vav:,.2f} per VAV",
            )

            controller_manufacturer = st.selectbox(
                "Controller manufacturer",
                manufacturers,
                index=manufacturer_index,
                key=f"vav_controller_manufacturer_{idx}",
            )
            st.markdown("#### Controller, sensor, and accessory selections")
            st.caption(
                "Choose catalog products and set the quantity used on each VAV. "
                "TR-series Sylk sensors remain billable but count as 0 AI/UI points."
            )

            replacements: dict[int, LegacyMaterialRule] = {}
            per_unit_overrides: dict[int, float] = {}
            option_rows: list[dict[str, object]] = []

            for material_index, material in enumerate(rule.materials):
                choices = _material_choices(
                    catalog,
                    material,
                    system_name=system_name,
                    controller_manufacturer=controller_manufacturer,
                    show_legacy_controllers=show_legacy_controllers,
                )
                selected_material = material

                configurable_quantity = material.item in {"Temp Sensor", "Current Sw", "Relay"}
                include_default = material.per_unit > 0
                included = True
                per_vav = float(material.per_unit)

                if configurable_quantity:
                    include_col, quantity_col = st.columns([1, 1])
                    included = include_col.checkbox(
                        f"Include {material.item}",
                        value=include_default,
                        key=f"vav_include_{idx}_{material_index}",
                    )
                    per_vav = quantity_col.number_input(
                        f"{material.item} qty per VAV",
                        min_value=0.0,
                        value=float(material.per_unit if include_default else 1.0),
                        step=1.0,
                        disabled=not included,
                        key=f"vav_qty_per_unit_{idx}_{material_index}",
                    )
                    per_unit_overrides[material.source_row] = float(per_vav if included else 0.0)

                if not choices.empty:
                    labels = choices["label"].tolist()
                    default_part = material.part_number
                    if material.item == "Controller":
                        preferred = standards.default_controller("VAV", controller_manufacturer)
                        if preferred and choices["part_number"].astype(str).eq(preferred).any():
                            default_part = preferred
                    selected_label = st.selectbox(
                        _selection_label(material),
                        labels,
                        index=_default_choice_index(choices, default_part),
                        key=f"vav_option_{idx}_{material_index}",
                    )
                    selected_row = choices.loc[choices["label"].eq(selected_label)].iloc[0]
                    selected_material = replace_material_from_catalog(material, selected_row)
                    replacements[material_index] = selected_material

                effective_per_vav = (
                    per_unit_overrides.get(material.source_row, selected_material.per_unit)
                    if configurable_quantity
                    else selected_material.per_unit
                )
                option_rows.append(
                    {
                        "item": selected_material.item,
                        "option": selected_material.option,
                        "supplier": selected_material.supplier,
                        "part_number": selected_material.part_number,
                        "included": bool(effective_per_vav > 0),
                        "quantity_per_vav": effective_per_vav,
                        "unit_cost": selected_material.unit_cost,
                        "extended_per_vav": effective_per_vav * selected_material.unit_cost,
                        "point_classification": (
                            "Sylk device — 0 AI/UI points"
                            if is_tr_sylk_sensor(
                                option=selected_material.option,
                                part_number=selected_material.part_number,
                            )
                            else "Physical I/O / material"
                        ),
                    }
                )

            configured_rule = replace_rule_materials(rule, replacements)
            preview_input = LegacySystemInput(
                configured_rule,
                qty,
                per_unit_overrides=per_unit_overrides,
                electrical_cost_per_unit_override=electrical_cost_per_vav,
            )
            preview = calculate_legacy_system(preview_input)
            material_cost = sum(line.extended_cost for line in preview.materials)
            metric_cols = st.columns(4)
            metric_cols[0].metric("Material cost", f"${material_cost:,.2f}")
            metric_cols[1].metric("Physical points", f"{preview.total_points:,.0f}")
            metric_cols[2].metric("Sylk devices", f"{preview.sylk_devices:,.0f}")
            metric_cols[3].metric("Electrical allowance", f"${preview.electrical_allowance:,.2f}")

            st.dataframe(
                pd.DataFrame(option_rows),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "item": st.column_config.TextColumn("Item"),
                    "option": st.column_config.TextColumn("Option"),
                    "supplier": st.column_config.TextColumn("Supplier"),
                    "part_number": st.column_config.TextColumn("Part number"),
                    "included": st.column_config.CheckboxColumn("Included"),
                    "quantity_per_vav": st.column_config.NumberColumn("Qty / VAV"),
                    "unit_cost": st.column_config.NumberColumn("Unit cost", format="$%.2f"),
                    "extended_per_vav": st.column_config.NumberColumn("Cost / VAV", format="$%.2f"),
                    "point_classification": st.column_config.TextColumn("Point classification"),
                },
            )

            if qty:
                legacy_inputs.append(preview_input)

    return legacy_inputs
