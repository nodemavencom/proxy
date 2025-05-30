#!/usr/bin/env python3
"""
Proxy rotation example for NodeMaven API client.

This example shows how to:
1. Rotate IP addresses for each request
2. Use sticky sessions
3. Target different geographical locations
4. Handle rate limiting and errors
"""

import os
import sys
import time
import random
import requests
from dotenv import load_dotenv

# Add parent directory to path to import nodemaven
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nodemaven import NodeMavenClient, NodeMavenAPIError
from nodemaven.utils import get_proxy_config, build_proxy_url

# Load environment variables
load_dotenv()


class ProxyRotator:
    """Helper class for managing proxy rotation."""
    
    def __init__(self, client: NodeMavenClient):
        self.client = client
        self.user_info = client.get_user_info()
        self.session_counter = 0
        self.rotation_countries = ['us', 'ca', 'gb', 'de', 'fr']
        
    def get_rotating_proxy(self) -> dict:
        """Get a proxy configuration that rotates IP for each request."""
        # Use random country for rotation
        country = random.choice(self.rotation_countries)
        return get_proxy_config(country=country, filter="medium")
    
    def get_sticky_proxy(self, session_id: str = None) -> dict:
        """Get a proxy configuration with sticky session."""
        if not session_id:
            self.session_counter += 1
            session_id = f"session_{self.session_counter}_{int(time.time())}"
        
        return get_proxy_config(session=session_id, filter="medium")
    
    def get_geo_targeted_proxy(self, country: str = None, region: str = None, city: str = None) -> dict:
        """Get a geo-targeted proxy configuration."""
        targeting = {"filter": "medium"}
        if country:
            targeting['country'] = country
        if region:
            targeting['region'] = region
        if city:
            targeting['city'] = city
        
        return get_proxy_config(**targeting)


def test_ip_rotation(rotator: ProxyRotator, num_requests: int = 5):
    """Test IP rotation by making multiple requests."""
    print(f"\n🔄 Testing IP rotation ({num_requests} requests)...")
    
    ips_seen = set()
    
    for i in range(num_requests):
        try:
            proxies = rotator.get_rotating_proxy()
            response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
            
            if response.status_code == 200:
                ip_data = response.json()
                ip = ip_data['origin']
                ips_seen.add(ip)
                print(f"   Request {i+1}: {ip} {'(NEW)' if ip not in ips_seen else '(SEEN)'}")
            else:
                print(f"   Request {i+1}: Failed with status {response.status_code}")
        
        except requests.RequestException as e:
            print(f"   Request {i+1}: Error - {e}")
        except ValueError as e:
            print(f"   Request {i+1}: Configuration error - {e}")
            break
        except Exception as e:
            print(f"   Request {i+1}: Unexpected error - {e}")
        
        # Add delay between requests
        if i < num_requests - 1:
            time.sleep(2)
    
    print(f"   📊 Total unique IPs seen: {len(ips_seen)}")


def test_sticky_session(rotator: ProxyRotator, num_requests: int = 3):
    """Test sticky session (same IP for multiple requests)."""
    print(f"\n📌 Testing sticky session ({num_requests} requests)...")
    
    session_id = f"test_{int(time.time())}"
    ips_seen = set()
    
    for i in range(num_requests):
        try:
            proxies = rotator.get_sticky_proxy(session_id)
            response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
            
            if response.status_code == 200:
                ip_data = response.json()
                ip = ip_data['origin']
                ips_seen.add(ip)
                print(f"   Request {i+1}: {ip}")
            else:
                print(f"   Request {i+1}: Failed with status {response.status_code}")
        
        except requests.RequestException as e:
            print(f"   Request {i+1}: Error - {e}")
        except ValueError as e:
            print(f"   Request {i+1}: Configuration error - {e}")
            break
        except Exception as e:
            print(f"   Request {i+1}: Unexpected error - {e}")
        
        # Add delay between requests
        if i < num_requests - 1:
            time.sleep(2)
    
    if len(ips_seen) == 1:
        print(f"   ✅ Sticky session working! All requests used same IP: {list(ips_seen)[0]}")
    else:
        print(f"   ❌ Sticky session failed. Saw {len(ips_seen)} different IPs: {ips_seen}")


def test_geo_targeting(rotator: ProxyRotator):
    """Test geo-targeting functionality."""
    print("\n🌍 Testing geo-targeting...")
    
    # Test different countries
    countries_to_test = ["US", "CA", "GB", "DE", "FR"]
    
    for country in countries_to_test:
        try:
            proxies = rotator.get_geo_targeted_proxy(country=country)
            response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=15)
            
            if response.status_code == 200:
                ip_data = response.json()
                ip = ip_data['origin']
                print(f"   {country}: {ip}")
                
                # Optional: Check IP geolocation (if you have a geolocation service)
                # You could add a call to ipapi.com or similar service here
                
            else:
                print(f"   {country}: Failed with status {response.status_code}")
        
        except requests.RequestException as e:
            print(f"   {country}: Error - {e}")
        except ValueError as e:
            print(f"   {country}: Configuration error - {e}")
            break
        except Exception as e:
            print(f"   {country}: Unexpected error - {e}")
        
        # Add delay between requests
        time.sleep(3)


def test_parallel_sessions(rotator: ProxyRotator):
    """Test multiple parallel sticky sessions."""
    print("\n🔀 Testing parallel sticky sessions...")
    
    sessions = {}
    num_sessions = 3
    requests_per_session = 2
    
    for session_num in range(num_sessions):
        session_id = f"parallel_{session_num}_{int(time.time())}"
        sessions[session_id] = []
        
        print(f"\n   Session {session_num + 1} ({session_id}):")
        
        for req_num in range(requests_per_session):
            try:
                proxies = rotator.get_sticky_proxy(session_id)
                response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
                
                if response.status_code == 200:
                    ip_data = response.json()
                    ip = ip_data['origin']
                    sessions[session_id].append(ip)
                    print(f"     Request {req_num + 1}: {ip}")
                else:
                    print(f"     Request {req_num + 1}: Failed with status {response.status_code}")
            
            except requests.RequestException as e:
                print(f"     Request {req_num + 1}: Error - {e}")
            except ValueError as e:
                print(f"     Request {req_num + 1}: Configuration error - {e}")
                break
            except Exception as e:
                print(f"     Request {req_num + 1}: Unexpected error - {e}")
            
            time.sleep(2)  # Increased delay to avoid 503 errors
    
    # Verify each session used the same IP
    print("\n   📊 Session analysis:")
    for session_id, ips in sessions.items():
        unique_ips = set(ips)
        if len(unique_ips) == 1 and len(ips) > 0:
            print(f"     ✅ {session_id}: Consistent IP {list(unique_ips)[0]}")
        else:
            print(f"     ❌ {session_id}: Inconsistent IPs {unique_ips}")


def main():
    """Main example function."""
    print("🔄 NodeMaven Proxy Rotation Example")
    print("=" * 60)
    
    try:
        # Initialize client and rotator
        client = NodeMavenClient()
        rotator = ProxyRotator(client)
        
        print("✅ Proxy rotator initialized")
        print(f"   👤 Username: {rotator.user_info['proxy_username']}")
        print(f"   📊 Data remaining: {rotator.user_info['data']:,} bytes")
        
        # Run rotation tests
        test_ip_rotation(rotator, num_requests=5)
        test_sticky_session(rotator, num_requests=3)
        test_geo_targeting(rotator)
        test_parallel_sessions(rotator)
        
    except NodeMavenAPIError as e:
        print(f"❌ NodeMaven API Error: {e}")
        if e.status_code == 403:
            print("   💡 Tip: Check if your API key is valid and not expired")
        elif e.status_code == 429:
            print("   💡 Tip: You've hit the rate limit, please wait before trying again")
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("   💡 Tip: Make sure you have NODEMAVEN_APIKEY, NODEMAVEN_USERNAME, and NODEMAVEN_PASSWORD set in your .env file")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Proxy rotation example completed!")


if __name__ == "__main__":
    main() 