import pathlib

import pytest
from flake8.main import application as flake8_app

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]


@pytest.mark.lint
def test_flake8_conformance():
    app = flake8_app.Application()
    app.run([
        "--config",
        str(PROJECT_ROOT / ".flake8"),
        str(PROJECT_ROOT / "app"),
        str(PROJECT_ROOT / "tests"),
    ])
    assert app.result_count == 0, f"Found {app.result_count} flake8 violations"
