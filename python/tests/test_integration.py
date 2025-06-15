"""
Integration tests for NodeMaven SDK - requires API key
These tests make real API calls and verify functionality
"""
import pytest
import os
import sys
import requests

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nodemaven import NodeMavenClient


@pytest.mark.integration
class TestClientIntegration:
    """Test real API client functionality"""
    
    def test_client_initialization(self):
        """Test client can be initialized with API key"""
        client = NodeMavenClient()
        assert client is not None
        assert client.api_key is not None
    
    def test_get_user_info(self):
        """Test getting user information from API"""
        client = NodeMavenClient()
        user_info = client.get_user_info()
        
        # Verify response structure
        assert isinstance(user_info, dict)
        assert "email" in user_info
        assert "proxy_username" in user_info
        assert "proxy_password" in user_info
        
        # Verify data types
        assert isinstance(user_info["email"], str)
        assert isinstance(user_info["proxy_username"], str)
        assert isinstance(user_info["proxy_password"], str)
    
    def test_get_countries(self):
        """Test getting available countries"""
        client = NodeMavenClient()
        countries = client.get_countries(limit=10)
        
        # Verify response structure
        assert isinstance(countries, dict)
        assert "results" in countries
        assert len(countries["results"]) > 0
        
        # Verify country structure
        country = countries["results"][0]
        assert "name" in country
        assert "code" in country
        assert isinstance(country["name"], str)
        assert isinstance(country["code"], str)


@pytest.mark.integration
class TestProxyIntegration:
    """Test proxy functionality"""
    
    def test_proxy_url_generation(self):
        """Test generating proxy URL"""
        client = NodeMavenClient()
        user_info = client.get_user_info()
        
        # Import utility function
        from nodemaven.utils import build_proxy_url
        
        # Test HTTP proxy URL
        proxy_url = build_proxy_url(protocol="http", country="us")
        assert "gate.nodemaven.com:8080" in proxy_url
        assert user_info["proxy_username"] in proxy_url
        assert user_info["proxy_password"] in proxy_url
    
    def test_proxy_connection(self):
        """Test actual proxy connection"""
        client = NodeMavenClient()
        user_info = client.get_user_info()
        
        # Import utility function
        from nodemaven.utils import build_proxy_url
        
        # Build proxy URL
        proxy_url = build_proxy_url(protocol="http", country="us")
        
        # Parse proxy for requests
        proxy_dict = {"http": proxy_url, "https": proxy_url}
        
        # Test connection (this is a basic connectivity test)
        try:
            response = requests.get(
                "http://httpbin.org/ip", 
                proxies=proxy_dict, 
                timeout=30
            )
            assert response.status_code == 200
            assert "origin" in response.json()
        except requests.exceptions.RequestException:
            # If proxy test fails, skip but don't fail the test
            pytest.skip("Proxy connection test skipped due to network issues")


@pytest.mark.integration
class TestIPChecker:
    """Test IP checking functionality"""
    
    def test_ip_checker_direct(self):
        """Test IP checker without proxy"""
        try:
            response = requests.get("http://httpbin.org/ip", timeout=10)
            assert response.status_code == 200
            data = response.json()
            assert "origin" in data
            assert isinstance(data["origin"], str)
        except requests.exceptions.RequestException:
            pytest.skip("IP checker test skipped due to network issues")
    
    def test_ip_checker_with_proxy(self):
        """Test IP checker through proxy"""
        client = NodeMavenClient()
        
        # Import utility function
        from nodemaven.utils import build_proxy_url
        
        # Build proxy URL
        proxy_url = build_proxy_url(protocol="http", country="gb")
        proxy_dict = {"http": proxy_url, "https": proxy_url}
        
        try:
            # Get IP without proxy
            direct_response = requests.get("http://httpbin.org/ip", timeout=10)
            direct_ip = direct_response.json()["origin"]
            
            # Get IP with proxy
            proxy_response = requests.get(
                "http://httpbin.org/ip", 
                proxies=proxy_dict, 
                timeout=30
            )
            proxy_ip = proxy_response.json()["origin"]
            
            # IPs should be different (proxy working)
            assert direct_ip != proxy_ip
            
        except requests.exceptions.RequestException:
            pytest.skip("Proxy IP test skipped due to network issues")


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"]) 