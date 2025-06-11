#!/usr/bin/env python3
"""
Comprehensive tests for nodemaven.exceptions module.
Tests all exception classes and error handling scenarios.
"""

import sys
import os
import unittest

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nodemaven.exceptions import (
    NodeMavenAPIError, AuthenticationError, RateLimitError, 
    ValidationError, get_exception_for_status_code
)


class TestNodeMavenAPIError(unittest.TestCase):
    """Test base NodeMavenAPIError exception"""

    def test_init_minimal(self):
        """Test exception with minimal parameters"""
        error = NodeMavenAPIError("Test error")
        self.assertEqual(str(error), "[None] Test error")
        self.assertEqual(error.message, "Test error")
        self.assertIsNone(error.status_code)
        self.assertEqual(error.response_data, {})

    def test_init_with_status_code(self):
        """Test exception with status code"""
        error = NodeMavenAPIError("Test error", 400)
        self.assertEqual(str(error), "[400] Test error")
        self.assertEqual(error.status_code, 400)

    def test_init_with_response_data(self):
        """Test exception with response data"""
        response_data = {"field": "error", "details": "validation failed"}
        error = NodeMavenAPIError("Test error", 400, response_data)
        self.assertEqual(error.response_data, response_data)

    def test_init_full(self):
        """Test exception with all parameters"""
        response_data = {"error": "detailed error"}
        error = NodeMavenAPIError("Test error", 400, response_data)
        
        self.assertEqual(str(error), "[400] Test error")
        self.assertEqual(error.message, "Test error")
        self.assertEqual(error.status_code, 400)
        self.assertEqual(error.response_data, response_data)

    def test_repr(self):
        """Test string representation"""
        error = NodeMavenAPIError("Test error", 400)
        expected = "NodeMavenAPIError('[400] Test error')"
        self.assertEqual(repr(error), expected)


class TestAuthenticationError(unittest.TestCase):
    """Test AuthenticationError exception"""

    def test_init_minimal(self):
        """Test authentication error with minimal parameters"""
        error = AuthenticationError("Invalid API key")
        self.assertEqual(str(error), "[None] Invalid API key")
        self.assertIsInstance(error, NodeMavenAPIError)

    def test_init_with_status_code(self):
        """Test authentication error with status code"""
        error = AuthenticationError("Invalid API key", 401)
        self.assertEqual(str(error), "[401] Invalid API key")
        self.assertEqual(error.status_code, 401)

    def test_init_with_response_data(self):
        """Test authentication error with response data"""
        response_data = {"detail": "Token expired"}
        error = AuthenticationError("Token expired", 401, response_data)
        self.assertEqual(error.response_data, response_data)


class TestRateLimitError(unittest.TestCase):
    """Test RateLimitError exception"""

    def test_init_minimal(self):
        """Test rate limit error with minimal parameters"""
        error = RateLimitError("Rate limit exceeded")
        self.assertEqual(str(error), "[None] Rate limit exceeded")
        self.assertIsInstance(error, NodeMavenAPIError)

    def test_init_with_status_code(self):
        """Test rate limit error with status code"""
        error = RateLimitError("Rate limit exceeded", 429)
        self.assertEqual(str(error), "[429] Rate limit exceeded")
        self.assertEqual(error.status_code, 429)

    def test_init_with_retry_after(self):
        """Test rate limit error with retry-after header"""
        response_data = {"retry_after": 60}
        error = RateLimitError("Rate limit exceeded", 429, response_data)
        self.assertEqual(error.response_data["retry_after"], 60)


class TestValidationError(unittest.TestCase):
    """Test ValidationError exception"""

    def test_init_minimal(self):
        """Test validation error with minimal parameters"""
        error = ValidationError("Invalid input")
        self.assertEqual(str(error), "[None] Invalid input")
        self.assertIsInstance(error, NodeMavenAPIError)

    def test_init_with_status_code(self):
        """Test validation error with status code"""
        error = ValidationError("Invalid input", 422)
        self.assertEqual(str(error), "[422] Invalid input")
        self.assertEqual(error.status_code, 422)

    def test_init_with_field_errors(self):
        """Test validation error with field-specific errors"""
        response_data = {
            "errors": {
                "username": ["This field is required"],
                "email": ["Invalid email format"]
            }
        }
        error = ValidationError("Validation failed", 422, response_data)
        self.assertEqual(error.response_data["errors"]["username"], ["This field is required"])


class TestExceptionFactory(unittest.TestCase):
    """Test get_exception_for_status_code factory function"""

    def test_200_success(self):
        """Test successful status codes don't raise exceptions"""
        # This function should only be called for error status codes
        # so we test edge cases
        pass

    def test_400_bad_request(self):
        """Test 400 Bad Request"""
        exception = get_exception_for_status_code(400, "Bad request")
        self.assertIsInstance(exception, ValidationError)
        self.assertEqual(str(exception), "[400] Bad request")

    def test_401_unauthorized(self):
        """Test 401 Unauthorized"""
        exception = get_exception_for_status_code(401, "Unauthorized")
        self.assertIsInstance(exception, AuthenticationError)
        self.assertEqual(str(exception), "[401] Unauthorized")

    def test_403_forbidden(self):
        """Test 403 Forbidden"""
        exception = get_exception_for_status_code(403, "Forbidden")
        self.assertIsInstance(exception, AuthenticationError)
        self.assertEqual(str(exception), "[403] Forbidden")

    def test_404_not_found(self):
        """Test 404 Not Found"""
        exception = get_exception_for_status_code(404, "Not found")
        self.assertIsInstance(exception, NodeMavenAPIError)
        self.assertEqual(str(exception), "[404] Not found")

    def test_422_unprocessable_entity(self):
        """Test 422 Unprocessable Entity"""
        exception = get_exception_for_status_code(422, "Validation error")
        self.assertIsInstance(exception, ValidationError)
        self.assertEqual(str(exception), "[422] Validation error")

    def test_429_rate_limit(self):
        """Test 429 Too Many Requests"""
        exception = get_exception_for_status_code(429, "Rate limit exceeded")
        self.assertIsInstance(exception, RateLimitError)
        self.assertEqual(str(exception), "[429] Rate limit exceeded")

    def test_500_server_error(self):
        """Test 500 Internal Server Error"""
        exception = get_exception_for_status_code(500, "Server error")
        self.assertIsInstance(exception, NodeMavenAPIError)
        self.assertEqual(str(exception), "[500] Server error")

    def test_502_bad_gateway(self):
        """Test 502 Bad Gateway"""
        exception = get_exception_for_status_code(502, "Bad gateway")
        self.assertIsInstance(exception, NodeMavenAPIError)
        self.assertEqual(str(exception), "[502] Bad gateway")

    def test_503_service_unavailable(self):
        """Test 503 Service Unavailable"""
        exception = get_exception_for_status_code(503, "Service unavailable")
        self.assertIsInstance(exception, NodeMavenAPIError)
        self.assertEqual(str(exception), "[503] Service unavailable")

    def test_unknown_status_code(self):
        """Test unknown status code"""
        exception = get_exception_for_status_code(999, "Unknown error")
        self.assertIsInstance(exception, NodeMavenAPIError)
        self.assertEqual(str(exception), "[999] Unknown error")

    def test_with_response_data(self):
        """Test exception creation with response data"""
        response_data = {"detail": "Detailed error message"}
        exception = get_exception_for_status_code(400, "Bad request", response_data)
        self.assertEqual(exception.response_data, response_data)

    def test_authentication_errors_priority(self):
        """Test that authentication errors are properly classified"""
        # 401 should be AuthenticationError
        auth_error = get_exception_for_status_code(401, "Invalid token")
        self.assertIsInstance(auth_error, AuthenticationError)
        
        # 403 should also be AuthenticationError (permission denied)
        perm_error = get_exception_for_status_code(403, "Permission denied")
        self.assertIsInstance(perm_error, AuthenticationError)

    def test_validation_errors_priority(self):
        """Test that validation errors are properly classified"""
        # 400 should be ValidationError
        bad_request = get_exception_for_status_code(400, "Invalid data")
        self.assertIsInstance(bad_request, ValidationError)
        
        # 422 should be ValidationError
        validation_error = get_exception_for_status_code(422, "Field validation failed")
        self.assertIsInstance(validation_error, ValidationError)


class TestExceptionInheritance(unittest.TestCase):
    """Test exception inheritance hierarchy"""

    def test_all_inherit_from_base(self):
        """Test that all custom exceptions inherit from NodeMavenAPIError"""
        auth_error = AuthenticationError("test")
        rate_error = RateLimitError("test")
        validation_error = ValidationError("test")
        
        self.assertIsInstance(auth_error, NodeMavenAPIError)
        self.assertIsInstance(rate_error, NodeMavenAPIError)
        self.assertIsInstance(validation_error, NodeMavenAPIError)

    def test_all_inherit_from_exception(self):
        """Test that all custom exceptions inherit from base Exception"""
        base_error = NodeMavenAPIError("test")
        auth_error = AuthenticationError("test")
        rate_error = RateLimitError("test")
        validation_error = ValidationError("test")
        
        self.assertIsInstance(base_error, Exception)
        self.assertIsInstance(auth_error, Exception)
        self.assertIsInstance(rate_error, Exception)
        self.assertIsInstance(validation_error, Exception)


class TestExceptionAttributes(unittest.TestCase):
    """Test exception attributes and properties"""

    def test_exception_attributes_accessible(self):
        """Test that all exception attributes are accessible"""
        response_data = {"error": "test", "code": 123}
        error = NodeMavenAPIError("Test message", 400, response_data)
        
        # Test attribute access
        self.assertEqual(error.message, "Test message")
        self.assertEqual(error.status_code, 400)
        self.assertEqual(error.response_data, response_data)
        
        # Test that attributes can be modified
        error.message = "New message"
        error.status_code = 500
        self.assertEqual(error.message, "New message")
        self.assertEqual(error.status_code, 500)

    def test_exception_with_none_values(self):
        """Test exception with None values"""
        error = NodeMavenAPIError(None, None, None)
        self.assertEqual(str(error), "[None] None")
        self.assertIsNone(error.message)
        self.assertIsNone(error.status_code)
        self.assertEqual(error.response_data, {})  # Should default to empty dict

    def test_exception_serialization(self):
        """Test that exceptions can be serialized/pickled"""
        import pickle
        
        error = NodeMavenAPIError("Test error", 400, {"detail": "test"})
        
        # Should be able to pickle and unpickle
        pickled = pickle.dumps(error)
        unpickled = pickle.loads(pickled)
        
        self.assertEqual(str(error), str(unpickled))
        self.assertEqual(error.status_code, unpickled.status_code)
        self.assertEqual(error.response_data, unpickled.response_data)


def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*50)
    print(f"🧪 Exception Tests run: {result.testsRun}")
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
    print(f"\n🎯 Exception Success rate: {success_rate:.1f}%")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 