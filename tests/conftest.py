import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "integration: live API tests (UniProt, StrainInfo, NCBI) — "
        "require network access; deselect with '-m \"not integration\"'",
    )
