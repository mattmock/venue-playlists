import pytest
from pathlib import Path
from venue_playlists_api.venues import load_venues

@pytest.fixture
def edge_case_dir(tmp_path):
    """Create a test directory with various edge cases."""
    # Basic structure
    venue_dir = tmp_path / "venue-data"
    venue_dir.mkdir()
    
    # Empty city directory
    (venue_dir / "empty_city").mkdir()
    
    # City with empty venues.yaml
    city_empty_yaml = venue_dir / "empty_yaml"
    city_empty_yaml.mkdir()
    (city_empty_yaml / "venues.yaml").write_text("")
    
    # City with malformed venue data
    city_malformed = venue_dir / "malformed"
    city_malformed.mkdir()
    (city_malformed / "venues.yaml").write_text("""
venues:
  broken-venue:
    # Missing required name field
    description: "Test venue"
    scrapers: not-a-dict
  valid-venue:
    name: "Valid Venue"
    description: "This one is fine"
    scrapers:
      bandisintown:
        url: "https://test.com"
        priority: 1
""")
    
    return venue_dir

def test_empty_directory(edge_case_dir):
    """Test handling of empty city directory."""
    data = load_venues(edge_case_dir)
    assert "venues" in data
    assert len(data["venues"]) == 1  # Only valid-venue should be loaded
    assert "last_updated" in data

def test_empty_yaml(edge_case_dir):
    """Test handling of empty venues.yaml file."""
    data = load_venues(edge_case_dir)
    assert "venues" in data
    assert len(data["venues"]) == 1  # Only valid-venue should be loaded

def test_malformed_venue_data(edge_case_dir):
    """Test handling of malformed venue data."""
    data = load_venues(edge_case_dir)
    assert "venues" in data
    # Should skip broken-venue but include valid-venue
    assert "broken-venue" not in data["venues"]
    assert "valid-venue" in data["venues"] 