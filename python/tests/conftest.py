"""
Simple pytest configuration and fixtures for NodeMaven SDK tests.
"""

import pytest
import os
import sys
from unittest.mock import Mock

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nodemaven import NodeMavenClient


@pytest.fixture
def api_client():
    """Provide configured API client for tests."""
    return NodeMavenClient(api_key="test_api_key_for_testing")


@pytest.fixture
def mock_credentials():
    """Provide test credentials."""
    return ("test_user_123456789", "test_password_123456789")


@pytest.fixture
def sample_user_info():
    """Sample user info response from API."""
    return {
        "email": "test@example.com",
        "proxy_username": "test_user_123456789",
        "proxy_password": "test_password_123456789",
        "data": 1073741824,  # 1GB in bytes
        "data_used": 268435456,  # 256MB in bytes
        "plan": "Premium",
        "active": True
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test requiring API key"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test (no external dependencies)"
    )


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their location."""
    for item in items:
        # Mark integration tests
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Mark unit tests
        if "unit" in str(item.fspath) or "test_unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)


# Skip integration tests if no API key
def pytest_runtest_setup(item):
    """Skip integration tests if no API key is configured."""
    if "integration" in item.keywords and not os.getenv('NODEMAVEN_APIKEY'):
        pytest.skip("Integration tests require NODEMAVEN_APIKEY environment variable") 