import pytest
import os
from pathlib import Path
import sys

def test_default_config():
    """Test default configuration values."""
    from venue_playlists_api import create_app
    app = create_app()
    assert 'VENUE_DATA_DIR' in app.config
    assert Path(app.config['VENUE_DATA_DIR']).exists()

def test_env_override(monkeypatch):
    """Test environment variable override of configuration."""
    test_path = "/tmp/test/data"
    monkeypatch.setenv('VENUE_PLAYLISTS_ROOT', '/tmp/test')
    monkeypatch.setenv('VENUE_DATA_DIR', test_path)
    
    from venue_playlists_api import create_app
    app = create_app()
    assert app.config['VENUE_DATA_DIR'] == test_path

def test_project_root_detection(monkeypatch):
    """Test project root detection with required directories."""
    # Create a temporary project structure
    tmp_dir = Path("/tmp/test_project")
    for d in ['api', 'website', 'data']:
        (tmp_dir / d).mkdir(parents=True, exist_ok=True)
    
    monkeypatch.setenv('VENUE_PLAYLISTS_ROOT', str(tmp_dir))
    from venue_playlists_api.config import find_project_root
    root = find_project_root()
    assert root == str(tmp_dir)

    # Clean up
    for d in ['api', 'website', 'data']:
        (tmp_dir / d).rmdir()
    tmp_dir.rmdir() 