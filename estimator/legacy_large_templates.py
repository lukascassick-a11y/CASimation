from __future__ import annotations

from .legacy_base_estimate import LegacyMaterialRule, LegacySystemRule

# Migrated from Base Estimate rows 46-296 in Estimate Tool VER-8.6.
LARGE_EQUIPMENT_SYSTEMS: dict[str, LegacySystemRule] = {
    'VAV Air Handling Unit': LegacySystemRule(
        name='VAV Air Handling Unit',
        points_per_unit=0.0, electrical_rate_per_point=350.0,
        technician_hours_per_point=1.0,
        graphics_hours_per_unit=4.0, programming_hours_per_unit=6.0,
        points_from_materials=True,
        materials=(
            LegacyMaterialRule(
                item='Controller', option='Optimizer Plant Cntr, 1 IP, 3 Ethernet Switched+4 RS485 Ports', per_unit=0.0, part_number='N-ADV-134-H-C', unit_cost=875.1457,
                source_row=47, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='Optimizer License with 18 Month SMA', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=48, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='I/O Module', option='Optimizer Unitary Cntr 5-UI, 5-DI, 4-AO, 4-DO I/O Module', per_unit=0.0, part_number='ISMA-B-MIX18', unit_cost=338.81,
                source_row=49, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Phoenix Controller Core License', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=50, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Phoenix ILC SMA', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=51, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Panel - Enclosure w Subpanel', option='Nema-1 Medium', per_unit=0.0, part_number='RET1-262007BT-P', unit_cost=436.83,
                source_row=52, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Relay', option='24VAC DPDT with Base', per_unit=0.0, part_number='RH2B-UAC24 + SH2B-05', unit_cost=8.120000000000001,
                source_row=53, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Transformer', option='75 VA with circuit breaker', per_unit=0.0, part_number='TR75VA004', unit_cost=42.14,
                source_row=54, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Power Supply', option='24VDC Panel Mounted - 1.3 A', per_unit=0.0, part_number='PS5R-VB24', unit_cost=50.96,
                source_row=55, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Static Pressure Tips', option='Duct Kit', per_unit=0.0, part_number='A-302K + A-345k', unit_cost=17.9,
                source_row=56, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Thermostat', option='Low Limit', per_unit=0.0, part_number='A11A-1C', unit_cost=270.31,
                source_row=57, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Filter Status', option='Digital Status', per_unit=0.0, part_number='AFS-145', unit_cost=40.9,
                source_row=58, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Press Transmitter', option='Duct Static Air', per_unit=0.0, part_number='PX3DXX02', unit_cost=130.12,
                source_row=59, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Press Transmitter', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=60, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Press Transmitter', option='High Static Limit Switch', per_unit=0.0, part_number='1900-5-MR', unit_cost=111.93,
                source_row=61, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Current Sw', option='Digital for VFD Status', per_unit=0.0, part_number='H904', unit_cost=88.31,
                source_row=62, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Damper Actuator', option='Large - Spring Return', per_unit=0.0, part_number='MS7520A2007', unit_cost=446.4658,
                source_row=63, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='Averaging Sensor', per_unit=0.0, part_number='C7041R2018', unit_cost=166.9283,
                source_row=64, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='Duct Temp/Humidity', per_unit=0.0, part_number='H7735B2018', unit_cost=266.23465,
                source_row=65, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Humidity', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=66, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Humidity', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=67, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Carbon Dioxide Sensor', option='Space CO2 wo LCD', per_unit=0.0, part_number='C7263A1008', unit_cost=355.7389,
                source_row=68, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Carbon Dioxide Sensor', option='Duct CO2 wo LCD', per_unit=0.0, part_number='C7632B1002', unit_cost=331.2441,
                source_row=69, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Emergency Stop Switch', option='Flush Mtd', per_unit=0.0, part_number='AOW401R + SSG1-67', unit_cost=75.69000000000001,
                source_row=70, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Air Flow Monitor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=71, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='See Valve Quote', option='', per_unit=0.0, part_number='N/A', unit_cost=0.0,
                source_row=72, contributes_to_points=True, controller_points_each=0.0,
            ),
        ),
    ),
    'Constant Volume Air Handling Units': LegacySystemRule(
        name='Constant Volume Air Handling Units',
        points_per_unit=0.0, electrical_rate_per_point=350.0,
        technician_hours_per_point=1.0,
        graphics_hours_per_unit=4.0, programming_hours_per_unit=6.0,
        points_from_materials=True,
        materials=(
            LegacyMaterialRule(
                item='Controller', option='Optimizer Plant Cntr, 1 IP, 3 Ethernet Switched+4 RS485 Ports', per_unit=0.0, part_number='N-ADV-134-H-C', unit_cost=875.1457,
                source_row=78, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='Optimizer License with 18 Month SMA', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=79, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='I/O Module', option='Optimizer Unitary Cntr 5-UI, 5-DI, 4-AO, 4-DO I/O Module', per_unit=0.0, part_number='ISMA-B-MIX18', unit_cost=338.81,
                source_row=80, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Phoenix Controller Core License', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=81, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Phoenix ILC SMA', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=82, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Panel - Enclosure w Subpanel', option='Nema-1 Medium', per_unit=0.0, part_number='RET1-262007BT-P', unit_cost=436.83,
                source_row=83, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Relay', option='24VAC DPDT with Base', per_unit=0.0, part_number='RH2B-UAC24 + SH2B-05', unit_cost=8.120000000000001,
                source_row=84, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Transformer', option='75 VA with circuit breaker', per_unit=0.0, part_number='TR75VA004', unit_cost=42.14,
                source_row=85, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Power Supply', option='24VDC Panel Mounted - 1.3 A', per_unit=0.0, part_number='PS5R-VB24', unit_cost=50.96,
                source_row=86, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Static Pressure Tips', option='Duct Kit', per_unit=0.0, part_number='A-302K + A-345k', unit_cost=17.9,
                source_row=87, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Thermostat', option='Low Limit', per_unit=0.0, part_number='A11A-1C', unit_cost=270.31,
                source_row=88, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Filter Status', option='Digital Status', per_unit=0.0, part_number='AFS-145', unit_cost=40.9,
                source_row=89, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Press Transmitter', option='Duct Static Air', per_unit=0.0, part_number='PX3DXX02', unit_cost=130.12,
                source_row=90, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Current Sw', option='Digital for VFD Status', per_unit=0.0, part_number='H904', unit_cost=88.31,
                source_row=91, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Damper Actuator', option='Large - Spring Return', per_unit=0.0, part_number='MS7520A2007', unit_cost=446.4658,
                source_row=92, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='Averaging Sensor', per_unit=0.0, part_number='C7041R2018', unit_cost=166.9283,
                source_row=93, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='Duct Temp/Humidity', per_unit=0.0, part_number='H7735B2018', unit_cost=266.23465,
                source_row=94, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Humidity', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=95, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Humidity', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=96, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Carbon Dioxide Sensor', option='Space CO2 wo LCD', per_unit=0.0, part_number='C7263A1008', unit_cost=355.7389,
                source_row=97, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Carbon Dioxide Sensor', option='Duct CO2 wo LCD', per_unit=0.0, part_number='C7632B1002', unit_cost=331.2441,
                source_row=98, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Emergency Stop Switch', option='Flush Mtd', per_unit=0.0, part_number='AOW401R + SSG1-67', unit_cost=75.69000000000001,
                source_row=99, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Air Flow Monitor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=100, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='See Valve Quote', option='', per_unit=0.0, part_number='N/A', unit_cost=0.0,
                source_row=101, contributes_to_points=True, controller_points_each=0.0,
            ),
        ),
    ),
    'Water Source Heat Pumps': LegacySystemRule(
        name='Water Source Heat Pumps',
        points_per_unit=0.0, electrical_rate_per_point=1500.0,
        technician_hours_per_point=3.0,
        graphics_hours_per_unit=1.0, programming_hours_per_unit=1.0,
        points_from_materials=True,
        materials=(
            LegacyMaterialRule(
                item='Controller', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=107, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='Panel - Enclosure w Subpanel', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=108, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Relay', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=109, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Transformer', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=110, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Static Pressure Tips', option='', per_unit=0.0, part_number='N/A', unit_cost=0.0,
                source_row=111, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Current Sw', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=112, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Filter Status', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=113, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Communicating Room Thermostat', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=114, contributes_to_points=True, controller_points_each=50.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=115, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=116, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Water Detection', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=117, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='See Valve Quote', option='', per_unit=0.0, part_number='N/A', unit_cost=0.0,
                source_row=118, contributes_to_points=True, controller_points_each=0.0,
            ),
        ),
    ),
    'Fan Coil Units': LegacySystemRule(
        name='Fan Coil Units',
        points_per_unit=0.0, electrical_rate_per_point=1500.0,
        technician_hours_per_point=3.0,
        graphics_hours_per_unit=1.0, programming_hours_per_unit=1.0,
        points_from_materials=True,
        materials=(
            LegacyMaterialRule(
                item='Controller', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=123, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='Panel - Enclosure w Subpanel', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=124, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Relay', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=125, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Transformer', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=126, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Static Pressure Tips', option='', per_unit=0.0, part_number='N/A', unit_cost=0.0,
                source_row=127, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Current Sw', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=128, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Filter Status', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=129, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Communicating Room Thermostat', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=130, contributes_to_points=True, controller_points_each=50.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=131, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=132, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Water Detection', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=133, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='See Valve Quote', option='', per_unit=0.0, part_number='N/A', unit_cost=0.0,
                source_row=134, contributes_to_points=True, controller_points_each=0.0,
            ),
        ),
    ),
    'Unit Ventilators': LegacySystemRule(
        name='Unit Ventilators',
        points_per_unit=0.0, electrical_rate_per_point=1500.0,
        technician_hours_per_point=3.0,
        graphics_hours_per_unit=1.0, programming_hours_per_unit=1.0,
        points_from_materials=True,
        materials=(
            LegacyMaterialRule(
                item='Controller', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=139, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='Panel - Enclosure w Subpanel', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=140, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Relay', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=141, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Transformer', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=142, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Static Pressure Tips', option='', per_unit=0.0, part_number='N/A', unit_cost=0.0,
                source_row=143, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Current Sw', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=144, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Filter Status', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=145, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Communicating Room Thermostat', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=146, contributes_to_points=True, controller_points_each=50.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=147, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=148, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Water Detection', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=149, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Damper Actuator', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=150, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='See Valve Quote', option='', per_unit=0.0, part_number='N/A', unit_cost=0.0,
                source_row=151, contributes_to_points=True, controller_points_each=0.0,
            ),
        ),
    ),
    'Rooftop Units': LegacySystemRule(
        name='Rooftop Units',
        points_per_unit=0.0, electrical_rate_per_point=350.0,
        technician_hours_per_point=1.0,
        graphics_hours_per_unit=2.0, programming_hours_per_unit=6.0,
        points_from_materials=True,
        materials=(
            LegacyMaterialRule(
                item='Controller', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=156, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='Optimizer License with 18 Month SMA', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=157, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='I/O Module', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=158, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Phoenix Controller Core License', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=159, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Phoenix ILC SMA', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=160, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Panel - Enclosure w Subpanel', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=161, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Relay', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=162, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Transformer', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=163, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Power Supply', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=164, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Static Pressure Tips', option='', per_unit=0.0, part_number='N/A', unit_cost=0.0,
                source_row=165, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Thermostat', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=166, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Filter Status', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=167, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Press Transmitter', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=168, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Press Transmitter', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=169, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Current Sw', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=170, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Damper Actuator', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=171, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=172, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=173, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Humidity', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=174, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Humidity', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=175, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Emergency Stop Switch', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=176, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Air Flow Monitor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=177, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='See Valve Quote', option='', per_unit=0.0, part_number='N/A', unit_cost=0.0,
                source_row=178, contributes_to_points=True, controller_points_each=0.0,
            ),
        ),
    ),
    'Outdoor Air Units': LegacySystemRule(
        name='Outdoor Air Units',
        points_per_unit=0.0, electrical_rate_per_point=450.0,
        technician_hours_per_point=8.0,
        graphics_hours_per_unit=4.0, programming_hours_per_unit=4.0,
        points_from_materials=True,
        materials=(
            LegacyMaterialRule(
                item='Controller', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=184, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='Optimizer License with 18 Month SMA', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=185, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='I/O Module', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=186, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Phoenix Controller Core License', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=187, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Phoenix ILC SMA', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=188, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Panel - Enclosure w Subpanel', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=189, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Relay', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=190, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Transformer', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=191, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Power Supply', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=192, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Static Pressure Tips', option='', per_unit=0.0, part_number='N/A', unit_cost=0.0,
                source_row=193, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Thermostat', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=194, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Filter Status', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=195, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Press Transmitter', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=196, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Press Transmitter', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=197, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Current Sw', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=198, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Damper Actuator', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=199, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=200, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=201, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Humidity', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=202, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Emergency Stop Switch', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=203, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Air Flow Monitor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=204, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='See Valve Quote', option='', per_unit=0.0, part_number='N/A', unit_cost=0.0,
                source_row=205, contributes_to_points=True, controller_points_each=0.0,
            ),
        ),
    ),
    'Chiller': LegacySystemRule(
        name='Chiller',
        points_per_unit=0.0, electrical_rate_per_point=750.0,
        technician_hours_per_point=1.0,
        graphics_hours_per_unit=24.0, programming_hours_per_unit=24.0,
        points_from_materials=True,
        materials=(
            LegacyMaterialRule(
                item='Controller', option='Optimizer Plant Cntr, 1 IP, 3 Ethernet Switched+4 RS485 Ports', per_unit=0.0, part_number='N-ADV-134-H-C', unit_cost=875.1457,
                source_row=212, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='Optimizer License with 18 Month SMA', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=213, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='I/O Module', option='Optimizer Unitary Cntr 5-UI, 5-DI, 4-AO, 4-DO I/O Module', per_unit=0.0, part_number='ISMA-B-MIX18', unit_cost=338.81,
                source_row=214, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Phoenix Controller Core License', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=215, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Phoenix ILC SMA', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=216, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Panel - Enclosure w Subpanel', option='Nema-1 Medium', per_unit=0.0, part_number='RET1-262007BT-P', unit_cost=436.83,
                source_row=217, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Relay', option='24VAC DPDT with Base', per_unit=0.0, part_number='RH2B-UAC24 + SH2B-05', unit_cost=8.120000000000001,
                source_row=218, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Transformer', option='75 VA with circuit breaker', per_unit=0.0, part_number='TR75VA004', unit_cost=42.14,
                source_row=219, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Power Supply', option='24VDC Panel Mounted - 1.3 A', per_unit=0.0, part_number='PS5R-VB24', unit_cost=50.96,
                source_row=220, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='Well - Stainless Steel for HW', per_unit=0.0, part_number='50001774-001', unit_cost=34.349149999999995,
                source_row=221, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='Immersion for HW', per_unit=0.0, part_number='C7041D2001', unit_cost=23.18855,
                source_row=222, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Press Transmitter', option="0-100 PSI with 2 Remote Sensors w 10' cables", per_unit=0.0, part_number='PWRLX04S010', unit_cost=592.31,
                source_row=223, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Press Transmitter', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=224, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Emergency Stop Switch', option='Surface Mtd', per_unit=0.0, part_number='AOW401R + E-1PBG', unit_cost=179.36,
                source_row=225, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Current Sw', option='Digital Status Switch', per_unit=0.0, part_number='H600', unit_cost=31.43,
                source_row=226, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Current Sw', option='Digital for VFD Status', per_unit=0.0, part_number='H904', unit_cost=88.31,
                source_row=227, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Flow Sensor', option='Onicon Electromagnetic - BACnet - 3" to 72"  w Display', per_unit=0.0, part_number='FT-3500', unit_cost=3790.5600000000004,
                source_row=228, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Flow Sensor', option='Onicon Mounting Hardware - 4" and Up Steel', per_unit=0.0, part_number='0', unit_cost=483.36,
                source_row=229, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='BTU Meter', option='', per_unit=0.0, part_number='System 10 + F3500 Flow Meter', unit_cost=4992.0,
                source_row=230, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Alarm Indication Panel', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=231, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Refrigerant Monitor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=232, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='See Valve Quote', option='', per_unit=0.0, part_number='N/A', unit_cost=0.0,
                source_row=233, contributes_to_points=True, controller_points_each=0.0,
            ),
        ),
    ),
    'Chiller Room Emergency Control Panel': LegacySystemRule(
        name='Chiller Room Emergency Control Panel',
        points_per_unit=0.0, electrical_rate_per_point=1200.0,
        technician_hours_per_point=1.0,
        graphics_hours_per_unit=1.0, programming_hours_per_unit=0.0,
        points_from_materials=True,
        materials=(
            LegacyMaterialRule(
                item='Panel - Enclosure w Subpanel', option='Nema-1 Medium', per_unit=0.0, part_number='RET1-262007BT-P', unit_cost=436.83,
                source_row=239, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Relay', option='24VAC DPDT with Base', per_unit=0.0, part_number='RH2B-UAC24 + SH2B-05', unit_cost=8.120000000000001,
                source_row=240, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Transformer', option='75 VA with circuit breaker', per_unit=0.0, part_number='TR75VA004', unit_cost=42.14,
                source_row=241, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Power Supply', option='24VDC Panel Mounted - 1.3 A', per_unit=0.0, part_number='PS5R-VB24', unit_cost=50.96,
                source_row=242, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Horn/Strobe', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=243, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Push button', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=244, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Push button', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=245, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Switch', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=246, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Current Sw', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=247, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Switch', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=248, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Pilot Light', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=249, contributes_to_points=False, controller_points_each=0.0,
            ),
        ),
    ),
    'Boiler System': LegacySystemRule(
        name='Boiler System',
        points_per_unit=0.0, electrical_rate_per_point=750.0,
        technician_hours_per_point=1.0,
        graphics_hours_per_unit=24.0, programming_hours_per_unit=24.0,
        points_from_materials=True,
        materials=(
            LegacyMaterialRule(
                item='Controller', option='Optimizer Plant Cntr, 1 IP, 3 Ethernet Switched+4 RS485 Ports', per_unit=0.0, part_number='N-ADV-134-H-C', unit_cost=875.1457,
                source_row=255, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='Optimizer License with 18 Month SMA', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=256, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='I/O Module', option='Optimizer Unitary Cntr 5-UI, 5-DI, 4-AO, 4-DO I/O Module', per_unit=0.0, part_number='ISMA-B-MIX18', unit_cost=338.81,
                source_row=257, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Phoenix Controller Core License', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=258, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Phoenix ILC SMA', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=259, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Panel - Enclosure w Subpanel', option='Nema-1 Medium', per_unit=0.0, part_number='RET1-262007BT-P', unit_cost=436.83,
                source_row=260, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Relay', option='24VAC DPDT with Base', per_unit=0.0, part_number='RH2B-UAC24 + SH2B-05', unit_cost=8.120000000000001,
                source_row=261, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Transformer', option='75 VA with circuit breaker', per_unit=0.0, part_number='TR75VA004', unit_cost=42.14,
                source_row=262, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Power Supply', option='24VDC Panel Mounted - 1.3 A', per_unit=0.0, part_number='PS5R-VB24', unit_cost=50.96,
                source_row=263, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='Well - Stainless Steel for HW', per_unit=0.0, part_number='50001774-001', unit_cost=34.349149999999995,
                source_row=264, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='Immersion for HW', per_unit=0.0, part_number='C7041D2001', unit_cost=23.18855,
                source_row=265, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Press Transmitter', option="0-100 PSI with 2 Remote Sensors w 10' cables", per_unit=0.0, part_number='PWRLX04S010', unit_cost=592.31,
                source_row=266, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Press Transmitter', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=267, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Emergency Stop Switch', option='Surface Mtd', per_unit=0.0, part_number='AOW401R + E-1PBG', unit_cost=179.36,
                source_row=268, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Current Sw', option='Digital Status Switch', per_unit=0.0, part_number='H600', unit_cost=31.43,
                source_row=269, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Current Sw', option='Digital for VFD Status', per_unit=0.0, part_number='H904', unit_cost=88.31,
                source_row=270, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Flow Sensor', option='Onicon Electromagnetic - BACnet - 3" to 72"  w Display', per_unit=0.0, part_number='FT-3500', unit_cost=3790.5600000000004,
                source_row=271, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Flow Sensor', option='Onicon Mounting Hardware - 4" and Up Steel', per_unit=0.0, part_number='0', unit_cost=483.36,
                source_row=272, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='BTU Meter', option='', per_unit=0.0, part_number='System 10 + F3500 Flow Meter', unit_cost=4992.0,
                source_row=273, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Alarm Indication Panel', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=274, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='See Valve Quote', option='', per_unit=0.0, part_number='N/A', unit_cost=0.0,
                source_row=275, contributes_to_points=True, controller_points_each=0.0,
            ),
        ),
    ),
    'Exhaust Fans': LegacySystemRule(
        name='Exhaust Fans',
        points_per_unit=0.0, electrical_rate_per_point=550.0,
        technician_hours_per_point=1.0,
        graphics_hours_per_unit=0.1, programming_hours_per_unit=0.1,
        points_from_materials=True,
        materials=(
            LegacyMaterialRule(
                item='Controller', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=282, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='Optimizer License with 18 Month SMA', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=283, contributes_to_points=False, controller_points_each=70.0,
            ),
            LegacyMaterialRule(
                item='I/O Module', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=284, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Panel - Enclosure w Subpanel', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=285, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Relay', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=286, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Transformer', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=287, contributes_to_points=False, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Thermostat', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=288, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Current Sw', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=289, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Temp Sensor', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=290, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='CO, NO2 and O2 Sensors', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=291, contributes_to_points=True, controller_points_each=50.0,
            ),
            LegacyMaterialRule(
                item='Damper Actuator', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=292, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Pneumatic', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=293, contributes_to_points=True, controller_points_each=0.0,
            ),
            LegacyMaterialRule(
                item='Timed Override', option='', per_unit=0.0, part_number='Select Option', unit_cost=0.0,
                source_row=294, contributes_to_points=True, controller_points_each=0.0,
            ),
        ),
    ),
}
