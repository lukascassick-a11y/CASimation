from __future__ import annotations

from .legacy_base_estimate import LegacyMaterialRule, LegacySystemRule

# First migrated Base Estimate sections. Values are taken directly from the
# corresponding section headers and material rows in Estimate Tool VER-8.6.
BASE_ESTIMATE_SYSTEMS: dict[str, LegacySystemRule] = {
    "VAV Boxes w Heat": LegacySystemRule(
        name="VAV Boxes w Heat",
        points_per_unit=1.0,
        electrical_rate_per_point=550.0,
        technician_hours_per_point=1.0,
        graphics_hours_per_unit=0.25,
        programming_hours_per_unit=0.25,
        controller_points_each=70.0,
        materials=(
            LegacyMaterialRule("Controller", "Optimizer BACnet MSTP VAV Cntr w Act & VP, Bluetooth, 7 UIO, 5 SSR", 1.0, "VAA-VA75MB24NMC", 281.3558, source_row=1),
            LegacyMaterialRule("Temp Sensor", "TR100 Space with LCD", 1.0, "TR100-T-G", 128.71265, source_row=2),
            LegacyMaterialRule("Temp Sensor", "Duct Insertion Sensor", 1.0, "C7041B2005", 23.18855, source_row=3),
            LegacyMaterialRule("Current Sw", "Digital Status Switch", 0.0, "H600", 31.43, source_row=4),
            LegacyMaterialRule("Relay", "RIB Pilot Relay", 0.0, "RIBU1C", 14.36, source_row=5),
            LegacyMaterialRule("VAV HW Valve 2W & 3-way NSR", "", 0.0, "N/A", 150.0, source_row=6),
            LegacyMaterialRule("Air Flow Monitor", "Retrofit Flow Ring for VAV Boxes", 0.0, "36FMI", 95.0, source_row=7),
        ),
    ),
    "Cooling Only VAV Boxes": LegacySystemRule(
        name="Cooling Only VAV Boxes",
        points_per_unit=1.0,
        electrical_rate_per_point=550.0,
        technician_hours_per_point=1.0,
        graphics_hours_per_unit=0.25,
        programming_hours_per_unit=0.25,
        controller_points_each=70.0,
        materials=(
            LegacyMaterialRule("Controller", "Optimizer BACnet MSTP VAV Cntr w Act & VP, Bluetooth, 7 UIO, 5 SSR", 1.0, "VAA-VA75MB24NMC", 281.3558, source_row=101),
            LegacyMaterialRule("Temp Sensor", "TR100 Space with LCD", 1.0, "TR100-T-G", 128.71265, source_row=102),
            LegacyMaterialRule("Transformer", "40 VA", 0.0, "TR40VA001", 17.76, source_row=103),
            LegacyMaterialRule("Air Flow Monitor", "Retrofit Flow Ring for VAV Boxes", 0.0, "36FMI", 95.0, source_row=104),
        ),
    ),
    "Supply Air Boxes - CRC/Phoenix LV Wiring and Integration": LegacySystemRule(
        name="Supply Air Boxes - CRC/Phoenix LV Wiring and Integration",
        points_per_unit=1.0,
        electrical_rate_per_point=750.0,
        technician_hours_per_point=1.0,
        graphics_hours_per_unit=0.25,
        programming_hours_per_unit=0.25,
    ),
    "Exhaust Air Boxes - CRC/Phoenix LV Wiring and Integration": LegacySystemRule(
        name="Exhaust Air Boxes - CRC/Phoenix LV Wiring and Integration",
        points_per_unit=1.0,
        electrical_rate_per_point=750.0,
        technician_hours_per_point=1.0,
        graphics_hours_per_unit=0.25,
        programming_hours_per_unit=0.25,
    ),
    "Return Air Boxes - CRC/Phoenix LV Wiring and Integration": LegacySystemRule(
        name="Return Air Boxes - CRC/Phoenix LV Wiring and Integration",
        points_per_unit=1.0,
        electrical_rate_per_point=750.0,
        technician_hours_per_point=1.0,
        graphics_hours_per_unit=0.25,
        programming_hours_per_unit=0.25,
    ),
    "OR Room Pressure Monitors - CRC/Phoenix LV Wiring and Integration": LegacySystemRule(
        name="OR Room Pressure Monitors - CRC/Phoenix LV Wiring and Integration",
        points_per_unit=1.0,
        electrical_rate_per_point=750.0,
        technician_hours_per_point=1.0,
        graphics_hours_per_unit=0.25,
        programming_hours_per_unit=0.25,
    ),
}
