#!/usr/bin/env python3
"""
Quick test script for NodeMaven proxy functionality.
Tests API connection, proxy credentials, and basic proxy functionality.
"""

import os
import sys

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from nodemaven.client import NodeMavenClient
    from nodemaven.utils import get_proxy_config, format_bytes, get_current_ip
    from nodemaven.exceptions import NodeMavenAPIError
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Make sure you're in the python/ directory and have the nodemaven package")
    sys.exit(1)


def test_proxy_connection(description: str, proxy_config: dict) -> bool:
    """Test proxy connection and return success status."""
    try:
        # Test proxy connection using our IP checker
        proxy_ip = get_current_ip(proxies=proxy_config, timeout=15)
        
        if proxy_ip:
            print(f"✅ {description} working! IP: {proxy_ip}")
            return True
        else:
            print(f"❌ {description} failed to get IP")
            return False
            
    except Exception as e:
        print(f"❌ {description} error: {str(e)[:50]}...")
        return False


def main():
    """Main test function."""
    print("🚀 NodeMaven Quick Test Starting...")
    print("=" * 50)
    
    try:
        # Check for API key
        from nodemaven.utils import get_api_key
        api_key = get_api_key()
        
        if not api_key:
            print("❌ No API key found!")
            print("💡 Make sure NODEMAVEN_APIKEY is set in your .env file")
            return
        
        print(f"✅ API Key found: {api_key[:20]}...")
        
        # Test API connection
        print("\n📡 Testing API Connection...")
        client = NodeMavenClient()
        user_info = client.get_user_info()
        
        user_display = user_info.get('email', 'Unknown')
        print(f"✅ Connected! User: {user_display}")
        
        # Get proxy credentials
        print("\n🔑 Getting Proxy Credentials...")
        username = user_info.get('proxy_username')
        password = user_info.get('proxy_password')
        
        if username and password:
            print(f"✅ Proxy credentials obtained!")
            print(f"   Username: {username}")
            print(f"   Password: {password[:8]}...")
        else:
            print("❌ Could not get proxy credentials")
            print("💡 Check if your account has proxy access enabled")
            return
        
        # Test basic proxy connection
        print("\n🌐 Testing Proxy Connection...")
        proxy_config = get_proxy_config(country="US")
        
        if proxy_config:
            print(f"✅ Proxy config created: {list(proxy_config.keys())}")
            
            # Test US proxy
            success = test_proxy_connection("US Proxy", proxy_config)
            
            if not success:
                print("❌ Proxy connection test failed")
                print("💡 This could be due to:")
                print("   • Network connectivity issues")
                print("   • Proxy server temporary issues")
                print("   • Account limitations")
                return
            
            # Test geo-targeting with UK
            print("\n🌍 Testing Geo-targeting (UK)...")
            uk_proxy_config = get_proxy_config(country="GB")
            uk_success = test_proxy_connection("UK Proxy", uk_proxy_config)
            
            if not uk_success:
                print("⚠️  UK proxy test failed, but US proxy worked")
        
        # Show account information
        print("\n📊 Account Information:")
        
        traffic_used = user_info.get('traffic_used', 0)
        traffic_limit = user_info.get('traffic_limit', 0)
        
        if traffic_used and traffic_limit:
            print(f"   Traffic Used: {format_bytes(traffic_used)}")
            print(f"   Traffic Limit: {format_bytes(traffic_limit)}")
            remaining = max(0, traffic_limit - traffic_used)
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
        
    except NodeMavenAPIError as e:
        print(f"❌ NodeMaven API Error: {e}")
        
        if "401" in str(e) or "403" in str(e):
            print("💡 Your API key may be invalid or expired")
        elif "account" in str(e).lower():
            print("💡 Your account may not have proxy access enabled")
        
    except Exception as e:
        if "requests" in str(e).lower() or "connection" in str(e).lower():
            print(f"❌ Network Error: {e}")
            print("💡 Check your internet connection and try again")
        else:
            print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    main() 