from pathlib import Path

import pandas as pd

from estimator.health_check import all_checks_pass, run_health_checks


def _write_valid_repo(root: Path) -> None:
    (root / "data").mkdir()
    (root / "projects").mkdir()
    (root / "app.py").write_text("# app", encoding="utf-8")
    (root / "requirements.txt").write_text("streamlit\n", encoding="utf-8")
    pd.DataFrame([{
        "item": "Controller", "option": "Test", "supplier": "Honeywell",
        "part_number": "TEST", "price": 1, "multiplier": 1, "category": "Controller",
    }]).to_csv(root / "data" / "parts.csv", index=False)
    pd.DataFrame([{"county": "Test, NC", "tax_rate": 0.07}]).to_csv(
        root / "data" / "taxes.csv", index=False
    )


def test_health_check_reports_valid_repository(tmp_path: Path):
    _write_valid_repo(tmp_path)
    results = run_health_checks(tmp_path)
    assert all_checks_pass(results)
    assert {item.name for item in results} >= {
        "Application files", "Python packages", "Parts catalog", "Tax catalog", "Project storage"
    }


def test_health_check_reports_missing_files(tmp_path: Path):
    results = run_health_checks(tmp_path)
    file_check = next(item for item in results if item.name == "Application files")
    assert not file_check.ok
    assert "Missing" in file_check.message
