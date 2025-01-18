import pytest
from pathlib import Path
from venue_playlists_api.venues import load_venues

@pytest.fixture
def test_paths(tmp_path):
    """Create a temporary test directory structure."""
    # Create basic structure
    venue_dir = tmp_path / "venue-data" / "sf"
    venue_dir.mkdir(parents=True)
    
    # Create test venue file
    venue_file = venue_dir / "venues.yaml"
    venue_file.write_text("""
venues:
  test-venue:
    name: Test Venue
    description: "Test venue"
    scrapers:
      bandisintown:
        url: "https://test.com"
        priority: 1
""")
    
    return tmp_path

def test_absolute_path(test_paths):
    """Test loading venues with absolute path."""
    data = load_venues(test_paths / "venue-data")
    assert "venues" in data
    assert "test-venue" in data["venues"]

def test_missing_directory():
    """Test handling of non-existent directory."""
    with pytest.raises(FileNotFoundError):
        load_venues("/nonexistent/path") 