#!/usr/bin/env python3
"""
Basic usage examples for NodeMaven proxy API.
Demonstrates core functionality including user info, countries, and proxy usage.
"""

import os
import sys
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from nodemaven.client import NodeMavenClient
    from nodemaven.utils import get_proxy_config, format_bytes, get_current_ip
    from nodemaven.exceptions import NodeMavenAPIError
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Make sure you're in the python/ directory and have the nodemaven package")
    sys.exit(1)


def test_proxy_connection(description: str, proxy_config: dict) -> Optional[str]:
    """Test proxy connection and return IP address."""
    try:
        # Use our IP checking function
        ip = get_current_ip(proxies=proxy_config, timeout=15)
        if ip:
            print(f"   ✅ {description} working! Your IP: {ip}")
            return ip
        else:
            print(f"   ❌ {description} failed to get IP")
            return None
    except Exception as e:
        print(f"   ❌ {description} error: {e}")
        return None


def main():
    """Demonstrate basic NodeMaven usage."""
    print("🚀 NodeMaven Basic Usage Example")
    print("=" * 50)
    
    try:
        # Initialize client
        client = NodeMavenClient()
        print("✅ Client initialized successfully")
        
        # Get user information
        print("\n📊 Getting user information...")
        user_info = client.get_user_info()
        
        print(f"   📧 Email: {user_info.get('email', 'Unknown')}")
        print(f"   👤 Proxy Username: {user_info.get('proxy_username', 'Unknown')}")
        print(f"   🔑 Proxy Password: {user_info.get('proxy_password', 'Unknown')[:8]}...")
        
        # Show data usage
        traffic_used = user_info.get('traffic_used', 0)
        traffic_limit = user_info.get('traffic_limit', 0)
        if traffic_limit > 0:
            remaining = max(0, traffic_limit - traffic_used)
            print(f"   📈 Data Remaining: {format_bytes(remaining)}")
        
        subscription = user_info.get('subscription_type') or user_info.get('subscription')
        print(f"   🎯 Subscription: {subscription}")
        
        # Get available countries
        print("\n🌍 Getting available countries...")
        countries = client.get_countries(limit=10)
        
        if countries.get('results'):
            print(f"   Found {len(countries['results'])} countries (showing first 10):")
            for country in countries['results'][:10]:
                print(f"   - {country.get('name', 'Unknown')} ({country.get('code', 'Unknown')})")
        
        # Get regions for a specific country (US)
        print("\n🏞️  Getting regions for United States...")
        try:
            regions = client.get_regions(country_code="US", limit=5)
            if regions.get('results'):
                print(f"   Found {len(regions['results'])} regions")
        except Exception as e:
            print(f"   ⚠️  Could not get regions: {e}")
        
        # Test basic proxy usage
        print("\n🔌 Testing basic proxy usage...")
        basic_proxies = get_proxy_config()
        test_proxy_connection("Basic proxy", basic_proxies)
        
        # Test geo-targeted proxy
        print("\n🎯 Testing geo-targeted proxy (US)...")
        us_proxies = get_proxy_config(country="US")
        test_proxy_connection("US geo-targeted proxy", us_proxies)
        
        # Test sticky session
        print("\n📌 Testing sticky session...")
        session_id = "example_session_123"
        session_proxies = get_proxy_config(country="US", session=session_id)
        
        # Make multiple requests with same session
        ips = []
        for i in range(3):
            ip = get_current_ip(proxies=session_proxies, timeout=10)
            if ip:
                print(f"   ✅ Sticky session request {i+1} working! Your IP: {ip}")
                ips.append(ip)
            else:
                print(f"   ❌ Sticky session request {i+1} failed")
        
        # Check if all IPs are the same (sticky session working)
        if len(set(ips)) == 1 and ips:
            print(f"   ✅ Sticky session working! All requests used same IP: {ips[0]}")
        elif ips:
            print(f"   ⚠️  Sticky session may not be working - got {len(set(ips))} different IPs")
        
        print("\n" + "=" * 50)
        print("🎉 Example completed!")
        
    except NodeMavenAPIError as e:
        print(f"❌ NodeMaven API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    main() 