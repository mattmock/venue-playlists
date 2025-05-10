"""Tests for SpotifyArtistSearch functionality."""
import pytest
from unittest.mock import Mock, patch
from ..artist_search import SpotifyArtistSearch

@pytest.fixture
def mock_spotify_client():
    """Create a mock Spotify client for testing."""
    client = Mock()
    # Setup default responses
    client.search.return_value = {
        'artists': {
            'items': [{
                'id': 'test_id_1',
                'name': 'Test Artist'
            }]
        }
    }
    client.artist_top_tracks.return_value = {
        'tracks': [
            {'id': 'track_1'},
            {'id': 'track_2'}
        ]
    }
    return client

@pytest.fixture
def artist_search(mock_spotify_client):
    """Create SpotifyArtistSearch instance with mock client."""
    return SpotifyArtistSearch(mock_spotify_client, rate_limit=0)  # No rate limiting in tests

def test_search_single_artist_success(artist_search, mock_spotify_client):
    """Test successful single artist search."""
    artist_id = artist_search._search_single_artist("Test Artist")
    assert artist_id == 'test_id_1'
    mock_spotify_client.search.assert_called_once_with(
        q="Test Artist",
        type='artist',
        limit=1
    )

def test_search_single_artist_no_results(artist_search, mock_spotify_client):
    """Test artist search with no results."""
    mock_spotify_client.search.return_value = {'artists': {'items': []}}
    artist_id = artist_search._search_single_artist("Unknown Artist")
    assert artist_id is None

def test_search_single_artist_name_mismatch(artist_search, mock_spotify_client):
    """Test artist search with name mismatch."""
    mock_spotify_client.search.return_value = {
        'artists': {
            'items': [{
                'id': 'test_id_2',
                'name': 'Different Artist'
            }]
        }
    }
    artist_id = artist_search._search_single_artist("Test Artist")
    assert artist_id is None

def test_search_artists_batch(artist_search, mock_spotify_client):
    """Test searching multiple artists."""
    artists = ["Artist 1", "Artist 2"]
    mock_spotify_client.search.side_effect = [
        {'artists': {'items': [{'id': 'id1', 'name': 'Artist 1'}]}},
        {'artists': {'items': [{'id': 'id2', 'name': 'Artist 2'}]}}
    ]
    
    results = artist_search.search_artists(artists)
    assert results == {"Artist 1": "id1", "Artist 2": "id2"}
    assert mock_spotify_client.search.call_count == 2

def test_get_top_tracks_success(artist_search, mock_spotify_client):
    """Test successful top tracks retrieval."""
    artist_ids = ["id1", "id2"]
    results = artist_search.get_top_tracks(artist_ids)
    
    assert results == {
        "id1": ["track_1", "track_2"],
        "id2": ["track_1", "track_2"]
    }
    assert mock_spotify_client.artist_top_tracks.call_count == 2

def test_search_with_retries(artist_search, mock_spotify_client):
    """Test retry logic on API failure."""
    mock_spotify_client.search.side_effect = [
        Exception("API Error"),
        {'artists': {'items': [{'id': 'retry_id', 'name': 'Test Artist'}]}}
    ]
    
    artist_id = artist_search._search_single_artist("Test Artist")
    assert artist_id == 'retry_id'
    assert mock_spotify_client.search.call_count == 2 