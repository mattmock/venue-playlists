"""Root level test configuration."""
import pytest
import sys
from pathlib import Path

@pytest.fixture(autouse=True)
def setup_path():
    """Add project root to Python path."""
    root = Path(__file__).parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root)) 