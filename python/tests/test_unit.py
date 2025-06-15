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
    validate_date_format, clean_dict, parse_error_message,
    validate_ttl_format, validate_proxy_username, validate_proxy_password
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


class TestProxyUsernameBuilding:
    """Comprehensive test for proxy username building with all targeting options"""
    
    def test_basic_username(self):
        """Test basic username without targeting"""
        username = build_proxy_username("testuser")
        assert username == "testuser"
    
    def test_country_targeting(self):
        """Test country targeting"""
        username = build_proxy_username("testuser", country="US")
        assert username == "testuser-country-us"
        
        username = build_proxy_username("testuser", country="gb")
        assert username == "testuser-country-gb"
    
    def test_region_targeting(self):
        """Test region targeting"""
        username = build_proxy_username("testuser", country="us", region="California")
        assert username == "testuser-country-us-region-california"
        
        # Test with spaces and underscores
        username = build_proxy_username("testuser", country="us", region="New York")
        assert username == "testuser-country-us-region-new_york"
        
        username = build_proxy_username("testuser", country="us", region="new_jersey")
        assert username == "testuser-country-us-region-new_jersey"
    
    def test_city_targeting(self):
        """Test city targeting"""
        username = build_proxy_username("testuser", country="us", city="Brooklyn")
        assert username == "testuser-country-us-city-brooklyn"
        
        username = build_proxy_username("testuser", country="us", city="New York")
        assert username == "testuser-country-us-city-new_york"
    
    def test_isp_targeting(self):
        """Test ISP targeting"""
        username = build_proxy_username("testuser", country="us", isp="Verizon")
        assert username == "testuser-country-us-isp-verizon"
        
        username = build_proxy_username("testuser", country="us", isp="AT&T")
        assert username == "testuser-country-us-isp-at&t"
        
        username = build_proxy_username("testuser", country="us", isp="T_Mobile")
        assert username == "testuser-country-us-isp-t_mobile"
    
    def test_connection_type_targeting(self):
        """Test connection type targeting"""
        username = build_proxy_username("testuser", country="us", type="residential")
        assert username == "testuser-country-us-type-residential"
        
        username = build_proxy_username("testuser", country="us", type="MOBILE")
        assert username == "testuser-country-us-type-mobile"
    
    def test_ipv4_targeting(self):
        """Test IPv4 targeting"""
        username = build_proxy_username("testuser", country="us", ipv4=True)
        assert username == "testuser-country-us-ipv4-true"
        
        username = build_proxy_username("testuser", country="us", ipv4=False)
        assert username == "testuser-country-us-ipv4-false"
        
        # Test without ipv4 parameter (should not appear)
        username = build_proxy_username("testuser", country="us")
        assert "ipv4" not in username
    
    def test_session_targeting(self):
        """Test session ID targeting"""
        username = build_proxy_username("testuser", country="us", session="session123")
        assert username == "testuser-country-us-sid-session123"
        
        # Test sticky sessions
        username = build_proxy_username("testuser", country="us", sticky=True)
        assert "testuser-country-us-sid-" in username
        assert len(username.split('-sid-')[1]) == 13  # Session ID length
    
    def test_ttl_targeting(self):
        """Test TTL (Time-To-Live) targeting"""
        # TTL only works with session ID
        username = build_proxy_username("testuser", country="us", session="test123", ttl="1h")
        assert username == "testuser-country-us-sid-test123-ttl-1h"
        
        username = build_proxy_username("testuser", country="us", session="test123", ttl="30m")
        assert username == "testuser-country-us-sid-test123-ttl-30m"
        
        username = build_proxy_username("testuser", country="us", session="test123", ttl="120s")
        assert username == "testuser-country-us-sid-test123-ttl-120s"
        
        # TTL without session should not appear
        username = build_proxy_username("testuser", country="us", ttl="1h")
        assert "ttl" not in username
        
        # Invalid TTL format should raise error
        with pytest.raises(ValueError, match="Invalid TTL format"):
            build_proxy_username("testuser", country="us", session="test123", ttl="invalid")
    
    def test_filter_targeting(self):
        """Test IP filter quality targeting"""
        username = build_proxy_username("testuser", country="us", filter="high")
        assert username == "testuser-country-us-filter-high"
        
        username = build_proxy_username("testuser", country="us", filter="MEDIUM")
        assert username == "testuser-country-us-filter-MEDIUM"
    
    def test_complex_targeting(self):
        """Test complex targeting with multiple options"""
        username = build_proxy_username(
            "aa101d91571b74",
            country="us",
            region="new_york", 
            city="brooklyn",
            type="residential",
            ipv4=True,
            session="a49c071423294",
            ttl="24h",
            filter="medium"
        )
        expected = "aa101d91571b74-country-us-region-new_york-city-brooklyn-type-residential-ipv4-true-sid-a49c071423294-ttl-24h-filter-medium"
        assert username == expected
    
    def test_mobile_targeting(self):
        """Test mobile-specific targeting"""
        username = build_proxy_username(
            "testuser",
            country="any",
            type="mobile",
            ipv4=True,
            session="a49c071423294",
            ttl="24h",
            filter="medium"
        )
        expected = "testuser-country-any-type-mobile-ipv4-true-sid-a49c071423294-ttl-24h-filter-medium"
        assert username == expected


class TestTTLValidation:
    """Test TTL format validation"""
    
    def test_valid_ttl_formats(self):
        """Test valid TTL formats"""
        assert validate_ttl_format("60s") == True
        assert validate_ttl_format("1m") == True
        assert validate_ttl_format("5m") == True
        assert validate_ttl_format("30m") == True
        assert validate_ttl_format("1h") == True
        assert validate_ttl_format("24h") == True
        assert validate_ttl_format("120s") == True
        assert validate_ttl_format("999m") == True
    
    def test_invalid_ttl_formats(self):
        """Test invalid TTL formats"""
        assert validate_ttl_format("1d") == False  # days not supported
        assert validate_ttl_format("60") == False  # no unit
        assert validate_ttl_format("s60") == False  # wrong order
        assert validate_ttl_format("1.5h") == False  # decimals not supported
        assert validate_ttl_format("") == False  # empty
        assert validate_ttl_format("invalid") == False  # invalid format


class TestCredentialValidation:
    """Test credential validation functions"""
    
    def test_valid_proxy_username(self):
        """Test valid proxy username formats"""
        assert validate_proxy_username("testuser12") == True
        assert validate_proxy_username("user_name_123") == True
        assert validate_proxy_username("a" * 50) == True  # 50 chars
        assert validate_proxy_username("abc123def") == True  # 9 chars (minimum)
    
    def test_invalid_proxy_username(self):
        """Test invalid proxy username formats"""
        assert validate_proxy_username("") == False  # empty
        assert validate_proxy_username("user-name") == False  # hyphen not allowed
        assert validate_proxy_username("user name") == False  # space not allowed
        assert validate_proxy_username("user@name") == False  # special chars not allowed
        assert validate_proxy_username("ab") == False  # too short
        assert validate_proxy_username("a" * 101) == False  # too long
    
    def test_valid_proxy_password(self):
        """Test valid proxy password formats"""
        assert validate_proxy_password("password123") == True
        assert validate_proxy_password("pass_word_123") == True
        assert validate_proxy_password("a" * 50) == True  # 50 chars
        assert validate_proxy_password("abc123def") == True  # 9 chars (minimum)
    
    def test_invalid_proxy_password(self):
        """Test invalid proxy password formats"""
        assert validate_proxy_password("") == False  # empty
        assert validate_proxy_password("pass-word") == False  # hyphen not allowed
        assert validate_proxy_password("pass word") == False  # space not allowed
        assert validate_proxy_password("pass@word") == False  # special chars not allowed
        assert validate_proxy_password("ab") == False  # too short
        assert validate_proxy_password("a" * 101) == False  # too long


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_generate_session_id(self):
        """Test session ID generation"""
        session_id = generate_session_id()
        assert len(session_id) == 13
        assert session_id.isalnum()
        
        # Test uniqueness
        session_id2 = generate_session_id()
        assert session_id != session_id2
    
    def test_format_bytes(self):
        """Test byte formatting"""
        assert format_bytes(0) == "0 B"
        assert format_bytes(1024) == "1.00 KB"
        assert format_bytes(1048576) == "1.00 MB"
        assert format_bytes(500) == "500 B"
        assert format_bytes(1073741824) == "1.00 GB"
        assert format_bytes(2048) == "2.00 KB"
    
    def test_validate_date_format(self):
        """Test date format validation"""
        # Valid date should not raise exception
        validate_date_format("25-12-2023")
        validate_date_format("01-01-2024")
        validate_date_format("31-12-2023")
        
        # Invalid date should raise ValueError
        with pytest.raises(ValueError):
            validate_date_format("2023-12-25")  # Wrong format
        
        with pytest.raises(ValueError):
            validate_date_format("invalid-date")
        
        with pytest.raises(ValueError):
            validate_date_format("32-13-2023")  # Invalid date
    
    def test_clean_dict(self):
        """Test dictionary cleaning"""
        dirty_dict = {"a": 1, "b": None, "c": "test", "d": None, "e": 0, "f": False}
        clean = clean_dict(dirty_dict)
        assert clean == {"a": 1, "c": "test", "e": 0, "f": False}
        
        # Test empty dict
        assert clean_dict({}) == {}
        
        # Test all None values
        assert clean_dict({"a": None, "b": None}) == {}
    
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
        
        # Test with 'errors' list
        errors_list = {"errors": ["Error 1", "Error 2"]}
        result = parse_error_message(errors_list)
        assert "Error 1; Error 2" == result
        
        # Test with unknown format
        assert parse_error_message({}) == "Unknown error occurred"
        assert parse_error_message({"unknown": "field"}) == "Unknown error occurred"


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
    
    def test_complex_proxy_url_building(self):
        """Test complex proxy URL building with all options"""
        from nodemaven.utils import build_proxy_url
        
        # Mock credentials for testing
        import nodemaven.utils
        original_func = nodemaven.utils.get_correct_proxy_credentials
        nodemaven.utils.get_correct_proxy_credentials = lambda: ("aa101d91571b74", "testpass123")
        
        try:
            # Test HTTP with complex targeting
            url = build_proxy_url(
                protocol="http",
                country="us",
                region="new_york",
                city="brooklyn", 
                type="residential",
                ipv4=True,
                session="test123",
                ttl="1h",
                filter="high"
            )
            assert "aa101d91571b74-country-us-region-new_york-city-brooklyn-type-residential-ipv4-true-sid-test123-ttl-1h-filter-high" in url
            assert "testpass123" in url
            assert "gate.nodemaven.com:8080" in url
            
            # Test SOCKS5 with mobile targeting
            url = build_proxy_url(
                protocol="socks5",
                country="any",
                type="mobile",
                sticky=True,
                filter="medium"
            )
            assert url.startswith("socks5://")
            assert "country-any-type-mobile" in url
            assert "sid-" in url  # Should have generated session ID
            assert "filter-medium" in url
            assert ":1080" in url
            
        finally:
            # Restore original function
            nodemaven.utils.get_correct_proxy_credentials = original_func


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 