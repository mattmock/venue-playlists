"""Test package initialization.

This module provides test suite initialization and configuration.
Tests should be run using pytest directly:

    pytest scripts/tests/ -v                 # Run all tests
    pytest scripts/tests/test_venue_data.py  # Run specific test file
    pytest scripts/tests/test_venue_data.py::test_venue_processing -v # Run specific test
"""
import pytest

def run_all_tests():
    """Run all test suites using pytest."""
    pytest.main(['-v', 'scripts/tests/'])

def run_venue_tests():
    """Run venue-specific tests using pytest."""
    pytest.main(['-v', 'scripts/tests/test_venue_data.py'])

def run_playlist_tests():
    """Run playlist-specific tests using pytest."""
    pytest.main(['-v', 'scripts/tests/test_playlist_data.py'])

__all__ = [
    'run_all_tests',
    'run_venue_tests',
    'run_playlist_tests'
] 