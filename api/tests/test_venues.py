import pytest
from pathlib import Path
from api.venues import bp, load_venues
from api import create_app
import yaml
from datetime import datetime

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

@pytest.fixture
def sample_playlist(test_data_dir):
    """Create a sample playlist file."""
    venue_dir = test_data_dir / "venue-data/sf/the-independent"
    venue_dir.mkdir(parents=True, exist_ok=True)
    
    current_month = datetime.now().strftime("%B_%Y")
    playlist_file = venue_dir / f"playlist_{current_month}.yaml"
    
    playlist_data = {
        "playlist_url": "https://open.spotify.com/playlist/123"
    }
    
    with open(playlist_file, "w") as f:
        yaml.dump(playlist_data, f)
    
    yield playlist_file
    playlist_file.unlink(missing_ok=True)

@pytest.fixture
def test_playlist(test_data_dir):
    """Create a test playlist file that should be filtered out."""
    venue_dir = test_data_dir / "venue-data/sf/the-independent"
    venue_dir.mkdir(parents=True, exist_ok=True)
    
    next_month = (datetime.now().month % 12) + 1
    next_month_date = datetime.now().replace(month=next_month)
    next_month_str = next_month_date.strftime("%B_%Y")
    
    playlist_file = venue_dir / f"playlist_{next_month_str}.yaml"
    
    playlist_data = {
        "playlist_url": "https://open.spotify.com/playlist/[TEST]456"
    }
    
    with open(playlist_file, "w") as f:
        yaml.dump(playlist_data, f)
    
    yield playlist_file
    playlist_file.unlink(missing_ok=True)

def test_load_venues(test_data_dir):
    """Test venue data loading."""
    data = load_venues(test_data_dir / "venue-data")
    assert "venues" in data
    assert "the-independent" in data["venues"]
    assert "last_updated" in data

def test_get_venues(client, sample_playlist, test_playlist):
    """Test venues endpoint returns correct structure."""
    response = client.get('/venues')
    assert response.status_code == 200
    
    # Test CORS headers
    assert 'Access-Control-Allow-Origin' in response.headers
    cors_origin = response.headers['Access-Control-Allow-Origin']
    assert any(origin in cors_origin for origin in ['http://localhost:8000', 'http://127.0.0.1:8000'])
    
    data = response.get_json()
    assert "venues" in data
    assert "last_updated" in data
    
    venues = data["venues"]
    assert isinstance(venues, dict)
    
    # Test a known venue
    assert "the-independent" in venues
    venue = venues["the-independent"]
    assert "name" in venue
    assert "description" in venue
    assert "months" in venue
    
    # Verify playlist data
    current_month = datetime.now().strftime("%B_%Y")
    assert current_month in venue["months"]
    assert "playlist_url" in venue["months"][current_month]
    assert "[TEST]" not in venue["months"][current_month]["playlist_url"]
    
    # Verify test playlist is filtered out
    next_month = (datetime.now().month % 12) + 1
    next_month_date = datetime.now().replace(month=next_month)
    next_month_str = next_month_date.strftime("%B_%Y")
    assert next_month_str not in venue["months"]

def test_venues_error_handling(app, client):
    """Test error handling for venues endpoint."""
    # Test with invalid data directory
    app.config["VENUE_DATA_DIR"] = "/nonexistent/path"
    response = client.get('/venues')
    assert response.status_code == 503
    data = response.get_json()
    assert "error" in data
    
    # Test with corrupted venue data
    app.config["VENUE_DATA_DIR"] = str(Path(__file__).parent / "data" / "venue-data")
    venue_file = Path(app.config["VENUE_DATA_DIR"]) / "sf" / "venues.yaml"
    venue_file.parent.mkdir(parents=True, exist_ok=True)
    with open(venue_file, "w") as f:
        f.write("invalid: yaml: content")
    
    response = client.get('/venues')
    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data