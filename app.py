from __future__ import annotations
from datetime import date
from pathlib import Path
import pandas as pd
import streamlit as st
from estimator import (ProjectInfo, MaterialLine, LaborLine, EstimateSettings, calculate_estimate,
    BASE_ESTIMATE_SYSTEMS, LARGE_EQUIPMENT_SYSTEMS, LegacySystemInput, calculate_legacy_system, combine_legacy_results,
    catalog_choices, catalog_choices_by_category, replace_material_from_catalog, replace_rule_materials,
    build_optimizer_library, optimizer_controller_choices, default_optimizer_controller, is_tr_sylk_sensor,
    build_sylk_device_library, build_controller_catalog, controller_choices, default_part_for_equipment, DEFAULT_CONTROLLERS,
    HONEYWELL_DEFAULT_CONTROLLERS, JOHNSON_CONTROLS_DEFAULT_CONTROLLERS, SUPPORTED_MANUFACTURERS)
from estimator.data_repository import DataRepository
from estimator.reports import build_excel, build_pdf
from estimator.validation import validate_project, ValidationError
from ui.vav_page import render_vav_air_box_sections

ROOT = Path(__file__).resolve().parent
repo = DataRepository(ROOT / "data")
st.set_page_config(page_title="CASimation Estimate Tool", layout="wide")
st.title("CASimation Building Automation Estimator")
st.caption("Standalone estimator rebuilt from Estimate Tool VER-8.6")

parts = repo.load_parts(); taxes = repo.load_taxes()
with st.sidebar:
    st.header("Project")
    project_name = st.text_input("Project name")
    customer = st.text_input("Customer")
    estimator = st.text_input("Estimator")
    estimate_date = st.date_input("Estimate date", date.today())
    county_options = [""] + sorted(taxes["county"].astype(str).unique().tolist()) if not taxes.empty else [""]
    county = st.selectbox("County", county_options)
    state = st.text_input("State", value="NC")
    project_type = st.selectbox("Project type", ["Retrofit", "New Construction", "Service", "Design-Build"])
    st.header("Company Standards")
    default_controller_manufacturer = st.selectbox(
        "Default controller manufacturer",
        list(SUPPORTED_MANUFACTURERS),
        index=0,
        help="This standard preselects and filters controller choices in the actual equipment screens.",
    )
    show_legacy_controllers = st.checkbox(
        "Allow legacy controllers in equipment lists",
        value=False,
        help="Shows Johnson Controls FX products for historical work. Siemens and Removed products remain unavailable.",
    )
    st.header("Pricing")
    tax_rate = st.number_input("Tax rate (%)", min_value=0.0, max_value=30.0, value=repo.tax_rate_for(county)*100, step=.01)/100
    material_markup = st.number_input("Material markup (%)", 0.0, 200.0, 15.0)/100
    labor_markup = st.number_input("Labor markup (%)", 0.0, 200.0, 0.0)/100
    contingency = st.number_input("Contingency (%)", 0.0, 100.0, 5.0)/100
    overhead = st.number_input("Overhead (%)", 0.0, 100.0, 10.0)/100
    profit = st.number_input("Profit (%)", 0.0, 100.0, 10.0)/100
    crew_size = st.number_input("Crew size", min_value=.25, value=2.0, step=.25)
    hours_per_day = st.number_input("Hours per day", min_value=1.0, value=8.0)

tab1, tab2, legacy_tab, tab3, tab4, standards_tab, controller_library_tab, sylk_library_tab = st.tabs([
    "Materials", "Labor", "Legacy Base Estimate", "Estimate", "Assumptions",
    "Company Standards", "Controller Library", "Sylk Device Library"
])
with tab1:
    st.subheader("Material and Equipment List")
    search = st.text_input("Search parts catalog", placeholder="controller, sensor, thermostat...")
    filtered = parts
    if search and not parts.empty:
        mask = parts.astype(str).apply(lambda c: c.str.contains(search, case=False, na=False)).any(axis=1)
        filtered = parts[mask].head(100)
    if not filtered.empty:
        st.dataframe(filtered.head(100), use_container_width=True, hide_index=True)
    default_materials = pd.DataFrame(columns=["item","option","supplier","part_number","quantity","unit_cost","multiplier"])
    material_df = st.data_editor(default_materials, num_rows="dynamic", use_container_width=True,
        column_config={"quantity": st.column_config.NumberColumn(min_value=0.0), "unit_cost": st.column_config.NumberColumn(format="$%.2f", min_value=0.0), "multiplier": st.column_config.NumberColumn(min_value=0.0, default=1.0)})
with legacy_tab:
    st.subheader("Migrated Base Estimate Systems")
    basic_subtab, large_subtab, controller_subtab, sylk_subtab = st.tabs(["VAV / Air Boxes", "Large Equipment", "Controller Library", "Sylk Device Library"])
    legacy_inputs = []

    with basic_subtab:
        legacy_inputs.extend(
            render_vav_air_box_sections(
                parts,
                default_controller_manufacturer=default_controller_manufacturer,
                show_legacy_controllers=show_legacy_controllers,
            )
        )


    with controller_subtab:
        st.caption("Approved Honeywell Optimizer controllers and compatible I/O modules extracted from the Parts List. Siemens products are excluded.")
        optimizer_library = build_optimizer_library(parts)
        family_filter = st.multiselect(
            "Product families",
            ["Optimizer Unitary", "Optimizer Plant"],
            default=["Optimizer Unitary", "Optimizer Plant"],
        )
        type_filter = st.multiselect(
            "Product types",
            ["Controller", "I/O Module"],
            default=["Controller", "I/O Module"],
        )
        shown_library = optimizer_library.loc[
            optimizer_library["family"].isin(family_filter)
            & optimizer_library["product_type"].isin(type_filter)
        ]
        st.dataframe(
            shown_library,
            use_container_width=True,
            hide_index=True,
            column_config={
                "unit_cost": st.column_config.NumberColumn("Unit cost", format="$%.2f"),
                "sylk_capable": st.column_config.CheckboxColumn("Sylk capable"),
            },
        )
        st.info("TR21, TR23, TR40, TR42, TR100, and TR120 sensor products are treated as Sylk devices. They remain in material costs but contribute 0 AI/UI points.")

    with sylk_subtab:
        st.caption("Honeywell TR-series sensors connected to Optimizer controllers over the Sylk bus. These remain material items but consume zero AI/UI points.")
        sylk_library = build_sylk_device_library(parts)
        show_discontinued_sylk = st.checkbox("Show discontinued Sylk devices", value=False)
        if not show_discontinued_sylk:
            sylk_library = sylk_library.loc[sylk_library["catalog_status"].eq("Active")].copy()
        st.dataframe(
            sylk_library,
            use_container_width=True,
            hide_index=True,
            column_config={
                "unit_cost": st.column_config.NumberColumn("Unit cost", format="$%.2f"),
                "uses_sylk_bus": st.column_config.CheckboxColumn("Uses Sylk bus"),
                "consumes_ai_ui": st.column_config.CheckboxColumn("Consumes AI/UI"),
                "ai_ui_points": st.column_config.NumberColumn("AI/UI points"),
                "sylk_device_count": st.column_config.NumberColumn("Sylk count"),
            },
        )
        st.info("Sizing rule: every selected TR-series sensor adds 1 Sylk device and 0 physical AI/UI points. Engineering and programming labor are not stored in either the Controller Library or the Sylk Device Library.")

    with large_subtab:
        st.caption("Rows 46-296: configure equipment quantity and component quantities per unit. Point-producing rows match each legacy Excel section formula.")
        selected_large = st.multiselect(
            "Equipment sections to configure",
            list(LARGE_EQUIPMENT_SYSTEMS),
            placeholder="Select AHUs, chillers, boiler systems, exhaust fans...",
        )
        for system_name in selected_large:
            rule = LARGE_EQUIPMENT_SYSTEMS[system_name]
            with st.expander(system_name, expanded=True):
                qty = st.number_input("Number of systems", min_value=0.0, value=1.0, step=1.0, key=f"large_qty_{system_name}")
                controller_manufacturer = st.selectbox(
                    "Controller manufacturer",
                    list(SUPPORTED_MANUFACTURERS),
                    index=list(SUPPORTED_MANUFACTURERS).index(default_controller_manufacturer),
                    key=f"large_controller_manufacturer_{system_name}",
                )
                large_choices = controller_choices(
                    parts,
                    manufacturer=controller_manufacturer,
                    include_legacy=show_legacy_controllers,
                )
                configured_rule = rule
                controller_rows = [i for i, m in enumerate(rule.materials) if m.item.strip().casefold() == "controller"]
                if controller_rows and large_choices.empty:
                    st.warning(f"No active {controller_manufacturer} controllers are available for this section.")
                if controller_rows and not large_choices.empty:
                    preferred_part = default_part_for_equipment(system_name, controller_manufacturer)
                    preferred_matches = large_choices.index[large_choices["part_number"].eq(preferred_part)].tolist()
                    selected_controller_label = st.selectbox(
                        "Controller",
                        large_choices["label"].tolist(),
                        index=preferred_matches[0] if preferred_matches else 0,
                        key=f"large_controller_{system_name}",
                        help=f"Company default for this equipment: {preferred_part}",
                    )
                    selected_controller = large_choices.loc[large_choices["label"].eq(selected_controller_label)].iloc[0]
                    replacements = {
                        i: replace_material_from_catalog(rule.materials[i], selected_controller)
                        for i in controller_rows
                    }
                    configured_rule = replace_rule_materials(rule, replacements)
                    st.caption(f"Default standard: {preferred_part} | Selected: {selected_controller['part_number']}")
                seed = pd.DataFrame([
                    {
                        "source_row": m.source_row,
                        "item": m.item,
                        "option": m.option,
                        "part_number": m.part_number,
                        "quantity_per_unit": m.per_unit,
                        "counts_as_point": m.contributes_to_points,
                        "unit_cost": m.unit_cost,
                    }
                    for m in configured_rule.materials
                ])
                configured = st.data_editor(
                    seed,
                    key=f"large_components_{system_name}",
                    use_container_width=True,
                    hide_index=True,
                    disabled=["source_row", "item", "option", "part_number", "counts_as_point", "unit_cost"],
                    column_config={
                        "source_row": None,
                        "quantity_per_unit": st.column_config.NumberColumn("Qty / unit", min_value=0.0, step=1.0),
                        "counts_as_point": st.column_config.CheckboxColumn("Point"),
                        "unit_cost": st.column_config.NumberColumn("Unit cost", format="$%.2f"),
                            "point_classification": st.column_config.TextColumn("Point classification"),
                    },
                )
                overrides = {int(r.source_row): float(r.quantity_per_unit or 0) for r in configured.itertuples()}
                if qty:
                    legacy_inputs.append(LegacySystemInput(configured_rule, qty, overrides))

    legacy_results = [calculate_legacy_system(x) for x in legacy_inputs]
    if legacy_results:
        legacy_summary = pd.DataFrame([{
            "System": r.name, "Quantity": r.quantity, "Points": r.total_points,
            "Electrical Cost / Unit": (r.electrical_allowance / r.quantity) if r.quantity else 0.0,
            "Electrical Allowance": r.electrical_allowance, "Tech Hours": r.technician_hours,
            "Graphics Hours": r.graphics_hours, "Programming Hours": r.programming_hours,
            "Controller Capacity": r.controller_points, "Sylk Devices": r.sylk_devices,
            "Material Cost": sum(x.extended_cost for x in r.materials),
        } for r in legacy_results])
        st.dataframe(legacy_summary, use_container_width=True, hide_index=True)
        generated_materials, generated_labor, electrical_allowance = combine_legacy_results(legacy_results)
        if electrical_allowance:
            generated_materials.append(MaterialLine(
                item="Legacy Electrical Allowance",
                option="VAV / air-valve and large-equipment electrical cost",
                supplier="Electrical Subcontractor",
                part_number="ELEC-ALLOW",
                quantity=1.0,
                unit_cost=electrical_allowance,
                multiplier=1.0,
                category="Electrical Allowance",
            ))
        st.info(f"Generated {len(generated_materials)} material lines and included ${electrical_allowance:,.2f} in electrical allowance in the estimate total.")
    else:
        generated_materials, generated_labor, electrical_allowance = [], [], 0.0


with standards_tab:
    st.subheader("Company Controller Standards")
    st.success(f"Active default manufacturer: {default_controller_manufacturer}")
    st.caption("These settings drive the controller dropdowns inside VAV and large-equipment estimating screens.")
    standards_rows = []
    equipment_names = ["VAV / Air Valves", "Fan Coils", "Unit Ventilators", "Heat Pumps", "AHUs", "Boilers", "Chillers", "Pump Systems"]
    for equipment_name in equipment_names:
        standards_rows.append({
            "Equipment": equipment_name,
            "Honeywell Optimizer Default": default_part_for_equipment(equipment_name, "Honeywell"),
            "Johnson Controls F4 Default": default_part_for_equipment(equipment_name, "Johnson Controls"),
            "Active Project Default": default_part_for_equipment(equipment_name, default_controller_manufacturer),
        })
    st.dataframe(pd.DataFrame(standards_rows), use_container_width=True, hide_index=True)
    st.markdown("### Product-list rules")
    st.markdown("""
- Honeywell uses the **Optimizer** product line.
- Johnson Controls **FX-** products are hidden unless legacy products are enabled.
- Johnson Controls **F4-CVM3050-0** is the VAV default; **F4-CGM09090-0** is standard for other equipment.
- Siemens products are **Removed** and never selectable.
- Phoenix Controls is available as a manufacturer filter when matching controller records exist.
""")
    st.info("Defaults affect new selections only. Existing material lines retain the controller already saved in the estimate.")

with controller_library_tab:
    st.subheader("Controller Library and Company Defaults")
    st.success(f"These standards are active in the equipment selectors. Current manufacturer: {default_controller_manufacturer}")
    defaults_df = pd.DataFrame([
        {"Equipment": "VAV / Air Valves", "Default Controller": DEFAULT_CONTROLLERS["VAV"]},
        {"Equipment": "Fan Coils", "Default Controller": DEFAULT_CONTROLLERS["Fan Coil"]},
        {"Equipment": "Unit Ventilators", "Default Controller": DEFAULT_CONTROLLERS["Unit Ventilator"]},
        {"Equipment": "Heat Pumps", "Default Controller": DEFAULT_CONTROLLERS["Heat Pump"]},
        {"Equipment": "AHUs", "Default Controller": DEFAULT_CONTROLLERS["AHU"]},
        {"Equipment": "Boilers", "Default Controller": DEFAULT_CONTROLLERS["Boiler"]},
        {"Equipment": "Chillers", "Default Controller": DEFAULT_CONTROLLERS["Chiller"]},
        {"Equipment": "Pump Systems", "Default Controller": DEFAULT_CONTROLLERS["Pump"]},
    ])
    st.dataframe(defaults_df, use_container_width=True, hide_index=True)
    controller_catalog = build_controller_catalog(parts)
    library_manufacturer = st.multiselect("Manufacturers", list(SUPPORTED_MANUFACTURERS), default=list(SUPPORTED_MANUFACTURERS))
    show_legacy = st.checkbox("Show legacy products (including Johnson Controls FX-)", value=show_legacy_controllers, key="library_show_legacy")
    shown_status = ["Active", "Legacy"] if show_legacy else ["Active"]
    shown_catalog = controller_catalog.loc[controller_catalog["catalog_status"].isin(shown_status) & controller_catalog["manufacturer"].isin(library_manufacturer)].copy()
    st.dataframe(
        shown_catalog,
        use_container_width=True,
        hide_index=True,
        column_config={
            "unit_cost": st.column_config.NumberColumn("Unit cost", format="$%.2f"),
            "selectable": st.column_config.CheckboxColumn("Selectable"),
        },
    )
    st.info("Siemens products are Removed and never appear in selectors. Johnson Controls FX- products are Legacy and hidden by default. Johnson Controls F4- products remain selectable.")

with sylk_library_tab:
    st.subheader("Sylk Device Library")
    st.success("TR-series devices are billable material items but consume 0 AI/UI points.")
    visible_sylk = build_sylk_device_library(parts)
    show_discontinued = st.checkbox("Show discontinued Sylk products", value=False, key="top_sylk_discontinued")
    if not show_discontinued:
        visible_sylk = visible_sylk.loc[visible_sylk["catalog_status"].eq("Active")].copy()
    st.dataframe(visible_sylk, use_container_width=True, hide_index=True)
    st.info("Each selected TR21, TR23, TR40, TR42, TR100, or TR120 device adds 1 Sylk device and 0 physical AI/UI points.")

with tab2:
    st.subheader("Labor")
    labor_seed = pd.DataFrame([
        {"category":"Engineering","hours":0.0,"hourly_rate":125.0,"burden_multiplier":1.0},
        {"category":"Programming","hours":0.0,"hourly_rate":125.0,"burden_multiplier":1.0},
        {"category":"Graphics","hours":0.0,"hourly_rate":110.0,"burden_multiplier":1.0},
        {"category":"Installation","hours":0.0,"hourly_rate":95.0,"burden_multiplier":1.0},
        {"category":"Commissioning","hours":0.0,"hourly_rate":115.0,"burden_multiplier":1.0},
        {"category":"Project Management","hours":0.0,"hourly_rate":125.0,"burden_multiplier":1.0},
    ])
    labor_df = st.data_editor(labor_seed, num_rows="dynamic", use_container_width=True)

manual_materials = [MaterialLine(item=str(r.get("item", "")), option=str(r.get("option", "")), supplier=str(r.get("supplier", "")), part_number=str(r.get("part_number", "")), quantity=float(r.get("quantity",0) or 0), unit_cost=float(r.get("unit_cost",0) or 0), multiplier=float(r.get("multiplier",1) or 1)) for _,r in material_df.fillna("").iterrows() if str(r.get("item","")).strip()]
manual_labor = [LaborLine(category=str(r.get("category", "Labor")), hours=float(r.get("hours",0) or 0), hourly_rate=float(r.get("hourly_rate",0) or 0), burden_multiplier=float(r.get("burden_multiplier",1) or 1)) for _,r in labor_df.fillna(0).iterrows()]
materials = manual_materials + generated_materials
labor = manual_labor + generated_labor
project = ProjectInfo(project_name, customer, estimator, estimate_date, county, state, project_type)
settings = EstimateSettings(tax_rate, material_markup, labor_markup, contingency, overhead, profit, crew_size, hours_per_day)
try:
    result = calculate_estimate(materials, labor, settings)
except ValidationError as exc:
    st.error(str(exc)); st.stop()

with tab3:
    st.subheader("Estimate Summary")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Grand Total", f"${result.grand_total:,.2f}")
    c2.metric("Materials + Tax", f"${result.taxable_material + result.tax:,.2f}")
    c3.metric("Labor Hours", f"{result.total_labor_hours:,.1f}")
    c4.metric("Duration", f"{result.duration_days:,.1f} days")
    summary = pd.DataFrame({"Cost Component":["Material Base","Material Markup","Sales Tax","Labor Base","Labor Markup","Contingency","Overhead","Profit"],"Amount":[result.material_base,result.material_markup,result.tax,result.labor_base,result.labor_markup,result.contingency,result.overhead,result.profit]})
    st.dataframe(summary.style.format({"Amount":"${:,.2f}"}), use_container_width=True, hide_index=True)
    try:
        validate_project(project)
        excel = build_excel(project, materials, labor, settings, result)
        pdf = build_pdf(project, materials, labor, settings, result)
        name = project.project_name.strip().replace(" ", "_")
        col1,col2 = st.columns(2)
        col1.download_button("Export Excel", excel, f"{name}_estimate.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        col2.download_button("Export PDF", pdf, f"{name}_estimate.pdf", "application/pdf", use_container_width=True)
    except ValidationError as exc:
        st.info(str(exc))
with tab4:
    st.write("The estimator includes migrated Base Estimate formulas for VAV/air-box systems and configurable large-equipment sections through row 296, including AHUs, heat pumps, fan coils, rooftop and outdoor-air units, chillers, boiler systems, emergency panels, and exhaust fans.")
    st.write("Workbook-specific controller sizing, valve sizing, Sylk-device rules, and every legacy option formula are intentionally isolated for phased migration and regression testing.")
