import pandas as pd

from estimator.catalog_manager import CatalogManager
from estimator.company_standards import CompanyStandards


def _parts():
    return pd.DataFrame([
        {"category": "Controller", "item": "Controller", "option": "Optimzer VAV", "supplier": "Honeywell", "part_number": "VAA-VA75MB24NMC", "price": 100, "multiplier": 1.1},
        {"category": "Controller", "item": "Controller", "option": "Legacy FX", "supplier": "Johnson Controls", "part_number": "FX-PCV", "price": 80, "multiplier": 1},
        {"category": "Controller", "item": "Controller", "option": "F4 VAV", "supplier": "Johnson Controls", "part_number": "F4-CVM3050-0", "price": 90, "multiplier": 1},
        {"category": "Controller", "item": "Controller", "option": "Siemens Controller", "supplier": "Siemens", "part_number": "ABC", "price": 70, "multiplier": 1},
        {"category": "Current Sw", "item": "Current Sw", "option": "Current Switch", "supplier": "Honeywell", "part_number": "H600", "price": 20, "multiplier": 1},
        {"category": "Relay", "item": "Relay", "option": "Relay", "supplier": "Functional Devices", "part_number": "RIBU1C", "price": 10, "multiplier": 1},
    ])


def test_catalog_manager_normalizes_optimizer_and_filters_lifecycle():
    catalog = CatalogManager(_parts())
    honeywell = catalog.controllers("Honeywell")
    assert honeywell.iloc[0]["option"] == "Optimizer VAV"
    jci = catalog.controllers("Johnson Controls")
    assert jci["part_number"].tolist() == ["F4-CVM3050-0"]
    jci_legacy = catalog.controllers("Johnson Controls", include_legacy=True)
    assert set(jci_legacy["part_number"]) == {"F4-CVM3050-0", "FX-PCV"}
    assert "ABC" not in catalog.controllers(include_legacy=True)["part_number"].tolist()


def test_catalog_manager_accessory_queries():
    catalog = CatalogManager(_parts())
    assert catalog.current_switches().iloc[0]["part_number"] == "H600"
    assert catalog.relays().iloc[0]["part_number"] == "RIBU1C"


def test_company_standards_controller_defaults():
    standards = CompanyStandards()
    assert standards.default_controller("VAV", "Honeywell") == "VAA-VA75MB24NMC"
    assert standards.default_controller("Fan Coil", "Honeywell") == "UN-RS0844MS24NMC"
    assert standards.default_controller("AHU", "Honeywell") == "UN-RL1644MS24NMC"
    assert standards.default_controller("VAV", "Johnson Controls") == "F4-CVM3050-0"
