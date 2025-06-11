#!/usr/bin/env python3
"""
Package Validation Test Suite
Tests that all package components work correctly together
"""

import sys
import os
import unittest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from nodemaven import utils, client, exceptions
from nodemaven.utils import build_proxy_username, generate_session_id, validate_ttl_format
from nodemaven.client import NodeMavenClient, get_socks5_proxy
from nodemaven.exceptions import NodeMavenException, InvalidCredentialsException

class TestPackageValidation(unittest.TestCase):
    """Test that all package components work correctly"""
    
    def test_package_imports(self):
        """Test that all modules can be imported"""
        print("🔍 Testing package imports...")
        
        # Test module imports
        self.assertIsNotNone(utils)
        self.assertIsNotNone(client) 
        self.assertIsNotNone(exceptions)
        
        # Test function imports
        self.assertTrue(callable(build_proxy_username))
        self.assertTrue(callable(generate_session_id))
        self.assertTrue(callable(validate_ttl_format))
        self.assertTrue(callable(get_socks5_proxy))
        
        # Test class imports
        self.assertTrue(callable(NodeMavenClient))
        self.assertTrue(callable(NodeMavenException))
        self.assertTrue(callable(InvalidCredentialsException))
        
        print("✅ All imports successful")
    
    def test_utils_functionality(self):
        """Test utils module functionality"""
        print("🔧 Testing utils functionality...")
        
        # Test basic username building
        username = build_proxy_username("test_user", country="us")
        self.assertIn("test_user", username)
        self.assertIn("country-us", username)
        
        # Test complex mobile proxy
        mobile_username = build_proxy_username(
            "alex_worldmediabuy_com",
            country="us",
            region="new york",
            city="new york city",
            isp="verizon g home internet",
            type="mobile",
            ipv4=True,
            sticky=True,
            ttl="12h",
            filter="medium"
        )
        
        expected_components = [
            "alex_worldmediabuy_com",
            "country-us",
            "region-new_york", 
            "city-new_york_city",
            "isp-verizon_g_home_internet",
            "type-mobile",
            "ipv4-true",
            "sid-",  # Session ID prefix
            "ttl-12h",
            "filter-medium"
        ]
        
        for component in expected_components:
            self.assertIn(component, mobile_username)
        
        # Test session ID generation
        session_id = generate_session_id()
        self.assertEqual(len(session_id), 13)
        self.assertTrue(session_id.isalnum())
        
        # Test TTL validation
        self.assertTrue(validate_ttl_format("60s"))
        self.assertTrue(validate_ttl_format("5m"))
        self.assertTrue(validate_ttl_format("1h"))
        self.assertTrue(validate_ttl_format("24h"))
        self.assertFalse(validate_ttl_format("invalid"))
        
        print("✅ Utils functionality working")
    
    def test_client_functionality(self):
        """Test client module functionality"""
        print("🌐 Testing client functionality...")
        
        # Test client initialization with invalid key (should not crash)
        try:
            client_instance = NodeMavenClient("invalid_key")
            self.assertIsNotNone(client_instance)
        except Exception as e:
            self.fail(f"Client initialization failed: {e}")
        
        # Test that client has required methods
        self.assertTrue(hasattr(NodeMavenClient, 'get_socks5_proxy'))
        self.assertTrue(hasattr(NodeMavenClient, 'get_http_proxy'))
        
        # Test get_socks5_proxy function availability
        self.assertTrue(callable(get_socks5_proxy))
        
        print("✅ Client functionality working")
    
    def test_exceptions_functionality(self):
        """Test exceptions module functionality"""
        print("⚠️ Testing exceptions functionality...")
        
        # Test exception creation
        base_exception = NodeMavenException("Test message")
        self.assertEqual(str(base_exception), "Test message")
        
        # Test specific exception
        creds_exception = InvalidCredentialsException("Invalid API key")
        self.assertEqual(str(creds_exception), "Invalid API key")
        self.assertIsInstance(creds_exception, NodeMavenException)
        
        print("✅ Exceptions functionality working")
    
    def test_integration(self):
        """Test integration between modules"""
        print("🔗 Testing module integration...")
        
        # Test that client can use utils functions
        try:
            # This should work even without valid credentials for username building
            username = build_proxy_username("test", country="us", ttl="1h")
            self.assertIn("test", username)
            self.assertIn("country-us", username)
            self.assertIn("ttl-1h", username)
        except Exception as e:
            self.fail(f"Integration test failed: {e}")
        
        # Test direct username building with all components
        full_username = build_proxy_username(
            "alex_worldmediabuy_com",
            country="us",
            region="california", 
            city="los angeles",
            isp="at&t",
            type="datacenter",
            ipv4=True,
            ipv6=False,
            session="test123",
            ttl="6h",
            filter="high"
        )
        
        # Verify all components are present
        components = [
            "alex_worldmediabuy_com",
            "country-us",
            "region-california",
            "city-los_angeles", 
            "isp-at&t",
            "type-datacenter",
            "ipv4-true",
            "ipv6-false",
            "sid-test123",
            "ttl-6h",
            "filter-high"
        ]
        
        for component in components:
            self.assertIn(component, full_username)
        
        print("✅ Integration working")

def run_validation_tests():
    """Run all package validation tests"""
    print("🚀 NodeMaven Package Validation")
    print("=" * 35)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPackageValidation)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print(f"\n📊 Test Results Summary")
    print("=" * 25)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  • {test}: {traceback}")
    
    if result.errors:
        print(f"\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"  • {test}: {traceback}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\n✅ Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("🎉 All package validation tests passed!")
        return True
    else:
        print("⚠️ Some tests failed - check the output above")
        return False

if __name__ == "__main__":
    success = run_validation_tests()
    sys.exit(0 if success else 1) 