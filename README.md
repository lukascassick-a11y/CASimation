<<<<<<< HEAD
# CASimation
=======
# CASimation Building Automation Estimator

A modular standalone rebuild of `Estimate Tool VER-8.6.xlsx`.

## Included in this release

- Streamlit interface
- Searchable parts catalog imported from the workbook
- County sales-tax lookup
- Material quantity, price, multiplier, and markup calculations
- Labor categories, hours, rates, and burden calculations
- Contingency, overhead, profit, and total estimate
- Crew-based project duration
- Excel and PDF exports
- Validation and calculation tests

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python extract_workbook_data.py "Estimate Tool VER-8.6.xlsx" data
streamlit run app.py
```

On macOS/Linux, activate with `source .venv/bin/activate`.

## Packaging for Windows

Streamlit applications are normally started through a small launcher. A future packaging phase can add PyInstaller plus a launcher that opens the local app in the user's browser.

## Architecture

- `app.py`: user interface
- `estimator/models.py`: typed project and estimate records
- `estimator/calculations.py`: independent calculation engine
- `estimator/validation.py`: input validation
- `estimator/data_repository.py`: pandas-based reference data access
- `estimator/reports.py`: Excel and PDF reporting
- `extract_workbook_data.py`: one-time workbook-to-CSV migration
- `tests/`: regression tests

## Migration status

This first release replaces the core cost/time engine. The following workbook-specific modules should be migrated next as separate tested components:

1. Controller and I/O sizing rules
2. Valve Schedule calculations
3. Sylk Device Tool calculations
4. Estimate option and allowance logic
5. Totals-sheet consolidation across multiple estimate alternatives
6. Exact comparison tests against representative completed workbook estimates

Keeping these rules separate prevents a direct cell-by-cell conversion from becoming difficult to maintain.

## Legacy Base Estimate migration — phase 1

The application now includes a dedicated **Legacy Base Estimate** tab and a reusable formula engine for the first six workbook sections:

- VAV Boxes with Heat
- Cooling Only VAV Boxes
- Supply Air Boxes — CRC/Phoenix LV Wiring and Integration
- Exhaust Air Boxes — CRC/Phoenix LV Wiring and Integration
- Return Air Boxes — CRC/Phoenix LV Wiring and Integration
- OR Room Pressure Monitors — CRC/Phoenix LV Wiring and Integration

The migrated engine reproduces the shared Base Estimate formulas for per-unit material quantities, material extensions, points, electrical allowances, technician hours, graphics hours, programming hours, controller count, and controller point capacity. Generated material and labor lines feed the existing estimate totals and exports.

## Version 1.2 - Larger Base Estimate equipment migration

The Legacy Base Estimate area now includes configurable templates migrated from Base Estimate rows 46-296:

- VAV Air Handling Units
- Constant Volume Air Handling Units
- Water Source Heat Pumps
- Fan Coil Units
- Unit Ventilators
- Rooftop Units
- Outdoor Air Units
- Chillers, including pump/sensor-related component rows
- Chiller Room Emergency Control Panels
- Boiler Systems, including pump/flow/pressure component rows
- Exhaust Fans

For each selected section, enter the number of systems and edit the quantity-per-unit component schedule. Rows marked as Point reproduce the source section's `N`-column point summation. The engine then calculates material quantities and extensions, point-based electrical allowance, technician hours, graphics hours, programming hours, controller quantities, and controller network capacity.

The templates preserve the original workbook row numbers to support future formula-by-formula validation and migration.

### Version 1.3: VAV / Air Valves option selection

The VAV / Air Boxes interface now includes catalog-linked selections for controller type, space sensor type, and duct sensor type. The visible Option column displays the selected description, supplier, part number, quantity per box, and multiplier-adjusted unit cost. Selected options flow into estimate totals and Excel/PDF exports.


## Version 1.4 update
- Added a clearly visible editable **Electrical cost per VAV** table above the VAV sections.
- Displays the calculated electrical cost before adding the section.
- Adds legacy electrical allowance to the estimate total and Excel/PDF exports.
- Validates that electrical cost overrides cannot be negative.


## Version 1.5 update
- VAV controller dropdowns now use the complete priced **Materials → Controllers** category list.
- Controller selection updates description, supplier, part number, multiplier-adjusted unit cost, totals, and exports.
- VAV electrical allowance is now explicitly entered and calculated **per VAV**.

## Optimizer Controller Library and Sylk Rules

- Approved controller choices are limited to the Honeywell Optimizer product line.
- Both `Optimizer` and the legacy catalog spelling `Optimzer` are recognized.
- The library separates Optimizer Unitary controllers, Optimizer Plant controllers, and compatible I/O modules.
- Siemens controllers are excluded.
- VAV controller dropdowns default to an Optimizer Unitary VAV controller.
- TR21, TR23, TR40, TR42, TR100, and TR120 sensors connect through the Sylk bus and therefore count as **0 AI/UI physical points**. They remain material items and are labeled as Sylk devices in the VAV option table.

## Version 1.7 — Sylk Device Library

- Added a dedicated Honeywell TR-series Sylk Device Library.
- TR21, TR23, TR40, TR42, TR100, and TR120 products remain billable materials.
- Each selected TR-series sensor contributes 1 Sylk device and 0 AI/UI points.
- The zero-I/O rule is enforced by the calculation engine, including configurable large-equipment sections.
- Discontinued Sylk devices are hidden by default and can be displayed from the library tab.
- Controller and Sylk capability records contain no engineering or programming labor factors.
- Normalized the legacy `Optimzer` spelling to `Optimizer` in controller-library display data.

## Version 1.8 — Visible Controller Standards

- Added top-level Controller Library and Sylk Device Library tabs.
- Added visible company-default controller table.
- VAV default: VAA-VA75MB24NMC.
- Fan coil, unit ventilator, and heat-pump default: UN-RS0844MS24NMC.
- AHU, boiler, chiller, pump, and other large-equipment default: UN-RL1644MS24NMC.
- Added controller dropdowns directly inside large-equipment sections.
- Normalized Optimzer to Optimizer in the shipped catalog and templates.
- Siemens controllers are Removed; Johnson Controls FX- products are Legacy and hidden by default; F4- products remain selectable.
- TR-series Sylk devices remain billable and contribute 0 AI/UI points.


## Version 1.9 correction

- The VAV electrical rate is now edited in a visible table at the top of **Legacy Base Estimate → VAV / Air Boxes**.
- Each row is an independent per-VAV rate.
- The formula is `VAV quantity × electrical cost per VAV`.
- The rate is no longer hidden inside an expander or treated as a per-point value.

## Version 2.1 interface migration

The VAV estimating screen now exposes the following controls directly inside each VAV section:

- Number of VAVs
- Editable electrical cost per VAV
- Live electrical allowance (`quantity x cost per VAV`)
- Controller manufacturer and controller model
- Space sensor type
- Duct sensor type, when required by the VAV template

Selected sensors update the material description, supplier, part number, catalog-adjusted unit cost, estimate totals, and exports. TR-series Sylk sensors remain billable but contribute zero AI/UI points.
>>>>>>> dbc23f9 (Initial CASimation estimator source)
