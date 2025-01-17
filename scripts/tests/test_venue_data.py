"""Tests for venue data processing and scraping functionality.

This module provides a comprehensive test suite for the venue data processing pipeline:

Core Test Areas:
1. Configuration Loading: Validates YAML config parsing and structure
2. Scraper Factory: Tests scraper creation and configuration
3. Venue Processing: Tests the end-to-end pipeline

Key Components Tested:
- Venue configuration loading and validation
- Scraper factory pattern implementation
- Event data processing and file output
- Mock scraper integration

The tests use fixtures from conftest.py for:
- Test data directory management
- Temporary output directory handling
- Mock venue configuration
- Mock scraper implementation
"""
from scripts.venue_data import (
    process_venue, 
    load_venue_config,
    save_artists_to_file
)
from scripts.venue_data.scraper_factory import ScraperFactory
from scripts.venue_data.models import ArtistEvent
import pytest
from pathlib import Path
import yaml
import json
from datetime import datetime
from scripts.venue_data.scrapers.bandisintown import BandsInTownScraper

@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary directory for test data."""
    return tmp_path / "test_data"

@pytest.fixture
def test_output_dir(tmp_path):
    """Create a temporary directory for test output."""
    return tmp_path / "output"

@pytest.fixture(autouse=True)
def cleanup():
    """Cleanup any files or state after each test."""
    yield  # This runs the test
    # After test finishes:
    try:
        # Clean up any screenshots
        screenshots = Path("logs/screenshots").glob("test-venue_*.png")
        for screenshot in screenshots:
            screenshot.unlink()
        
        # Clean up any logs
        test_logs = Path("logs").glob("test_*.log")
        for log in test_logs:
            log.unlink()
    except Exception as e:
        print(f"Cleanup error: {e}")

def test_venue_processing(test_data_dir, test_output_dir):
    """Test the complete venue processing pipeline."""
    # Setup test venue
    venue_key = "the-independent"
    venue_info = {
        "name": "The Independent",
        "scrapers": {
            "bandisintown": {
                "url": "https://www.bandsintown.com/v/10001466-the-independent",
                "priority": 1
            }
        }
    }
    
    # Process venue
    output_files = process_venue(venue_key, output_dir=str(test_output_dir))
    
    # Verify output
    assert output_files, "No output files generated"
    
    # Check each output file
    for file_path in output_files:
        path = Path(file_path)
        assert path.exists(), f"Output file {file_path} not found"
        
        # Load and verify YAML content
        with open(path) as f:
            data = yaml.safe_load(f)
            assert "venue" in data, "Missing venue field"
            assert "month" in data, "Missing month field"
            assert "artists" in data, "Missing artists field"
            assert isinstance(data["artists"], list), "Artists should be a list"
            
            # Verify no duplicates in artists list
            artists = data["artists"]
            assert len(artists) == len(set(artists)), "Found duplicate artists"

def test_load_venue_config():
    """Test loading venue configuration."""
    venues = load_venue_config()
    assert venues, "Venues config should not be empty"
    assert "the-independent" in venues, "Should find The Independent"
    assert "scrapers" in venues["the-independent"], "Venue should have scrapers config"

def test_deduplication(test_output_dir):
    """Test artist deduplication."""
    # Create test events with duplicates
    events = [
        ArtistEvent(name="Test Artist", date=datetime.now(), venue="Test Venue"),
        ArtistEvent(name="Test Artist", date=datetime.now(), venue="Test Venue"),
        ArtistEvent(name="Another Artist", date=datetime.now(), venue="Test Venue")
    ]
    
    # Process and verify
    output_file = save_artists_to_file("test-venue", events, "January_2025", str(test_output_dir))
    
    with open(output_file) as f:
        data = yaml.safe_load(f)
        assert len(data["artists"]) == 2, "Should have deduplicated artists"
        assert len(set(data["artists"])) == len(data["artists"]), "No duplicates should remain"

def test_invalid_venue():
    """Test handling of invalid venue key."""
    output_files = process_venue("non-existent-venue")
    assert not output_files, "Should return empty list for invalid venue"

def test_empty_events(test_output_dir):
    """Test handling of empty event list."""
    events = []
    output_file = save_artists_to_file("test-venue", events, "January_2025", str(test_output_dir))
    
    with open(output_file) as f:
        data = yaml.safe_load(f)
        assert isinstance(data["artists"], list), "Should have empty artists list"
        assert len(data["artists"]) == 0, "Artists list should be empty"
        assert data["venue"] == "test-venue", "Venue name should be preserved"
        assert data["month"] == "January_2025", "Month should be preserved"

def test_bandisintown_scraper(test_output_dir):
    """Test BandsInTown scraper specifically."""
    # Create scraper instance
    scraper = BandsInTownScraper()
    
    # Test venue info
    venue_info = {
        "name": "The Independent",
        "scrapers": {
            "bandisintown": {
                "url": "https://www.bandsintown.com/v/10001466-the-independent",
                "priority": 1
            }
        }
    }
    
    # Get events
    events = scraper.get_events("the-independent", venue_info)
    
    # Verify events
    assert events, "No events found"
    for event in events:
        assert isinstance(event, ArtistEvent), "Event should be ArtistEvent instance"
        assert event.name, "Event should have artist name"
        assert event.date, "Event should have date"
        assert event.venue == venue_info["name"], "Event should have venue name"
    
    # Cleanup
    scraper.cleanup()

def test_scraper_factory():
    """Test scraper factory functionality."""
    # Test getting BandsInTown scraper
    scraper = ScraperFactory.get_scraper("bandisintown")
    assert isinstance(scraper, BandsInTownScraper)
    
    # Test getting scraper for venue
    venue_info = {
        "scrapers": {
            "bandisintown": {"priority": 1},
            "website": {"priority": 2}
        }
    }
    scraper = ScraperFactory.get_scraper_for_venue(venue_info)
    assert isinstance(scraper, BandsInTownScraper)
    assert scraper.scraper_type == "bandisintown"