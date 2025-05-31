#!/usr/bin/env python3
"""
NodeMaven Quick Test Script
Tests API connection and proxy functionality in 30 seconds!
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from nodemaven import NodeMavenClient
    from nodemaven.utils import get_proxy_config, get_correct_proxy_credentials
    from nodemaven.exceptions import NodeMavenAPIError
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Make sure you're in the python/ directory and have the nodemaven package")
    sys.exit(1)

def main():
    """Run quick test of NodeMaven API and proxy functionality"""
    
    print("🚀 NodeMaven Quick Test Starting...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv(dotenv_path="../.env")
    
    # Check for API key
    api_key = os.getenv("NODEMAVEN_APIKEY")
    if not api_key:
        print("❌ No API key found!")
        print("💡 Make sure NODEMAVEN_APIKEY is set in your .env file")
        return False
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    try:
        # Test 1: Initialize client and get user info
        print("\n📡 Testing API Connection...")
        client = NodeMavenClient()
        user_info = client.get_user_info()
        print(f"✅ Connected! User: {user_info.get('username', 'Unknown')}")
        
        # Test 2: Get proxy credentials
        print("\n🔑 Getting Proxy Credentials...")
        username, password = get_correct_proxy_credentials()
        
        if username and password:
            print(f"✅ Proxy credentials obtained!")
            print(f"   Username: {username}")
            print(f"   Password: {password[:8]}...")
        else:
            print("❌ Could not get proxy credentials")
            print("💡 Check if your account has proxy access enabled")
            return False
        
        # Test 3: Test proxy connection
        print("\n🌐 Testing Proxy Connection...")
        
        # Get proxy configuration
        proxy_config = get_proxy_config(country="US")
        print(f"✅ Proxy config created: {list(proxy_config.keys())}")
        
        # Test the proxy with a simple request
        test_url = "https://httpbin.org/ip"
        print(f"📡 Making request to {test_url}...")
        
        response = requests.get(
            test_url, 
            proxies=proxy_config,
            timeout=30
        )
        
        if response.status_code == 200:
            ip_info = response.json()
            print(f"✅ Proxy working! Your IP: {ip_info.get('origin', 'Unknown')}")
        else:
            print(f"❌ Proxy request failed with status: {response.status_code}")
            return False
            
        # Test 4: Test different country
        print("\n🌍 Testing Geo-targeting (UK)...")
        uk_proxy_config = get_proxy_config(country="GB")
        
        response = requests.get(
            test_url,
            proxies=uk_proxy_config,
            timeout=30
        )
        
        if response.status_code == 200:
            ip_info = response.json()
            print(f"✅ UK Proxy working! IP: {ip_info.get('origin', 'Unknown')}")
        else:
            print(f"⚠️  UK proxy test failed with status: {response.status_code}")
        
        # Test 5: Show account info
        print("\n📊 Account Information:")
        if 'traffic_used' in user_info:
            from nodemaven.utils import format_bytes
            traffic_used = user_info.get('traffic_used', 0)
            traffic_limit = user_info.get('traffic_limit', 0)
            print(f"   Traffic Used: {format_bytes(traffic_used)}")
            if traffic_limit > 0:
                print(f"   Traffic Limit: {format_bytes(traffic_limit)}")
                remaining = traffic_limit - traffic_used
                print(f"   Remaining: {format_bytes(remaining)}")
        
        print("\n" + "=" * 50)
        print("🎉 Quick Test Complete!")
        print("✅ Your NodeMaven setup is working perfectly!")
        print("\n📚 Next Steps:")
        print("   • Run: python examples/basic_usage.py")
        print("   • Run: python examples/proxy_rotation.py")
        print("   • Check: python examples/README.md")
        print("\n🔗 Resources:")
        print("   • Dashboard: https://dashboard.nodemaven.com")
        print("   • API Docs: https://dashboard.nodemaven.com/documentation")
        print("   • Support: https://t.me/node_maven")
        
        return True
        
    except NodeMavenAPIError as e:
        print(f"❌ NodeMaven API Error: {e}")
        if hasattr(e, 'status_code'):
            if e.status_code == 401:
                print("💡 Your API key may be invalid or expired")
            elif e.status_code == 403:
                print("💡 Your account may not have proxy access enabled")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
        print("💡 Check your internet connection and try again")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 