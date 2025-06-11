#!/usr/bin/env python3
"""
Comprehensive tests for nodemaven.client module.
Tests all API endpoints, error handling, and client functionality.
"""

import sys
import os
import unittest
from unittest.mock import patch, Mock, MagicMock
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nodemaven.client import NodeMavenClient
from nodemaven.exceptions import NodeMavenAPIError, AuthenticationError


class TestClientInitialization(unittest.TestCase):
    """Test client initialization and configuration"""

    def test_init_with_api_key(self):
        """Test client initialization with API key"""
        client = NodeMavenClient(api_key="test_key")
        self.assertEqual(client.api_key, "test_key")
        self.assertIsNotNone(client.base_url)
        self.assertIsNotNone(client.timeout)

    def test_init_without_api_key(self):
        """Test client initialization without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                NodeMavenClient()

    @patch.dict(os.environ, {'NODEMAVEN_APIKEY': 'env_key'})
    def test_init_with_env_api_key(self):
        """Test client initialization with environment API key"""
        client = NodeMavenClient()
        self.assertEqual(client.api_key, "env_key")

    def test_init_with_custom_base_url(self):
        """Test client initialization with custom base URL"""
        client = NodeMavenClient(api_key="test", base_url="https://custom.api")
        self.assertEqual(client.base_url, "https://custom.api")

    def test_init_with_custom_timeout(self):
        """Test client initialization with custom timeout"""
        client = NodeMavenClient(api_key="test", timeout=60)
        self.assertEqual(client.timeout, 60)

    @patch('nodemaven.client.HAS_REQUESTS', False)
    def test_init_without_requests_library(self):
        """Test client initialization without requests library"""
        client = NodeMavenClient(api_key="test")
        self.assertIsNone(client.session)


class TestRequestMethods(unittest.TestCase):
    """Test HTTP request methods"""

    def setUp(self):
        self.client = NodeMavenClient(api_key="test_key")

    @patch('nodemaven.client.HAS_REQUESTS', True)
    @patch('requests.Session')
    def test_make_request_requests_success(self, mock_session_class):
        """Test successful request using requests library"""
        # Setup mock
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"test": "data"}
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        # Create client and set session
        client = NodeMavenClient(api_key="test_key")
        client.session = mock_session
        
        # Test request
        result = client._make_request_requests("GET", "/test", {"param": "value"})
        
        # Verify
        self.assertEqual(result, {"test": "data"})
        mock_session.request.assert_called_once()

    @patch('nodemaven.client.HAS_REQUESTS', True)
    @patch('requests.Session')
    def test_make_request_requests_error(self, mock_session_class):
        """Test error response using requests library"""
        # Setup mock
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"detail": "Bad request"}
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        # Create client and set session
        client = NodeMavenClient(api_key="test_key")
        client.session = mock_session
        
        # Test request should raise exception
        with self.assertRaises(NodeMavenAPIError):
            client._make_request_requests("GET", "/test")

    @patch('urllib.request.urlopen')
    def test_make_request_urllib_success(self, mock_urlopen):
        """Test successful request using urllib"""
        # Setup mock
        mock_response = Mock()
        mock_response.read.return_value = b'{"test": "data"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Test request
        result = self.client._make_request_urllib("GET", "https://api.test/endpoint")
        
        # Verify
        self.assertEqual(result, {"test": "data"})

    @patch('urllib.request.urlopen')
    def test_make_request_urllib_http_error(self, mock_urlopen):
        """Test HTTP error using urllib"""
        from urllib.error import HTTPError
        
        # Setup mock
        error = HTTPError("url", 401, "Unauthorized", {}, None)
        error.read = Mock(return_value=b'{"detail": "Unauthorized"}')
        mock_urlopen.side_effect = error
        
        # Test request should raise exception
        with self.assertRaises(AuthenticationError):
            self.client._make_request_urllib("GET", "https://api.test/endpoint")

    def test_make_request_delegates_correctly(self):
        """Test that _make_request delegates to correct method"""
        with patch.object(self.client, '_make_request_requests') as mock_requests:
            with patch('nodemaven.client.HAS_REQUESTS', True):
                self.client.session = Mock()  # Simulate requests session
                self.client._make_request("GET", "/test")
                mock_requests.assert_called_once_with("GET", "/test", None, None)

    def test_make_request_falls_back_to_urllib(self):
        """Test that _make_request falls back to urllib when no session"""
        with patch.object(self.client, '_make_request_urllib') as mock_urllib:
            self.client.session = None
            self.client._make_request("GET", "/test")
            mock_urllib.assert_called_once()


class TestUserEndpoints(unittest.TestCase):
    """Test user-related API endpoints"""

    def setUp(self):
        self.client = NodeMavenClient(api_key="test_key")

    @patch.object(NodeMavenClient, '_make_request')
    def test_get_user_info(self, mock_request):
        """Test getting user information"""
        mock_request.return_value = {
            "email": "test@example.com",
            "proxy_username": "testuser",
            "data": 1000000
        }
        
        result = self.client.get_user_info()
        
        mock_request.assert_called_once_with('GET', '/api/v2/base/users/me')
        self.assertEqual(result["email"], "test@example.com")


class TestLocationEndpoints(unittest.TestCase):
    """Test location-related API endpoints"""

    def setUp(self):
        self.client = NodeMavenClient(api_key="test_key")

    @patch.object(NodeMavenClient, '_make_request')
    def test_get_countries_default(self, mock_request):
        """Test getting countries with default parameters"""
        mock_request.return_value = {"results": [{"name": "US", "code": "us"}]}
        
        result = self.client.get_countries()
        
        expected_params = {
            'limit': 50,
            'offset': 0,
            'name': None,
            'code': None,
            'connection_type': 'residential'
        }
        mock_request.assert_called_once_with('GET', '/api/v2/base/locations/countries/', expected_params)

    @patch.object(NodeMavenClient, '_make_request')
    def test_get_countries_custom_params(self, mock_request):
        """Test getting countries with custom parameters"""
        mock_request.return_value = {"results": []}
        
        self.client.get_countries(limit=10, offset=20, name="United", code="us", connection_type="mobile")
        
        expected_params = {
            'limit': 10,
            'offset': 20,
            'name': 'United',
            'code': 'us',
            'connection_type': 'mobile'
        }
        mock_request.assert_called_once_with('GET', '/api/v2/base/locations/countries/', expected_params)

    @patch.object(NodeMavenClient, '_make_request')
    def test_get_regions(self, mock_request):
        """Test getting regions"""
        mock_request.return_value = {"results": []}
        
        self.client.get_regions(country_code="us", name="California")
        
        expected_params = {
            'limit': 50,
            'offset': 0,
            'country__code': 'us',
            'name': 'California',
            'code': None,
            'connection_type': 'residential'
        }
        mock_request.assert_called_once_with('GET', '/api/v2/base/locations/regions/', expected_params)

    @patch.object(NodeMavenClient, '_make_request')
    def test_get_cities(self, mock_request):
        """Test getting cities"""
        mock_request.return_value = {"results": []}
        
        self.client.get_cities(country_code="us", region_code="ca", name="Los Angeles")
        
        expected_params = {
            'limit': 50,
            'offset': 0,
            'country__code': 'us',
            'region__code': 'ca',
            'name': 'Los Angeles',
            'code': None,
            'connection_type': 'residential'
        }
        mock_request.assert_called_once_with('GET', '/api/v2/base/locations/cities/', expected_params)

    @patch.object(NodeMavenClient, '_make_request')
    def test_get_isps(self, mock_request):
        """Test getting ISPs"""
        mock_request.return_value = {"results": []}
        
        self.client.get_isps(country_code="us", region_code="ca", city_code="la", name="Verizon")
        
        expected_params = {
            'limit': 50,
            'offset': 0,
            'country__code': 'us',
            'region__code': 'ca',
            'city__code': 'la',
            'name': 'Verizon',
            'connection_type': 'residential'
        }
        mock_request.assert_called_once_with('GET', '/api/v2/base/locations/isps/', expected_params)

    @patch.object(NodeMavenClient, '_make_request')
    def test_get_zip_codes(self, mock_request):
        """Test getting ZIP codes"""
        mock_request.return_value = {"results": []}
        
        self.client.get_zip_codes(country_code="us", region_code="ca", city_code="la", code="90210")
        
        expected_params = {
            'limit': 50,
            'offset': 0,
            'country__code': 'us',
            'region__code': 'ca',
            'city__code': 'la',
            'code': '90210',
            'connection_type': 'residential'
        }
        mock_request.assert_called_once_with('GET', '/api/v2/base/locations/zip-codes/', expected_params)


class TestStatisticsEndpoints(unittest.TestCase):
    """Test statistics-related API endpoints"""

    def setUp(self):
        self.client = NodeMavenClient(api_key="test_key")

    @patch.object(NodeMavenClient, '_make_request')
    def test_get_statistics_default(self, mock_request):
        """Test getting statistics with default parameters"""
        mock_request.return_value = {"stats": []}
        
        result = self.client.get_statistics()
        
        expected_params = {'group_by': 'day'}
        mock_request.assert_called_once_with('GET', '/api/v2/base/statistics/', expected_params)

    @patch.object(NodeMavenClient, '_make_request')
    def test_get_statistics_with_dates(self, mock_request):
        """Test getting statistics with date range"""
        mock_request.return_value = {"stats": []}
        
        result = self.client.get_statistics(start_date="01-01-2023", end_date="31-01-2023", group_by="week")
        
        expected_params = {
            'start_date': '01-01-2023',
            'end_date': '31-01-2023',
            'group_by': 'week'
        }
        mock_request.assert_called_once_with('GET', '/api/v2/base/statistics/', expected_params)

    @patch.object(NodeMavenClient, '_make_request')
    def test_get_statistics_invalid_date(self, mock_request):
        """Test getting statistics with invalid date format"""
        with self.assertRaises(ValueError):
            self.client.get_statistics(start_date="2023-01-01")  # Wrong format

    @patch.object(NodeMavenClient, '_make_request')
    def test_get_domain_statistics(self, mock_request):
        """Test getting domain statistics"""
        mock_request.return_value = {"results": []}
        
        result = self.client.get_domain_statistics(
            start_date="01-01-2023", 
            end_date="31-01-2023",
            limit=100,
            offset=50
        )
        
        expected_params = {
            'start_date': '01-01-2023',
            'end_date': '31-01-2023',
            'limit': 100,
            'offset': 50
        }
        mock_request.assert_called_once_with('GET', '/api/v2/base/statistics/domains/', expected_params)


class TestSubUserEndpoints(unittest.TestCase):
    """Test sub-user management endpoints"""

    def setUp(self):
        self.client = NodeMavenClient(api_key="test_key")

    @patch.object(NodeMavenClient, '_make_request')
    def test_get_sub_users(self, mock_request):
        """Test getting sub-users"""
        mock_request.return_value = {"results": []}
        
        result = self.client.get_sub_users(limit=25, offset=10)
        
        expected_params = {'limit': 25, 'offset': 10}
        mock_request.assert_called_once_with('GET', '/api/v2/base/sub-users/', expected_params)

    @patch.object(NodeMavenClient, '_make_request')
    def test_create_sub_user_minimal(self, mock_request):
        """Test creating sub-user with minimal parameters"""
        mock_request.return_value = {"id": "123", "username": "testuser"}
        
        result = self.client.create_sub_user("testuser", "testpass")
        
        expected_data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        mock_request.assert_called_once_with('POST', '/api/v2/base/sub-users/', json_data=expected_data)

    @patch.object(NodeMavenClient, '_make_request')
    def test_create_sub_user_full(self, mock_request):
        """Test creating sub-user with all parameters"""
        mock_request.return_value = {"id": "123"}
        
        result = self.client.create_sub_user(
            "testuser", 
            "testpass", 
            traffic_limit=1000000,
            expiry_date="31-12-2023"
        )
        
        expected_data = {
            'username': 'testuser',
            'password': 'testpass',
            'traffic_limit': 1000000,
            'expiry_date': '31-12-2023'
        }
        mock_request.assert_called_once_with('POST', '/api/v2/base/sub-users/', json_data=expected_data)

    @patch.object(NodeMavenClient, '_make_request')
    def test_create_sub_user_invalid_date(self, mock_request):
        """Test creating sub-user with invalid date"""
        with self.assertRaises(ValueError):
            self.client.create_sub_user("user", "pass", expiry_date="2023-12-31")

    @patch.object(NodeMavenClient, '_make_request')
    def test_update_sub_user(self, mock_request):
        """Test updating sub-user"""
        mock_request.return_value = {"id": "123"}
        
        result = self.client.update_sub_user(
            "123",
            username="newuser",
            traffic_limit=2000000
        )
        
        expected_data = {
            'username': 'newuser',
            'traffic_limit': 2000000
        }
        mock_request.assert_called_once_with('PATCH', '/api/v2/base/sub-users/123/', json_data=expected_data)

    @patch.object(NodeMavenClient, '_make_request')
    def test_delete_sub_user(self, mock_request):
        """Test deleting sub-user"""
        mock_request.return_value = {}
        
        result = self.client.delete_sub_user("123")
        
        mock_request.assert_called_once_with('DELETE', '/api/v2/base/sub-users/123/')


class TestWhitelistEndpoints(unittest.TestCase):
    """Test IP whitelist management endpoints"""

    def setUp(self):
        self.client = NodeMavenClient(api_key="test_key")

    @patch.object(NodeMavenClient, '_make_request')
    def test_get_whitelist_ips(self, mock_request):
        """Test getting whitelist IPs"""
        mock_request.return_value = {"results": []}
        
        result = self.client.get_whitelist_ips(limit=25, offset=10)
        
        expected_params = {'limit': 25, 'offset': 10}
        mock_request.assert_called_once_with('GET', '/api/v2/base/whitelist-ips/', expected_params)

    @patch.object(NodeMavenClient, '_make_request')
    def test_add_whitelist_ip_minimal(self, mock_request):
        """Test adding IP to whitelist with minimal parameters"""
        mock_request.return_value = {"id": "123"}
        
        result = self.client.add_whitelist_ip("192.168.1.1")
        
        expected_data = {'ip_address': '192.168.1.1'}
        mock_request.assert_called_once_with('POST', '/api/v2/base/whitelist-ips/', json_data=expected_data)

    @patch.object(NodeMavenClient, '_make_request')
    def test_add_whitelist_ip_with_description(self, mock_request):
        """Test adding IP to whitelist with description"""
        mock_request.return_value = {"id": "123"}
        
        result = self.client.add_whitelist_ip("192.168.1.1", "Office IP")
        
        expected_data = {
            'ip_address': '192.168.1.1',
            'description': 'Office IP'
        }
        mock_request.assert_called_once_with('POST', '/api/v2/base/whitelist-ips/', json_data=expected_data)

    @patch.object(NodeMavenClient, '_make_request')
    def test_delete_whitelist_ip(self, mock_request):
        """Test removing IP from whitelist"""
        mock_request.return_value = {}
        
        result = self.client.delete_whitelist_ip("123")
        
        mock_request.assert_called_once_with('DELETE', '/api/v2/base/whitelist-ips/123/')


class TestErrorHandling(unittest.TestCase):
    """Test error handling and exception scenarios"""

    def setUp(self):
        self.client = NodeMavenClient(api_key="test_key")

    @patch.object(NodeMavenClient, '_make_request')
    def test_authentication_error(self, mock_request):
        """Test authentication error handling"""
        mock_request.side_effect = AuthenticationError("Invalid API key", 401)
        
        with self.assertRaises(AuthenticationError):
            self.client.get_user_info()

    @patch.object(NodeMavenClient, '_make_request')
    def test_general_api_error(self, mock_request):
        """Test general API error handling"""
        mock_request.side_effect = NodeMavenAPIError("Server error", 500)
        
        with self.assertRaises(NodeMavenAPIError):
            self.client.get_countries()


def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*50)
    print(f"🧪 Client Tests run: {result.testsRun}")
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
    print(f"\n🎯 Client Success rate: {success_rate:.1f}%")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 