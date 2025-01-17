import pytest
from pathlib import Path
from api.venues import bp, load_venues
from api import create_app

@pytest.fixture
def test_data_dir():
    """Test data directory."""
    return Path(__file__).parent / "data"

@pytest.fixture
def app(test_data_dir):
    """Create application for the tests."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "VENUE_DATA_DIR": str(test_data_dir / "venue-data")
    })
    yield app

@pytest.fixture
def client(app):
    """Test client for our Flask app."""
    return app.test_client()

def test_load_venues(test_data_dir):
    """Test venue data loading."""
    data = load_venues(test_data_dir / "venue-data")
    assert "venues" in data
    assert "the-independent" in data["venues"]

def test_get_venues(client):
    """Test venues endpoint returns correct structure."""
    response = client.get('/venues')
    assert response.status_code == 200
    
    data = response.get_json()
    assert "venues" in data
    
    venues = data["venues"]
    assert isinstance(venues, dict)
    
    # Test a known venue
    assert "the-independent" in venues
    venue = venues["the-independent"]
    assert "name" in venue
    assert "description" in venue
    assert "months" in venue