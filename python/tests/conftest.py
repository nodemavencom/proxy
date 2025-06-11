"""
Pytest configuration and fixtures for NodeMaven SDK tests.
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nodemaven import NodeMavenClient
from nodemaven.utils import generate_session_id


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


@pytest.fixture
def sample_countries():
    """Sample countries response from API."""
    return {
        "count": 3,
        "next": None,
        "previous": None,
        "results": [
            {"name": "United States", "code": "us", "available": True},
            {"name": "United Kingdom", "code": "gb", "available": True},
            {"name": "Germany", "code": "de", "available": True}
        ]
    }


@pytest.fixture
def sample_regions():
    """Sample regions response from API."""
    return {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {"name": "New York", "code": "new_york", "country_code": "us"},
            {"name": "California", "code": "california", "country_code": "us"}
        ]
    }


@pytest.fixture
def sample_cities():
    """Sample cities response from API."""
    return {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {"name": "New York", "code": "new_york", "region_code": "new_york", "country_code": "us"},
            {"name": "Brooklyn", "code": "brooklyn", "region_code": "new_york", "country_code": "us"}
        ]
    }


@pytest.fixture
def sample_isps():
    """Sample ISPs response from API."""
    return {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {"name": "Verizon", "code": "verizon", "city_code": "new_york"},
            {"name": "Comcast", "code": "comcast", "city_code": "new_york"}
        ]
    }


@pytest.fixture
def proxy_examples_from_docs():
    """Examples from how-api-works.md for compliance testing."""
    return [
        {
            "description": "Mobile / IPv4 / Sticky / TTL / Filter",
            "expected": "aa101d91571b74-country-any-type-mobile-ipv4-true-sid-a49c071423294-ttl-24h-filter-medium",
            "params": {
                "country": "any",
                "type": "mobile",
                "ipv4": True,
                "session": "a49c071423294",
                "ttl": "24h",
                "filter": "medium"
            }
        },
        {
            "description": "Residential / US / Brooklyn / Rotating / No Filter",
            "expected": "aa101d91571b74-country-us-region-new_york-city-brooklyn",
            "params": {
                "country": "us",
                "region": "new_york",
                "city": "brooklyn"
            }
        },
        {
            "description": "Mobile / Russia / Sticky 60s / ISP / Filter",
            "expected": "aa101d91571b74-country-ru-region-moscow-city-moscow-isp-beeline_home-type-mobile-ipv4-true-sid-a49c071423294-ttl-1m-filter-medium",
            "params": {
                "country": "ru",
                "region": "moscow",
                "city": "moscow",
                "isp": "beeline_home",
                "type": "mobile",
                "ipv4": True,
                "session": "a49c071423294",
                "ttl": "1m",
                "filter": "medium"
            }
        }
    ]


@pytest.fixture
def mock_api_responses():
    """Mock API responses for testing."""
    return {
        "user_info": {
            "email": "test@example.com",
            "proxy_username": "test_user",
            "proxy_password": "test_pass",
            "data": 1000000000
        },
        "countries": {
            "results": [
                {"name": "United States", "code": "us"},
                {"name": "United Kingdom", "code": "gb"}
            ]
        },
        "error_401": {
            "detail": "Invalid API key"
        },
        "error_429": {
            "detail": "Rate limit exceeded"
        }
    }


@pytest.fixture(scope="session")
def skip_integration():
    """Skip integration tests if no API key is available."""
    return not os.getenv('NODEMAVEN_APIKEY')


@pytest.fixture
def ttl_test_cases():
    """Test cases for TTL functionality (currently missing)."""
    return [
        {"ttl": "60s", "expected_seconds": 60},
        {"ttl": "1m", "expected_seconds": 60},
        {"ttl": "5m", "expected_seconds": 300},
        {"ttl": "1h", "expected_seconds": 3600},
        {"ttl": "24h", "expected_seconds": 86400}
    ]


@pytest.fixture
def edge_case_inputs():
    """Edge case inputs for testing robustness."""
    return {
        "empty_strings": {"country": "", "region": "", "city": ""},
        "none_values": {"country": None, "region": None},
        "special_chars": {"city": "new-york_test", "region": "california@123"},
        "long_strings": {"country": "x" * 100, "session": "a" * 50},
        "invalid_formats": {"ttl": "invalid", "filter": "unknown"}
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
    config.addinivalue_line(
        "markers", "performance: mark test as performance/benchmark test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow-running"
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
        
        # Mark performance tests
        if "performance" in str(item.fspath) or "benchmark" in str(item.fspath):
            item.add_marker(pytest.mark.performance)


# Skip integration tests if no API key
def pytest_runtest_setup(item):
    """Skip integration tests if no API key is configured."""
    if "integration" in item.keywords and not os.getenv('NODEMAVEN_APIKEY'):
        pytest.skip("Integration tests require NODEMAVEN_APIKEY environment variable") 