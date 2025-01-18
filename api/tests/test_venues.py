import pytest
from pathlib import Path
import yaml
from datetime import datetime
from venue_playlists_api.venues import load_venues

@pytest.fixture
def test_data_dir():
    """Create test data directory."""
    return Path(__file__).parent / "data"

@pytest.fixture
def app():
    """Create test app."""
    from venue_playlists_api import create_app
    app = create_app()
    app.config["VENUE_DATA_DIR"] = str(Path(__file__).parent / "data" / "venue-data")
    return app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def sample_playlist(test_data_dir):
    """Create sample playlist."""
    playlist_dir = test_data_dir / "venue-data" / "sf" / "the-independent"
    playlist_dir.mkdir(parents=True, exist_ok=True)
    playlist_file = playlist_dir / "playlist_January_2025.yaml"
    playlist_data = {
        "playlist_url": "https://open.spotify.com/playlist/sample_january_2025",
        "events": [
            {
                "name": "Sample Event 1",
                "date": "2025-01-15",
                "artist": "Test Artist 1"
            },
            {
                "name": "Sample Event 2",
                "date": "2025-01-20",
                "artist": "Test Artist 2"
            }
        ]
    }
    with open(playlist_file, "w") as f:
        yaml.dump(playlist_data, f)
    return playlist_file

@pytest.fixture
def test_playlist(test_data_dir):
    """Create test playlist."""
    playlist_dir = test_data_dir / "venue-data" / "sf" / "the-independent"
    playlist_dir.mkdir(parents=True, exist_ok=True)
    playlist_file = playlist_dir / "playlist_February_2025.yaml"
    playlist_data = {
        "playlist_url": "https://open.spotify.com/playlist/test_february_2025",
        "events": [
            {
                "name": "Test Event 1",
                "date": "2025-02-10",
                "artist": "Test Artist 3"
            },
            {
                "name": "Test Event 2",
                "date": "2025-02-25",
                "artist": "Test Artist 4"
            }
        ]
    }
    with open(playlist_file, "w") as f:
        yaml.dump(playlist_data, f)
    return playlist_file

def test_load_venues(test_data_dir):
    """Test venue data loading."""
    # Create test venue data
    venue_dir = test_data_dir / "venue-data" / "sf"
    venue_dir.mkdir(parents=True, exist_ok=True)
    venue_file = venue_dir / "venues.yaml"
    venue_data = {
        "venues": {
            "the-independent": {
                "name": "The Independent",
                "description": "A historic music venue in San Francisco",
                "scrapers": [
                    {
                        "type": "eventbrite",
                        "url": "https://www.eventbrite.com/o/the-independent-sf"
                    }
                ]
            }
        }
    }
    with open(venue_file, "w") as f:
        yaml.dump(venue_data, f)

    data = load_venues(test_data_dir / "venue-data")
    assert "venues" in data
    assert "the-independent" in data["venues"]
    assert data["venues"]["the-independent"]["name"] == "The Independent"

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
    assert venue["name"] == "The Independent"
    assert "months" in venue

def test_venues_error_handling(app, client):
    """Test error handling for venues endpoint."""
    # Test with invalid data directory
    app.config["VENUE_DATA_DIR"] = "/nonexistent/path"
    response = client.get('/venues')
    assert response.status_code == 503
    data = response.get_json()
    assert "error" in data

    # Test with corrupted venue data
    error_dir = Path(__file__).parent / "data" / "error-data"
    app.config["VENUE_DATA_DIR"] = str(error_dir)
    venue_file = error_dir / "sf" / "venues.yaml"
    venue_file.parent.mkdir(parents=True, exist_ok=True)
    with open(venue_file, "w") as f:
        f.write("invalid: yaml: content")

    response = client.get('/venues')
    assert response.status_code == 500