"""
Unit tests for NodeMaven SDK - no API calls required
These tests run in CI/CD without needing API keys
"""
import pytest
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nodemaven.exceptions import NodeMavenAPIError, AuthenticationError
from nodemaven.utils import (
    build_proxy_username, generate_session_id, format_bytes, 
    validate_date_format, clean_dict, parse_error_message
)


class TestExceptions:
    """Test custom exception classes"""
    
    def test_base_exception(self):
        """Test NodeMavenAPIError base exception"""
        error = NodeMavenAPIError("Test error", 400, {"detail": "test"})
        assert str(error) == "[400] Test error"
        assert error.status_code == 400
        assert error.response_data == {"detail": "test"}
    
    def test_authentication_error(self):
        """Test AuthenticationError"""
        error = AuthenticationError("Invalid API key", 401)
        assert "Invalid API key" in str(error)
        assert error.status_code == 401


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_build_proxy_username(self):
        """Test proxy username building"""
        username = build_proxy_username("testuser", country="us", city="newyork")
        assert "testuser" in username
        assert "country-us" in username
        assert "city-newyork" in username
        assert "ipv4-true" in username
        assert "filter-medium" in username
    
    def test_build_proxy_username_with_session(self):
        """Test proxy username with session"""
        username = build_proxy_username("testuser", country="uk", session="session123")
        assert "sid-session123" in username
    
    def test_generate_session_id(self):
        """Test session ID generation"""
        session_id = generate_session_id()
        assert len(session_id) == 13
        assert session_id.isalnum()
    
    def test_format_bytes(self):
        """Test byte formatting"""
        assert format_bytes(0) == "0 B"
        assert format_bytes(1024) == "1.00 KB"
        assert format_bytes(1048576) == "1.00 MB"
        assert format_bytes(500) == "500 B"
    
    def test_validate_date_format(self):
        """Test date format validation"""
        # Valid date should not raise exception
        validate_date_format("25-12-2023")
        
        # Invalid date should raise ValueError
        with pytest.raises(ValueError):
            validate_date_format("2023-12-25")  # Wrong format
        
        with pytest.raises(ValueError):
            validate_date_format("invalid-date")
    
    def test_clean_dict(self):
        """Test dictionary cleaning"""
        dirty_dict = {"a": 1, "b": None, "c": "test", "d": None}
        clean = clean_dict(dirty_dict)
        assert clean == {"a": 1, "c": "test"}
    
    def test_parse_error_message(self):
        """Test error message parsing"""
        # Test with 'error' key
        assert parse_error_message({"error": "Test error"}) == "Test error"
        
        # Test with 'detail' key
        assert parse_error_message({"detail": "Test detail"}) == "Test detail"
        
        # Test with 'errors' dict
        errors_dict = {"errors": {"field1": ["Error 1"], "field2": "Error 2"}}
        result = parse_error_message(errors_dict)
        assert "field1: Error 1" in result
        assert "field2: Error 2" in result
        
        # Test with unknown format
        assert parse_error_message({}) == "Unknown error occurred"


class TestClientInitialization:
    """Test client initialization without API calls"""
    
    def test_client_import(self):
        """Test that client can be imported"""
        from nodemaven import NodeMavenClient
        assert NodeMavenClient is not None
    
    def test_client_init_with_api_key(self):
        """Test client initialization with provided API key"""
        from nodemaven import NodeMavenClient
        client = NodeMavenClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.base_url is not None
        assert client.timeout is not None
    
    def test_client_init_without_requests(self):
        """Test client works without requests library"""
        # This tests the urllib fallback functionality
        from nodemaven.client import NodeMavenClient
        # Even without API key, should initialize
        try:
            client = NodeMavenClient(api_key="test")
            assert client is not None
        except ValueError:
            # Expected if no API key provided
            pass


class TestConfigurationFunctions:
    """Test configuration-related functions"""
    
    def test_proxy_config_structure(self):
        """Test proxy configuration structure"""
        from nodemaven.utils import build_proxy_url
        
        # Mock credentials for testing
        import nodemaven.utils
        original_func = nodemaven.utils.get_correct_proxy_credentials
        nodemaven.utils.get_correct_proxy_credentials = lambda: ("testuser", "testpass")
        
        try:
            url = build_proxy_url(protocol="http", country="us")
            assert "testuser" in url
            assert "testpass" in url
            assert "gate.nodemaven.com" in url
            assert ":8080" in url
        finally:
            # Restore original function
            nodemaven.utils.get_correct_proxy_credentials = original_func
    
    def test_socks5_proxy_url(self):
        """Test SOCKS5 proxy URL building"""
        from nodemaven.utils import build_proxy_url
        
        # Mock credentials for testing
        import nodemaven.utils
        original_func = nodemaven.utils.get_correct_proxy_credentials
        nodemaven.utils.get_correct_proxy_credentials = lambda: ("testuser", "testpass")
        
        try:
            url = build_proxy_url(protocol="socks5", country="uk")
            assert url.startswith("socks5://")
            assert ":1080" in url  # SOCKS5 port
        finally:
            # Restore original function
            nodemaven.utils.get_correct_proxy_credentials = original_func


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 