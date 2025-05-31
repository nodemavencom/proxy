#!/usr/bin/env python3
"""
Comprehensive proxy examples for NodeMaven.
Shows various proxy configurations and usage patterns.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from nodemaven.utils import get_proxy_config, get_socks5_proxy, get_current_ip
    from nodemaven.client import NodeMavenClient
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Make sure you're in the python/ directory and have the nodemaven package")
    sys.exit(1)

# Try to load environment variables if dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def main():
    """Show comprehensive proxy examples."""
    print("🚀 NodeMaven Proxy Examples")
    print("=" * 60)
    
    # Get API key info
    try:
        from nodemaven.utils import get_api_key
        api_key = get_api_key()
        if api_key:
            print(f"🔑 Using API key: {api_key[:20]}...")
            print("💡 Proxy credentials will be fetched automatically from API")
        else:
            print("❌ No API key found. Please set NODEMAVEN_APIKEY in your .env file")
            return
    except Exception as e:
        print(f"❌ Error getting API key: {e}")
        return
    
    print("\n📋 Proxy Configuration Examples:")
    print("-" * 40)
    
    # Example 1: Basic US targeting
    print("\n1️⃣ Basic US targeting:")
    try:
        us_config = get_proxy_config(country="US")
        proxy_url = us_config['http']
        # Mask credentials in display
        masked_url = proxy_url.replace(proxy_url.split('@')[0].split(':')[-1], '...')
        print(f"   HTTP: {masked_url}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Example 2: UK London targeting
    print("\n2️⃣ UK London targeting:")
    try:
        london_config = get_proxy_config(country="GB", city="london")
        proxy_url = london_config['http']
        masked_url = proxy_url.replace(proxy_url.split('@')[0].split(':')[-1], '...')
        print(f"   HTTP: {masked_url}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Example 3: Sticky session
    print("\n3️⃣ Sticky session (same IP for multiple requests):")
    try:
        sticky_config = get_proxy_config(country="US", session="my_session_123")
        proxy_url = sticky_config['http']
        masked_url = proxy_url.replace(proxy_url.split('@')[0].split(':')[-1], '...')
        print(f"   HTTP: {masked_url}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Example 4: SOCKS5 proxy
    print("\n4️⃣ SOCKS5 proxy (Canada):")
    try:
        socks5_url = get_socks5_proxy(country="CA")
        masked_url = socks5_url.replace(socks5_url.split('@')[0].split(':')[-1], '...')
        print(f"   SOCKS5: {masked_url}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Example 5: Mobile proxy
    print("\n5️⃣ Mobile proxy (US):")
    try:
        mobile_config = get_proxy_config(country="US", type="mobile")
        proxy_url = mobile_config['http']
        masked_url = proxy_url.replace(proxy_url.split('@')[0].split(':')[-1], '...')
        print(f"   HTTP: {masked_url}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Example 6: Regional targeting
    print("\n6️⃣ Regional targeting (California):")
    try:
        ca_config = get_proxy_config(country="US", region="california")
        proxy_url = ca_config['http']
        masked_url = proxy_url.replace(proxy_url.split('@')[0].split(':')[-1], '...')
        print(f"   HTTP: {masked_url}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Usage examples
    print("\n📖 Usage with requests library:")
    print("-" * 40)
    print("""
import requests
from nodemaven.utils import get_proxy_config, get_current_ip

# Get proxy configuration (credentials fetched automatically)
proxies = get_proxy_config(country="US", city="new_york")

# Make request through proxy
ip = get_current_ip(proxies=proxies)
print(f"Your IP: {ip}")

# Different country
uk_proxies = get_proxy_config(country="GB")
uk_ip = get_current_ip(proxies=uk_proxies)
print(f"UK IP: {uk_ip}")
""")
    
    print("\n📖 Sticky Sessions Example:")
    print("-" * 40)
    print("""
import requests
from nodemaven.utils import get_proxy_config, get_current_ip

# Same session ID = same IP for all requests
session_proxies = get_proxy_config(session="my_session_123")

for i in range(3):
    ip = get_current_ip(proxies=session_proxies)
    print(f"Request {i+1}: {ip}")  # Same IP each time!
""")
    
    print("\n📖 IP Rotation Example:")
    print("-" * 40)
    print("""
import requests
from nodemaven.utils import get_proxy_config, get_current_ip

# No session ID = different IP for each request
for i in range(3):
    proxies = get_proxy_config(country="US")  # New proxy each time
    ip = get_current_ip(proxies=proxies)
    print(f"Request {i+1}: {ip}")  # Different IPs
""")
    
    print("\n📖 SOCKS5 Usage:")
    print("-" * 40)
    print("""
import requests
from nodemaven.utils import get_socks5_proxy, get_current_ip

# Get SOCKS5 proxy URL
socks5_url = get_socks5_proxy(country="CA", session="my_session")

# Use with requests (requires requests[socks])
proxies = {
    'http': socks5_url,
    'https': socks5_url
}
ip = get_current_ip(proxies=proxies)
print(f"Your IP: {ip}")
""")
    
    print("\n🎯 Targeting Options:")
    print("-" * 40)
    print("• country: 2-letter country code (US, GB, CA, DE, etc.)")
    print("• region: region/state name (california, texas, etc.)")
    print("• city: city name (new_york, london, etc.)")
    print("• isp: ISP name (verizon, comcast, etc.)")
    print("• type: connection type (mobile, residential)")
    print("• session: custom session ID for sticky sessions")
    print("• filter: IP quality (low, medium, high)")
    print("• ipv4: True for IPv4 only, False for mixed")
    
    print("\n🌍 Popular Country Codes:")
    print("-" * 40)
    print("• US - United States    • GB - United Kingdom")
    print("• CA - Canada          • DE - Germany")
    print("• FR - France          • AU - Australia")
    print("• JP - Japan           • BR - Brazil")
    print("• IN - India           • IT - Italy")
    
    print("\n💡 Pro Tips:")
    print("-" * 40)
    print("• Use sticky sessions for multi-step workflows")
    print("• Use IP rotation for large-scale data collection")
    print("• Use mobile proxies for mobile app testing")
    print("• Use city targeting for location-specific content")
    print("• Use our get_current_ip() function for reliable IP checking")
    
    print("\n" + "=" * 60)
    print("✅ Examples completed!")

if __name__ == "__main__":
    main() 