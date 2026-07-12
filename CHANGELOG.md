## Unreleased

### Changed
- Renamed **Legacy Base Estimate** to **Controls Estimate** and moved it to the first tab.
- Renamed **Estimate** to **Totals Summary** and moved it to the second tab.
- Set the primary workflow order to Controls Estimate, Totals Summary, Labor, and Materials.

# Changelog

All notable changes to CASimation are recorded here.

## [Unreleased]

### Planned
- Continue formula-by-formula migration from the legacy Base Estimate sheets.
- Add persistent project save/open support.
- Add controller I/O capacity validation and expansion-module recommendations.

## [2.1.0] - 2026-07-12

### Added
- VAV quantity, electrical cost per VAV, controller, and sensor controls in the estimating workflow.
- Live VAV electrical allowance calculation.
- Honeywell Optimizer and Johnson Controls F4 controller standards.
- Controller and Sylk device libraries.

### Changed
- TR-series Sylk sensors remain billable but consume zero AI/UI points.
- Siemens controllers are excluded.
- Johnson Controls FX products are treated as legacy and hidden by default.
- Catalog spelling normalized from `Optimzer` to `Optimizer`.

## Unreleased

### Added
- Central `CatalogManager` for controller, sensor, current-switch, and relay selections.
- Central `CompanyStandards` configuration for manufacturer policies and equipment controller defaults.
- Reusable equipment-template definitions, beginning with the VAV template.
- Behavioral tests for catalog lifecycle filtering, company defaults, and equipment-template roles.

### Changed
- VAV UI now consumes the shared catalog manager, company standards, and VAV equipment template instead of embedding catalog filters and default-controller rules.
