import pytest
from pathlib import Path
import yaml
import sys
from datetime import datetime

@pytest.fixture(autouse=True)
def clean_imports():
    """Clean up imports before each test."""
    # Remove any cached imports
    to_remove = [m for m in sys.modules if m.startswith('venue_playlists_api')]
    for m in to_remove:
        del sys.modules[m]

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