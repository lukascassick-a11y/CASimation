from __future__ import annotations

import argparse
import importlib
import json
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class HealthCheckResult:
    name: str
    ok: bool
    message: str
    elapsed_ms: float = 0.0


REQUIRED_FILES = (
    "app.py",
    "requirements.txt",
    "data/parts.csv",
    "data/taxes.csv",
)

REQUIRED_PART_COLUMNS = {
    "item", "option", "supplier", "part_number", "price", "multiplier", "category"
}
REQUIRED_TAX_COLUMNS = {"county", "tax_rate"}
REQUIRED_IMPORTS = (
    "streamlit",
    "pandas",
    "openpyxl",
    "reportlab",
)


def _timed(name: str, check) -> HealthCheckResult:
    started = time.perf_counter()
    try:
        message = check()
        return HealthCheckResult(name, True, str(message), (time.perf_counter() - started) * 1000)
    except Exception as exc:  # startup diagnostics should report rather than crash
        return HealthCheckResult(name, False, str(exc), (time.perf_counter() - started) * 1000)


def _check_required_files(root: Path) -> str:
    missing = [item for item in REQUIRED_FILES if not (root / item).exists()]
    if missing:
        raise FileNotFoundError("Missing: " + ", ".join(missing))
    return "Required application files found"


def _check_imports() -> str:
    missing: list[str] = []
    for package in REQUIRED_IMPORTS:
        try:
            importlib.import_module(package)
        except Exception:
            missing.append(package)
    if missing:
        raise ImportError("Unavailable packages: " + ", ".join(missing))
    return "Required Python packages import successfully"


def _read_csv(path: Path, required_columns: set[str]) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = sorted(required_columns.difference(frame.columns))
    if missing:
        raise ValueError(f"{path.name} missing columns: {', '.join(missing)}")
    return frame


def _check_parts(root: Path) -> str:
    frame = _read_csv(root / "data" / "parts.csv", REQUIRED_PART_COLUMNS)
    return f"parts.csv loaded ({len(frame):,} rows)"


def _check_taxes(root: Path) -> str:
    frame = _read_csv(root / "data" / "taxes.csv", REQUIRED_TAX_COLUMNS)
    return f"taxes.csv loaded ({len(frame):,} rows)"


def _check_project_storage(root: Path) -> str:
    projects = root / "projects"
    projects.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix="casimation_", suffix=".tmp", dir=projects, delete=False) as handle:
        test_path = Path(handle.name)
        handle.write(b"health-check")
    test_path.unlink(missing_ok=True)
    return "projects folder is writable"


def _check_estimator_imports() -> str:
    importlib.import_module("estimator")
    importlib.import_module("estimator.data_repository")
    return "CASimation estimator package imports successfully"


def git_metadata(root: Path) -> dict[str, str]:
    def run(*args: str) -> str:
        try:
            completed = subprocess.run(
                ["git", "-C", str(root), *args],
                check=True,
                capture_output=True,
                text=True,
                timeout=3,
            )
            return completed.stdout.strip()
        except Exception:
            return "Unavailable"

    status = run("status", "--porcelain")
    return {
        "branch": run("branch", "--show-current"),
        "commit": run("rev-parse", "--short", "HEAD"),
        "working_tree": "Clean" if status == "" else "Modified",
    }


def run_health_checks(root: str | Path) -> list[HealthCheckResult]:
    root_path = Path(root).resolve()
    checks = (
        ("Application files", lambda: _check_required_files(root_path)),
        ("Python packages", _check_imports),
        ("Estimator package", _check_estimator_imports),
        ("Parts catalog", lambda: _check_parts(root_path)),
        ("Tax catalog", lambda: _check_taxes(root_path)),
        ("Project storage", lambda: _check_project_storage(root_path)),
    )
    return [_timed(name, check) for name, check in checks]


def all_checks_pass(results: Iterable[HealthCheckResult]) -> bool:
    return all(result.ok for result in results)


def format_console_report(root: Path, results: list[HealthCheckResult]) -> str:
    metadata = git_metadata(root)
    lines = [
        "CASimation startup health check",
        f"Root: {root}",
        f"Python: {sys.version.split()[0]}",
        f"Branch: {metadata['branch']}",
        f"Commit: {metadata['commit']}",
        f"Working tree: {metadata['working_tree']}",
        "",
    ]
    for result in results:
        marker = "PASS" if result.ok else "FAIL"
        lines.append(f"[{marker}] {result.name}: {result.message} ({result.elapsed_ms:.0f} ms)")
    lines.append("")
    lines.append("Health check passed." if all_checks_pass(results) else "Health check failed.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CASimation startup requirements.")
    parser.add_argument("--root", default=".", help="CASimation repository root")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a console report")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    results = run_health_checks(root)
    if args.json:
        print(json.dumps({"root": str(root), "results": [asdict(item) for item in results]}, indent=2))
    else:
        print(format_console_report(root, results))
    return 0 if all_checks_pass(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
