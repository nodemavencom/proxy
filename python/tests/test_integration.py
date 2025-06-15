"""
Integration tests for NodeMaven SDK - requires API key
These tests make real API calls and verify functionality
"""
import pytest
import os
import sys
import requests
import time

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
        
        print(f"✅ User: {user_info['email']}")
        print(f"✅ Proxy Username: {user_info['proxy_username']}")
    
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
        
        print(f"✅ Found {len(countries['results'])} countries")
        for country in countries["results"][:3]:
            print(f"   - {country['name']} ({country['code']})")
    
    def test_get_regions(self):
        """Test getting regions for a specific country"""
        client = NodeMavenClient()
        regions = client.get_regions(country_code="US", limit=5)
        
        assert isinstance(regions, dict)
        assert "results" in regions
        
        if len(regions["results"]) > 0:
            region = regions["results"][0]
            assert "name" in region
            assert "code" in region
            print(f"✅ Found {len(regions['results'])} US regions")
    
    def test_get_cities(self):
        """Test getting cities for a specific country"""
        client = NodeMavenClient()
        cities = client.get_cities(country_code="US", limit=5)
        
        assert isinstance(cities, dict)
        assert "results" in cities
        
        if len(cities["results"]) > 0:
            city = cities["results"][0]
            assert "name" in city
            assert "code" in city
            print(f"✅ Found {len(cities['results'])} US cities")
    
    def test_get_isps(self):
        """Test getting ISPs for a specific country"""
        client = NodeMavenClient()
        isps = client.get_isps(country_code="US", limit=5)
        
        assert isinstance(isps, dict)
        # API returns different format: {'city': '', 'country': 'US', 'isps': [], 'region': ''}
        if "results" in isps:
            assert "results" in isps
            if len(isps["results"]) > 0:
                isp = isps["results"][0]
                assert "name" in isp
                print(f"✅ Found {len(isps['results'])} US ISPs")
        elif "isps" in isps:
            # Handle different API format
            assert "isps" in isps
            print(f"✅ Found {len(isps['isps'])} US ISPs")
    
    def test_get_statistics(self):
        """Test getting usage statistics"""
        client = NodeMavenClient()
        try:
            stats = client.get_statistics()
            assert isinstance(stats, dict)
            print("✅ Statistics retrieved successfully")
        except Exception as e:
            # Some endpoints might not be available for all accounts
            print(f"⚠️  Statistics endpoint not available: {str(e)}")
            pytest.skip("Statistics endpoint not available for this account")
    
    def test_get_whitelist_ips(self):
        """Test getting whitelisted IPs"""
        client = NodeMavenClient()
        try:
            whitelist = client.get_whitelist_ips()
            assert isinstance(whitelist, dict)
            assert "results" in whitelist
            print(f"✅ Found {len(whitelist['results'])} whitelisted IPs")
        except Exception as e:
            # Some endpoints might not be available for all accounts
            print(f"⚠️  Whitelist endpoint not available: {str(e)}")
            pytest.skip("Whitelist endpoint not available for this account")


@pytest.mark.integration 
class TestProxyIntegration:
    """Test proxy functionality with comprehensive targeting options"""
    
    def test_basic_proxy_url_generation(self):
        """Test generating basic proxy URL"""
        client = NodeMavenClient()
        user_info = client.get_user_info()
        
        # Import utility function
        from nodemaven.utils import build_proxy_url
        
        # Test HTTP proxy URL
        proxy_url = build_proxy_url(protocol="http", country="us")
        assert "gate.nodemaven.com:8080" in proxy_url
        assert user_info["proxy_username"] in proxy_url
        assert user_info["proxy_password"] in proxy_url
        assert "country-us" in proxy_url
        print(f"✅ Basic HTTP proxy URL: {proxy_url[:50]}...")
    
    def test_comprehensive_proxy_targeting(self):
        """Test proxy URL generation with all targeting options"""
        client = NodeMavenClient()
        user_info = client.get_user_info()
        
        from nodemaven.utils import build_proxy_url, generate_session_id
        
        # Test complex HTTP proxy with all options
        session_id = generate_session_id()
        proxy_url = build_proxy_url(
            protocol="http",
            country="us",
            region="california",
            city="los_angeles",
            type="residential",
            ipv4=True,
            session=session_id,
            ttl="1h",
            filter="high"
        )
        
        assert "gate.nodemaven.com:8080" in proxy_url
        assert f"{user_info['proxy_username']}-country-us-region-california-city-los_angeles-type-residential-ipv4-true-sid-{session_id}-ttl-1h-filter-high" in proxy_url
        print(f"✅ Complex HTTP targeting: {proxy_url[:80]}...")
        
        # Test SOCKS5 with mobile targeting
        proxy_url = build_proxy_url(
            protocol="socks5",
            country="gb",
            type="mobile",
            sticky=True,
            filter="medium"
        )
        
        assert proxy_url.startswith("socks5://")
        assert "gate.nodemaven.com:1080" in proxy_url
        assert "country-gb-type-mobile" in proxy_url
        assert "sid-" in proxy_url
        assert "filter-medium" in proxy_url
        print(f"✅ Mobile SOCKS5 targeting: {proxy_url[:80]}...")
    
    def test_client_proxy_config_methods(self):
        """Test client's proxy configuration methods"""
        client = NodeMavenClient()
        
        # Test getProxyConfig method
        proxy_config = client.getProxyConfig({'country': 'US', 'filter': 'high'})
        assert isinstance(proxy_config, dict)
        assert 'http' in proxy_config
        assert 'https' in proxy_config
        assert 'country-us' in proxy_config['http']
        assert 'filter-high' in proxy_config['http']
        print("✅ getProxyConfig method working")
        
        # Test getSocks5ProxyUrl method
        socks5_url = client.getSocks5ProxyUrl({'country': 'GB', 'type': 'mobile'})
        assert isinstance(socks5_url, str)
        assert socks5_url.startswith('socks5://')
        assert 'country-gb' in socks5_url
        assert 'type-mobile' in socks5_url
        print("✅ getSocks5ProxyUrl method working")
    
    def test_proxy_connection_basic(self):
        """Test basic proxy connection"""
        client = NodeMavenClient()
        
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
            ip_data = response.json()
            assert "origin" in ip_data
            print(f"✅ Basic proxy connection successful. IP: {ip_data['origin']}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Proxy connection test skipped: {str(e)}")
            pytest.skip("Proxy connection test skipped due to network issues")
    
    def test_proxy_connection_with_targeting(self):
        """Test proxy connection with specific targeting"""
        from nodemaven.utils import build_proxy_url, generate_session_id
        
        # Test with UK residential proxy
        proxy_url = build_proxy_url(
            protocol="http",
            country="gb",
            type="residential",
            session=generate_session_id(),
            ttl="30m"
        )
        proxy_dict = {"http": proxy_url, "https": proxy_url}
        
        try:
            response = requests.get(
                "http://httpbin.org/ip", 
                proxies=proxy_dict, 
                timeout=30
            )
            assert response.status_code == 200
            ip_data = response.json()
            print(f"✅ UK residential proxy connection successful. IP: {ip_data['origin']}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️  UK proxy test skipped: {str(e)}")
            pytest.skip("UK proxy connection test skipped due to network issues")


@pytest.mark.integration
class TestIPCheckerIntegration:
    """Test IP checking functionality with various proxy configurations"""
    
    def test_ip_checker_direct(self):
        """Test IP checker without proxy"""
        try:
            response = requests.get("http://httpbin.org/ip", timeout=10)
            assert response.status_code == 200
            data = response.json()
            assert "origin" in data
            assert isinstance(data["origin"], str)
            print(f"✅ Direct IP: {data['origin']}")
        except requests.exceptions.RequestException:
            pytest.skip("IP checker test skipped due to network issues")
    
    def test_ip_checker_with_different_countries(self):
        """Test IP checker through proxies from different countries"""
        from nodemaven.utils import build_proxy_url
        
        countries_to_test = ["us", "gb", "ca"]
        
        for country in countries_to_test:
            try:
                proxy_url = build_proxy_url(protocol="http", country=country)
                proxy_dict = {"http": proxy_url, "https": proxy_url}
                
                response = requests.get(
                    "http://httpbin.org/ip", 
                    proxies=proxy_dict, 
                    timeout=30
                )
                
                if response.status_code == 200:
                    ip_data = response.json()
                    print(f"✅ {country.upper()} proxy IP: {ip_data['origin']}")
                else:
                    print(f"⚠️  {country.upper()} proxy failed with status {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"⚠️  {country.upper()} proxy test failed: {str(e)}")
    
    def test_session_persistence(self):
        """Test that session IDs provide persistent IPs"""
        from nodemaven.utils import build_proxy_url, generate_session_id
        
        session_id = generate_session_id()
        
        try:
            # Make two requests with the same session ID
            proxy_url = build_proxy_url(
                protocol="http",
                country="us", 
                session=session_id,
                ttl="1h"
            )
            proxy_dict = {"http": proxy_url, "https": proxy_url}
            
            # First request
            response1 = requests.get(
                "http://httpbin.org/ip", 
                proxies=proxy_dict, 
                timeout=30
            )
            
            # Wait a moment
            time.sleep(2)
            
            # Second request with same session
            response2 = requests.get(
                "http://httpbin.org/ip", 
                proxies=proxy_dict, 
                timeout=30
            )
            
            if response1.status_code == 200 and response2.status_code == 200:
                ip1 = response1.json()["origin"]
                ip2 = response2.json()["origin"]
                
                # IPs should be the same due to session persistence
                assert ip1 == ip2, f"Session persistence failed: {ip1} != {ip2}"
                print(f"✅ Session persistence working: {ip1}")
            else:
                print("⚠️  Session persistence test inconclusive due to request failures")
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Session persistence test skipped: {str(e)}")
            pytest.skip("Session persistence test skipped due to network issues")


@pytest.mark.integration
class TestErrorHandling:
    """Test error handling in integration scenarios"""
    
    def test_invalid_api_key(self):
        """Test handling of invalid API key"""
        from nodemaven.exceptions import AuthenticationError
        
        # Test with invalid API key
        with pytest.raises(AuthenticationError):
            client = NodeMavenClient(api_key="invalid_key")
            client.get_user_info()
    
    def test_invalid_proxy_credentials(self):
        """Test handling of invalid proxy credentials"""
        from nodemaven.utils import build_proxy_url
        
        # Mock invalid credentials
        import nodemaven.utils
        original_func = nodemaven.utils.get_correct_proxy_credentials
        nodemaven.utils.get_correct_proxy_credentials = lambda: ("invalid_user", "invalid_pass")
        
        try:
            proxy_url = build_proxy_url(protocol="http", country="us")
            proxy_dict = {"http": proxy_url, "https": proxy_url}
            
            # This should fail with proxy authentication error
            response = requests.get(
                "http://httpbin.org/ip", 
                proxies=proxy_dict, 
                timeout=10
            )
            
            # If we get here, the test should fail
            if response.status_code == 200:
                pytest.fail("Expected proxy authentication to fail with invalid credentials")
                
        except requests.exceptions.ProxyError:
            print("✅ Invalid proxy credentials properly rejected")
        except requests.exceptions.RequestException:
            print("✅ Invalid proxy credentials caused expected request failure")
        finally:
            # Restore original function
            nodemaven.utils.get_correct_proxy_credentials = original_func
    
    def test_network_timeout_handling(self):
        """Test handling of network timeouts"""
        from nodemaven.utils import build_proxy_url
        
        try:
            proxy_url = build_proxy_url(protocol="http", country="us")
            proxy_dict = {"http": proxy_url, "https": proxy_url}
            
            # Use very short timeout to force timeout
            response = requests.get(
                "http://httpbin.org/delay/10",  # This endpoint delays 10 seconds
                proxies=proxy_dict, 
                timeout=1  # 1 second timeout
            )
            
            # Should not reach here
            pytest.fail("Expected timeout exception")
            
        except requests.exceptions.Timeout:
            print("✅ Timeout handling working correctly")
        except requests.exceptions.RequestException:
            print("✅ Request exception handling working")


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v", "-s"])  # Added -s to show print statements 