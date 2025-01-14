"""Tests for playlist generation functionality.

This module provides a comprehensive test suite for the playlist generation pipeline:

Core Test Areas:
1. Spotify Authentication: Tests client initialization and auth
2. Artist Search: Tests track search and retrieval
3. Playlist Creation: Tests playlist generation and metadata

Key Components Tested:
- Spotify client initialization and authentication
- Artist track search functionality
- Playlist creation and configuration
- Track metadata handling

The tests use fixtures from conftest.py for:
- Mock Spotify client configuration
- Test data directory management
- Temporary output directory handling
"""
from playlist_data import (
    PlaylistGenerator,
    save_playlist_info
)
import pytest
import logging
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)

@pytest.fixture
def generator():
    """Fixture for playlist generator."""
    try:
        generator = PlaylistGenerator()
        assert generator.sp, "Spotify client not initialized"
        return generator
    except Exception as e:
        logger.error(f"Failed to initialize playlist generator: {e}")
        raise

def test_spotify_client(generator):
    """Test Spotify client initialization."""
    assert generator.sp is not None, "Spotify client should be initialized"
    assert hasattr(generator.sp, 'search'), "Spotify client missing search method"
    assert hasattr(generator.sp, 'playlist'), "Spotify client missing playlist method"
    
    logger.info("✓ Spotify client initialized and validated")

def test_artist_search(generator):
    """Test artist track search functionality."""
    test_artist = "The Beatles"
    tracks = generator.search_artist_top_tracks(test_artist)
    
    # Validate track data
    assert tracks, f"No tracks found for {test_artist}"
    assert len(tracks) > 0, "Should return at least one track"
    
    # Test track structure (updated for URI format)
    track = tracks[0]
    assert track.startswith("spotify:track:"), "Invalid track URI format"
    
    logger.info(f"✓ Found {len(tracks)} tracks for {test_artist}")

def test_playlist_creation(generator, test_output_dir):
    """Test playlist creation and configuration."""
    # Setup test data
    test_tracks = generator.search_artist_top_tracks("The Beatles")
    venue_name = "Test Venue"
    month = "December_2023"
    
    # Create playlist
    playlist_url = generator.create_venue_playlist(
        venue_name,
        month,
        test_tracks
    )
    
    # Validate playlist creation
    assert playlist_url, "Failed to create playlist"
    assert playlist_url.startswith("https://"), "Invalid playlist URL format"
    
    # Test playlist info saving
    if test_output_dir:
        # Call save_playlist_info
        save_playlist_info(venue_name, month, playlist_url, test_output_dir)
        
        # Check that file exists
        expected_file = Path(test_output_dir) / venue_name / f"playlist_{month}.yaml"
        assert expected_file.exists(), "Playlist info file not created"
        assert expected_file.stat().st_size > 0, "Playlist info file is empty"
        
        # Validate file contents
        with open(expected_file) as f:
            data = yaml.safe_load(f)
            assert data['venue'] == venue_name
            assert data['month'] == month
            assert data['playlist_url'] == playlist_url
    
    logger.info(f"✓ Created and validated playlist: {playlist_url}")

def run_playlist_tests():
    """Run all playlist tests."""
    pytest.main([__file__, "-v"])