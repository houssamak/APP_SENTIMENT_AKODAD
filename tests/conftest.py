import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

# ClÃ©s factices de tests uniquement; aucune vraie clÃ© n'est versionnÃ©e.
os.environ.setdefault(
    "API_KEYS",
    "test-client-key-not-a-secret:client,test-admin-key-not-a-secret:admin",
)
os.environ.setdefault("API_KEY", "test-client-key-not-a-secret")


@pytest.fixture(scope="session")
def root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def cadrage_dir(root: Path) -> Path:
    return root / "docs" / "cadrage"
