from pathlib import Path


def test_primary_tab_names_and_order():
    app_source = (Path(__file__).resolve().parents[1] / "app.py").read_text(encoding="utf-8")
    expected = '''st.tabs([\n    "Controls Estimate", "Totals Summary", "Labor", "Materials", "Assumptions",\n    "Company Standards", "Controller Library", "Sylk Device Library"\n])'''
    assert expected in app_source


def test_old_primary_tab_names_are_removed():
    app_source = (Path(__file__).resolve().parents[1] / "app.py").read_text(encoding="utf-8")
    assert '"Legacy Base Estimate"' not in app_source
    assert 'st.subheader("Estimate Summary")' not in app_source
