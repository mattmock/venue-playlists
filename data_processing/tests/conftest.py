"""Test configuration and fixtures."""
import pytest
from pathlib import Path
import shutil
import yaml

@pytest.fixture
def test_data_dir():
    """Fixture for test data directory."""
    return Path(__file__).parent / "data"

@pytest.fixture
def test_venue_config(test_data_dir):
    """Fixture for test venue configuration."""
    config_file = test_data_dir / "venue-data/sf/venues.yaml"
    with open(config_file) as f:
        return yaml.safe_load(f)["venues"]

@pytest.fixture
def test_output_dir(tmp_path):
    """Fixture for test output directory."""
    return tmp_path / "venue-data/sf"

@pytest.fixture
def test_month():
    """Fixture for test month."""
    return "December_2023" 