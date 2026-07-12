import pandas as pd

from estimator.controller_catalog import (
    DEFAULT_CONTROLLERS,
    build_controller_catalog,
    controller_choices,
    default_part_for_equipment,
    normalize_manufacturer,
)


def sample_parts():
    return pd.DataFrame([
        {"category":"Controller","item":"Controller","option":"Optimzer VAV","supplier":"Honeywell","part_number":"VAA-VA75MB24NMC","price":100,"multiplier":1},
        {"category":"Controller","item":"Controller","option":"Optimizer Small","supplier":"Honeywell","part_number":"UN-RS0844MS24NMC","price":200,"multiplier":1},
        {"category":"Controller","item":"Controller","option":"Optimizer Large","supplier":"Honeywell","part_number":"UN-RL1644MS24NMC","price":300,"multiplier":1},
        {"category":"Controller","item":"Controller","option":"JCI old","supplier":"JCI","part_number":"FX-PCV","price":50,"multiplier":1},
        {"category":"Controller","item":"Controller","option":"JCI VAV","supplier":"JCI","part_number":"F4-CVM3050-0","price":60,"multiplier":1},
        {"category":"Controller","item":"Controller","option":"Siemens","supplier":"Siemens","part_number":"PXC","price":70,"multiplier":1},
    ])


def test_catalog_normalizes_optimizer_and_lifecycle():
    catalog = build_controller_catalog(sample_parts())
    assert not catalog["description"].str.contains("Optimzer").any()
    assert catalog.loc[catalog.part_number.eq("FX-PCV"), "catalog_status"].iloc[0] == "Legacy"
    assert catalog.loc[catalog.part_number.eq("PXC"), "catalog_status"].iloc[0] == "Removed"


def test_selectors_hide_fx_and_siemens_by_default():
    choices = controller_choices(sample_parts())
    assert "FX-PCV" not in set(choices.part_number)
    assert "PXC" not in set(choices.part_number)
    assert "F4-CVM3050-0" in set(choices.part_number)


def test_equipment_defaults():
    assert default_part_for_equipment("VAV Boxes with Heat") == DEFAULT_CONTROLLERS["VAV"]
    assert default_part_for_equipment("Fan Coil Units") == DEFAULT_CONTROLLERS["Fan Coil"]
    assert default_part_for_equipment("Water Source Heat Pumps") == DEFAULT_CONTROLLERS["Heat Pump"]
    assert default_part_for_equipment("Boiler Systems") == DEFAULT_CONTROLLERS["Boiler"]


def test_manufacturer_filtered_choices_and_jci_defaults():
    honeywell = controller_choices(sample_parts(), manufacturer="Honeywell")
    jci = controller_choices(sample_parts(), manufacturer="Johnson Controls")
    assert set(honeywell.part_number) == {"VAA-VA75MB24NMC", "UN-RS0844MS24NMC", "UN-RL1644MS24NMC"}
    assert set(jci.part_number) == {"F4-CVM3050-0"}
    assert default_part_for_equipment("VAV Boxes", "Johnson Controls") == "F4-CVM3050-0"
    assert default_part_for_equipment("Air Handling Units", "Johnson Controls") == "F4-CGM09090-0"


def test_phoenix_name_is_normalized():
    assert normalize_manufacturer("Broudy CRC/Phoenix Controls") == "Phoenix Controls"
