# CASimation Architecture

CASimation separates user-interface code, business rules, reference data, and report generation.

## Main layers

- `app.py` — Streamlit user interface and workflow orchestration.
- `estimator/models.py` — typed estimate and project data structures.
- `estimator/calculations.py` — project-level cost and duration calculations.
- `estimator/legacy_base_estimate.py` — reusable legacy Base Estimate formula engine.
- `estimator/legacy_templates.py` — VAV and air-valve templates.
- `estimator/legacy_large_templates.py` — larger equipment templates.
- `estimator/controller_catalog.py` — manufacturer, lifecycle, and default-selection rules.
- `estimator/controller_library.py` — controller capability records.
- `estimator/sylk_device_library.py` — Sylk classification and zero-I/O rules.
- `estimator/reports.py` — Excel and PDF exports.
- `data/` — normalized reference tables used at runtime.
- `tests/` — regression tests for formulas and UI contracts.

## Design principle

Workbook cell references are treated as migration evidence, not as the permanent application architecture. Business rules should be expressed as named, tested Python functions.
