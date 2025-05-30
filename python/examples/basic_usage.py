#!/usr/bin/env python3
"""
Basic usage example for NodeMaven API client.

This example shows how to:
1. Initialize the client
2. Get user information
3. List available countries
4. Use proxies for web requests
"""

import os
import sys

# Add parent directory to path to import nodemaven
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nodemaven import NodeMavenClient, NodeMavenAPIError
from nodemaven.utils import get_proxy_config, build_proxy_url

# Try to load environment variables if dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("💡 Note: python-dotenv not available, using system environment variables")

# Try to import requests
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    print("❌ Warning: requests module not available, proxy tests will be skipped")
    REQUESTS_AVAILABLE = False


def main():
    """Main example function."""
    print("🚀 NodeMaven Basic Usage Example")
    print("=" * 50)
    
    try:
        # Initialize client (will use NODEMAVEN_APIKEY from .env)
        client = NodeMavenClient()
        print("✅ Client initialized successfully")
        
        # Get user information
        print("\n📊 Getting user information...")
        user_info = client.get_user_info()
        
        print(f"   📧 Email: {user_info['email']}")
        print(f"   👤 Proxy Username: {user_info['proxy_username']}")
        print(f"   🔑 Proxy Password: {user_info['proxy_password']}")
        print(f"   📈 Data Remaining: {user_info['data']:,} bytes")
        print(f"   🎯 Subscription: {user_info['subscription_status']}")
        
        # List available countries
        print("\n🌍 Getting available countries...")
        countries = client.get_countries(limit=10)
        
        print(f"   Found {len(countries['results'])} countries (showing first 10):")
        for country in countries['results']:
            print(f"   - {country['name']} ({country['code']})")
        
        # Example: Get regions for United States
        print("\n🏞️  Getting regions for United States...")
        us_regions = client.get_regions(country_code="US", limit=5)
        
        if us_regions['results']:
            print(f"   Found {len(us_regions['results'])} regions (showing first 5):")
            for region in us_regions['results']:
                print(f"   - {region['name']} ({region['code']})")
        
        if not REQUESTS_AVAILABLE:
            print("\n⚠️  Skipping proxy tests - requests module not available")
            print("   Install with: pip install requests")
            return
        
        # Example: Basic proxy usage using environment variables
        print("\n🔌 Testing basic proxy usage...")
        
        try:
            # Use utility function to get proxy config
            proxies = get_proxy_config()
            
            # Test IP check
            response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
            if response.status_code == 200:
                ip_data = response.json()
                print(f"   ✅ Proxy working! Your IP: {ip_data['origin']}")
            else:
                print(f"   ❌ Proxy test failed with status: {response.status_code}")
        except ValueError as e:
            print(f"   ❌ Proxy configuration error: {e}")
            print("   💡 Tip: Set NODEMAVEN_USERNAME and NODEMAVEN_PASSWORD in your .env file")
        except requests.RequestException as e:
            print(f"   ❌ Proxy test failed: {e}")
        
        # Example: Geo-targeted proxy
        print("\n🎯 Testing geo-targeted proxy (US)...")
        
        try:
            # Build geo-targeted proxy (targeting US)
            geo_proxies = get_proxy_config(country="US")
            
            response = requests.get('https://httpbin.org/ip', proxies=geo_proxies, timeout=10)
            if response.status_code == 200:
                ip_data = response.json()
                print(f"   ✅ Geo-targeted proxy working! US IP: {ip_data['origin']}")
            else:
                print(f"   ❌ Geo-targeted proxy test failed with status: {response.status_code}")
        except ValueError as e:
            print(f"   ❌ Geo-targeted proxy configuration error: {e}")
        except requests.RequestException as e:
            print(f"   ❌ Geo-targeted proxy test failed: {e}")
        
        # Example: Sticky session
        print("\n📌 Testing sticky session...")
        
        try:
            # Build sticky session proxy
            sticky_proxies = get_proxy_config(session="example_session_123")
            
            # Make multiple requests with same session
            ips = []
            for i in range(3):
                response = requests.get('https://httpbin.org/ip', proxies=sticky_proxies, timeout=10)
                if response.status_code == 200:
                    ip_data = response.json()
                    ips.append(ip_data['origin'])
                    print(f"   Request {i+1}: {ip_data['origin']}")
            
            if len(set(ips)) == 1:
                print(f"   ✅ Sticky session working! All requests used same IP")
            else:
                print(f"   ⚠️  Sticky session may not be working - got {len(set(ips))} different IPs")
                
        except ValueError as e:
            print(f"   ❌ Sticky session configuration error: {e}")
        except requests.RequestException as e:
            print(f"   ❌ Sticky session test failed: {e}")
        
    except NodeMavenAPIError as e:
        print(f"❌ NodeMaven API Error: {e}")
        if e.status_code == 403:
            print("   💡 Tip: Check if your API key is valid and not expired")
        elif e.status_code == 429:
            print("   💡 Tip: You've hit the rate limit, please wait before trying again")
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("   💡 Tip: Make sure you have NODEMAVEN_APIKEY set in your .env file")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Example completed!")


if __name__ == "__main__":
    main() 