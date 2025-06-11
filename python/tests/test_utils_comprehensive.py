#!/usr/bin/env python3
"""
Comprehensive tests for nodemaven.utils module.
Tests every function with edge cases and error conditions.
"""

import sys
import os
import unittest
from unittest.mock import patch, mock_open

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nodemaven.utils import (
    load_env_file, get_api_key, get_proxy_username, get_proxy_password,
    get_api_credentials, get_correct_proxy_credentials, get_base_url,
    get_proxy_host, get_http_port, get_socks5_port, get_timeout,
    is_debug_enabled, format_bytes, validate_proxy_username,
    validate_proxy_password, validate_date_format, generate_session_id,
    validate_ttl_format, build_proxy_username, build_proxy_url,
    get_proxy_config, get_socks5_proxy, clean_dict, parse_error_message
)


class TestEnvironmentFunctions(unittest.TestCase):
    """Test environment and configuration functions"""

    def test_load_env_file_existing(self):
        """Test loading environment from file"""
        env_content = "TEST_KEY=test_value\nANOTHER_KEY=another_value"
        with patch("builtins.open", mock_open(read_data=env_content)):
            with patch("os.path.exists", return_value=True):
                load_env_file(".env")
                # Function should execute without error

    def test_load_env_file_missing(self):
        """Test loading environment from missing file"""
        with patch("os.path.exists", return_value=False):
            load_env_file(".env")  # Should not raise error

    @patch.dict(os.environ, {'NODEMAVEN_APIKEY': 'test_api_key'})
    def test_get_api_key_from_env(self):
        """Test getting API key from environment"""
        self.assertEqual(get_api_key(), 'test_api_key')

    @patch.dict(os.environ, {}, clear=True)
    def test_get_api_key_missing(self):
        """Test getting API key when not set"""
        self.assertIsNone(get_api_key())

    @patch.dict(os.environ, {'NODEMAVEN_USERNAME': 'test_user'})
    def test_get_proxy_username_from_env(self):
        """Test getting proxy username from environment"""
        self.assertEqual(get_proxy_username(), 'test_user')

    @patch.dict(os.environ, {'NODEMAVEN_PASSWORD': 'test_pass'})
    def test_get_proxy_password_from_env(self):
        """Test getting proxy password from environment"""
        self.assertEqual(get_proxy_password(), 'test_pass')

    def test_get_base_url_default(self):
        """Test getting default base URL"""
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_base_url(), 'https://dashboard.nodemaven.com')

    @patch.dict(os.environ, {'NODEMAVEN_BASE_URL': 'https://custom.url'})
    def test_get_base_url_custom(self):
        """Test getting custom base URL"""
        self.assertEqual(get_base_url(), 'https://custom.url')

    def test_get_proxy_host_default(self):
        """Test getting default proxy host"""
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_proxy_host(), 'gate.nodemaven.com')

    def test_get_http_port_default(self):
        """Test getting default HTTP port"""
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_http_port(), 8080)

    @patch.dict(os.environ, {'NODEMAVEN_HTTP_PORT': '9090'})
    def test_get_http_port_custom(self):
        """Test getting custom HTTP port"""
        self.assertEqual(get_http_port(), 9090)

    @patch.dict(os.environ, {'NODEMAVEN_HTTP_PORT': 'invalid'})
    def test_get_http_port_invalid(self):
        """Test getting HTTP port with invalid value"""
        self.assertEqual(get_http_port(), 8080)  # Should fallback to default

    def test_get_socks5_port_default(self):
        """Test getting default SOCKS5 port"""
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_socks5_port(), 1080)

    def test_get_timeout_default(self):
        """Test getting default timeout"""
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_timeout(), 30)

    @patch.dict(os.environ, {'DEBUG': 'true'})
    def test_is_debug_enabled_true(self):
        """Test debug enabled"""
        self.assertTrue(is_debug_enabled())

    @patch.dict(os.environ, {'DEBUG': 'false'})
    def test_is_debug_enabled_false(self):
        """Test debug disabled"""
        self.assertFalse(is_debug_enabled())


class TestUtilityFunctions(unittest.TestCase):
    """Test utility and formatting functions"""

    def test_format_bytes_zero(self):
        """Test formatting zero bytes"""
        self.assertEqual(format_bytes(0), "0 B")

    def test_format_bytes_bytes(self):
        """Test formatting bytes"""
        self.assertEqual(format_bytes(500), "500 B")
        self.assertEqual(format_bytes(1000), "1000 B")

    def test_format_bytes_kilobytes(self):
        """Test formatting kilobytes"""
        self.assertEqual(format_bytes(1024), "1.00 KB")
        self.assertEqual(format_bytes(2048), "2.00 KB")

    def test_format_bytes_megabytes(self):
        """Test formatting megabytes"""
        self.assertEqual(format_bytes(1048576), "1.00 MB")
        self.assertEqual(format_bytes(1572864), "1.50 MB")

    def test_format_bytes_gigabytes(self):
        """Test formatting gigabytes"""
        self.assertEqual(format_bytes(1073741824), "1.00 GB")

    def test_validate_proxy_username_valid(self):
        """Test valid proxy usernames"""
        valid_usernames = [
            "test_user_123",
            "a" * 9,  # minimum length
            "a" * 100,  # maximum length
            "user123456789"
        ]
        for username in valid_usernames:
            self.assertTrue(validate_proxy_username(username))

    def test_validate_proxy_username_invalid(self):
        """Test invalid proxy usernames"""
        invalid_usernames = [
            "",  # empty
            "short",  # too short
            "a" * 101,  # too long
            "user-name",  # invalid character
            "user@name",  # invalid character
            "user name",  # space
        ]
        for username in invalid_usernames:
            self.assertFalse(validate_proxy_username(username))

    def test_validate_proxy_password_valid(self):
        """Test valid proxy passwords"""
        valid_passwords = [
            "test_pass_123",
            "a" * 9,  # minimum length
            "a" * 100,  # maximum length
        ]
        for password in valid_passwords:
            self.assertTrue(validate_proxy_password(password))

    def test_validate_proxy_password_invalid(self):
        """Test invalid proxy passwords"""
        invalid_passwords = [
            "",  # empty
            "short",  # too short
            "a" * 101,  # too long
            "pass-word",  # invalid character
        ]
        for password in invalid_passwords:
            self.assertFalse(validate_proxy_password(password))

    def test_validate_date_format_valid(self):
        """Test valid date formats"""
        valid_dates = [
            "01-01-2023",
            "25-12-2023",
            "31-12-2023"
        ]
        for date in valid_dates:
            # Should not raise exception
            validate_date_format(date)

    def test_validate_date_format_invalid(self):
        """Test invalid date formats"""
        invalid_dates = [
            "2023-01-01",  # wrong format
            "1-1-2023",  # missing zero padding
            "32-01-2023",  # invalid day
            "01-13-2023",  # invalid month
            "invalid-date",  # completely invalid
            ""  # empty
        ]
        for date in invalid_dates:
            with self.assertRaises(ValueError):
                validate_date_format(date)

    def test_generate_session_id(self):
        """Test session ID generation"""
        session1 = generate_session_id()
        session2 = generate_session_id()
        
        # Should be different
        self.assertNotEqual(session1, session2)
        
        # Should be 13 characters
        self.assertEqual(len(session1), 13)
        self.assertEqual(len(session2), 13)
        
        # Should be alphanumeric
        self.assertTrue(session1.isalnum())
        self.assertTrue(session2.isalnum())

    def test_validate_ttl_format_valid(self):
        """Test valid TTL formats"""
        valid_ttls = ["60s", "1m", "5m", "1h", "24h", "999s", "100m", "48h"]
        for ttl in valid_ttls:
            self.assertTrue(validate_ttl_format(ttl))

    def test_validate_ttl_format_invalid(self):
        """Test invalid TTL formats"""
        invalid_ttls = ["60", "1x", "invalid", "", "1.5h", "60 s", "60S"]
        for ttl in invalid_ttls:
            self.assertFalse(validate_ttl_format(ttl))

    def test_clean_dict(self):
        """Test dictionary cleaning"""
        dirty_dict = {"a": 1, "b": None, "c": "test", "d": None, "e": 0}
        expected = {"a": 1, "c": "test", "e": 0}
        self.assertEqual(clean_dict(dirty_dict), expected)

    def test_clean_dict_empty(self):
        """Test cleaning empty dictionary"""
        self.assertEqual(clean_dict({}), {})

    def test_clean_dict_all_none(self):
        """Test cleaning dictionary with all None values"""
        self.assertEqual(clean_dict({"a": None, "b": None}), {})


class TestErrorMessageParsing(unittest.TestCase):
    """Test error message parsing"""

    def test_parse_error_message_error_key(self):
        """Test parsing with 'error' key"""
        response = {"error": "Test error message"}
        self.assertEqual(parse_error_message(response), "Test error message")

    def test_parse_error_message_detail_key(self):
        """Test parsing with 'detail' key"""
        response = {"detail": "Test detail message"}
        self.assertEqual(parse_error_message(response), "Test detail message")

    def test_parse_error_message_errors_dict(self):
        """Test parsing with 'errors' dictionary"""
        response = {"errors": {"field1": ["Error 1", "Error 2"], "field2": "Single error"}}
        result = parse_error_message(response)
        self.assertIn("field1: Error 1", result)
        self.assertIn("field1: Error 2", result)
        self.assertIn("field2: Single error", result)

    def test_parse_error_message_errors_list(self):
        """Test parsing with 'errors' list"""
        response = {"errors": ["Error 1", "Error 2"]}
        result = parse_error_message(response)
        self.assertIn("Error 1", result)
        self.assertIn("Error 2", result)

    def test_parse_error_message_unknown(self):
        """Test parsing unknown error format"""
        response = {"unknown": "test"}
        self.assertEqual(parse_error_message(response), "Unknown error occurred")

    def test_parse_error_message_empty(self):
        """Test parsing empty response"""
        self.assertEqual(parse_error_message({}), "Unknown error occurred")


class TestProxyBuilding(unittest.TestCase):
    """Test proxy username and URL building"""

    def test_build_proxy_username_basic(self):
        """Test basic proxy username building"""
        username = build_proxy_username("testuser", country="us")
        self.assertEqual(username, "testuser-country-us")

    def test_build_proxy_username_full_hierarchy(self):
        """Test full location hierarchy"""
        username = build_proxy_username(
            "testuser", 
            country="us", 
            region="new_york", 
            city="brooklyn", 
            isp="verizon_home"
        )
        expected = "testuser-country-us-region-new_york-city-brooklyn-isp-verizon_home"
        self.assertEqual(username, expected)

    def test_build_proxy_username_mobile_type(self):
        """Test mobile connection type"""
        username = build_proxy_username("testuser", country="us", type="mobile")
        self.assertEqual(username, "testuser-country-us-type-mobile")

    def test_build_proxy_username_ipv4_explicit(self):
        """Test explicit IPv4 setting"""
        username = build_proxy_username("testuser", country="us", ipv4=True)
        self.assertEqual(username, "testuser-country-us-ipv4-true")

    def test_build_proxy_username_session(self):
        """Test session ID"""
        username = build_proxy_username("testuser", country="us", session="test123")
        self.assertEqual(username, "testuser-country-us-sid-test123")

    def test_build_proxy_username_sticky(self):
        """Test sticky session generation"""
        username = build_proxy_username("testuser", country="us", sticky=True)
        self.assertIn("-sid-", username)
        # Extract session ID and verify format
        parts = username.split("-")
        sid_index = parts.index("sid") + 1
        session_id = parts[sid_index]
        self.assertEqual(len(session_id), 13)
        self.assertTrue(session_id.isalnum())

    def test_build_proxy_username_ttl(self):
        """Test TTL functionality"""
        username = build_proxy_username("testuser", country="us", session="test123", ttl="24h")
        self.assertEqual(username, "testuser-country-us-sid-test123-ttl-24h")

    def test_build_proxy_username_ttl_invalid(self):
        """Test invalid TTL format"""
        with self.assertRaises(ValueError):
            build_proxy_username("testuser", country="us", session="test123", ttl="invalid")

    def test_build_proxy_username_ttl_without_session(self):
        """Test TTL without session (should be ignored)"""
        username = build_proxy_username("testuser", country="us", ttl="24h")
        self.assertNotIn("ttl", username)

    def test_build_proxy_username_filter(self):
        """Test IP filter"""
        username = build_proxy_username("testuser", country="us", filter="medium")
        self.assertEqual(username, "testuser-country-us-filter-medium")

    def test_build_proxy_username_space_handling(self):
        """Test space to underscore conversion"""
        username = build_proxy_username("testuser", region="new york", city="san francisco")
        self.assertIn("region-new_york", username)
        self.assertIn("city-san_francisco", username)

    def test_build_proxy_username_documentation_examples(self):
        """Test examples from how-api-works.md"""
        # Example 1: Residential / US / Brooklyn / Rotating / No Filter
        username1 = build_proxy_username("aa101d91571b74", country="us", region="new_york", city="brooklyn")
        expected1 = "aa101d91571b74-country-us-region-new_york-city-brooklyn"
        self.assertEqual(username1, expected1)

        # Example 2: Mobile / IPv4 / Sticky / TTL / Filter
        username2 = build_proxy_username(
            "aa101d91571b74", 
            country="any", 
            type="mobile", 
            ipv4=True, 
            session="a49c071423294", 
            ttl="24h", 
            filter="medium"
        )
        expected2 = "aa101d91571b74-country-any-type-mobile-ipv4-true-sid-a49c071423294-ttl-24h-filter-medium"
        self.assertEqual(username2, expected2)

    @patch('nodemaven.utils.get_correct_proxy_credentials')
    def test_build_proxy_url_http(self, mock_creds):
        """Test HTTP proxy URL building"""
        mock_creds.return_value = ("testuser", "testpass")
        
        url = build_proxy_url(protocol="http", country="us")
        expected = "http://testuser-country-us:testpass@gate.nodemaven.com:8080"
        self.assertEqual(url, expected)

    @patch('nodemaven.utils.get_correct_proxy_credentials')
    def test_build_proxy_url_socks5(self, mock_creds):
        """Test SOCKS5 proxy URL building"""
        mock_creds.return_value = ("testuser", "testpass")
        
        url = build_proxy_url(protocol="socks5", country="us")
        expected = "socks5://testuser-country-us:testpass@gate.nodemaven.com:1080"
        self.assertEqual(url, expected)

    @patch('nodemaven.utils.get_correct_proxy_credentials')
    def test_build_proxy_url_no_credentials(self, mock_creds):
        """Test proxy URL building without credentials"""
        mock_creds.return_value = (None, None)
        
        with self.assertRaises(ValueError):
            build_proxy_url(country="us")

    @patch('nodemaven.utils.get_correct_proxy_credentials')
    def test_get_proxy_config(self, mock_creds):
        """Test proxy configuration dictionary"""
        mock_creds.return_value = ("testuser", "testpass")
        
        config = get_proxy_config(country="us")
        expected_url = "http://testuser-country-us:testpass@gate.nodemaven.com:8080"
        
        self.assertEqual(config['http'], expected_url)
        self.assertEqual(config['https'], expected_url)

    @patch('nodemaven.utils.get_correct_proxy_credentials')
    def test_get_socks5_proxy(self, mock_creds):
        """Test SOCKS5 proxy URL"""
        mock_creds.return_value = ("testuser", "testpass")
        
        url = get_socks5_proxy(country="us")
        expected = "socks5://testuser-country-us:testpass@gate.nodemaven.com:1080"
        self.assertEqual(url, expected)


def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*50)
    print(f"🧪 Tests run: {result.testsRun}")
    print(f"✅ Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"💥 Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"   {test}: {traceback}")
    
    if result.errors:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"   {test}: {traceback}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\n🎯 Success rate: {success_rate:.1f}%")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 