#!/usr/bin/env python3
"""
NodeMaven Proxy Examples - Correct Format
"""

import os
import sys

# Add the nodemaven package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nodemaven.utils import get_proxy_config, get_socks5_proxy, build_proxy_url

def main():
    print("🚀 NodeMaven Proxy Examples")
    print("=" * 60)
    
    # Check if credentials are available
    username = os.getenv('NODEMAVEN_USERNAME')
    password = os.getenv('NODEMAVEN_PASSWORD')
    
    if not username or not password:
        print("❌ Missing credentials!")
        print("   Please set NODEMAVEN_USERNAME and NODEMAVEN_PASSWORD in .env file")
        return
    
    print(f"🔑 Using username: {username}")
    print(f"🔑 Using password: {password}")
    
    print("\n📋 Proxy URL Examples:")
    print("-" * 40)
    
    # Example 1: Residential Canada with sticky session
    print("\n1️⃣ Residential Canada (sticky session):")
    socks5_url = get_socks5_proxy(country="ca", sticky=True, filter="medium")
    print(f"   SOCKS5: {socks5_url}")
    
    # Example 2: Mobile US with specific location
    print("\n2️⃣ Mobile US (Alabama, Birmingham):")
    socks5_url = get_socks5_proxy(
        country="us", 
        region="alabama", 
        city="birmingham", 
        type="mobile", 
        filter="medium"
    )
    print(f"   SOCKS5: {socks5_url}")
    
    # Example 3: HTTP proxy with custom session
    print("\n3️⃣ HTTP UK (London, custom session):")
    http_config = get_proxy_config(
        country="gb", 
        city="london", 
        session="my_session_123"
    )
    print(f"   HTTP: {http_config['http']}")
    
    # Example 4: Basic country targeting
    print("\n4️⃣ Basic Germany targeting:")
    http_config = get_proxy_config(country="de", filter="high")
    print(f"   HTTP: {http_config['http']}")
    
    # Example 5: ISP targeting
    print("\n5️⃣ Specific ISP targeting:")
    proxy_url = build_proxy_url(
        protocol="http",
        country="us",
        isp="verizon",
        filter="medium"
    )
    print(f"   HTTP: {proxy_url}")
    
    print("\n📖 Usage with requests library:")
    print("-" * 40)
    print("""
import requests
from nodemaven.utils import get_proxy_config

# Get proxy configuration
proxies = get_proxy_config(country="us", city="new_york")

# Make request through proxy
response = requests.get('https://httpbin.org/ip', proxies=proxies)
print(f"Your IP: {response.json()['origin']}")
""")
    
    print("\n📖 Usage with SOCKS5:")
    print("-" * 40)
    print("""
import requests
import socks
import socket
from nodemaven.utils import get_socks5_proxy

# Get SOCKS5 proxy URL
proxy_url = get_socks5_proxy(country="ca", session="my_session")

# Parse proxy URL for socks configuration
# proxy_url format: socks5://username:password@host:port
# You'll need to extract these components for socks.set_default_proxy()
""")
    
    print("\n🎯 Targeting Options:")
    print("-" * 40)
    print("• country: 2-letter country code (us, gb, ca, de, etc.)")
    print("• region: region/state name (california, texas, etc.)")
    print("• city: city name (new_york, london, etc.)")
    print("• isp: ISP name (verizon, comcast, etc.)")
    print("• type: connection type (mobile, residential)")
    print("• session: custom session ID for sticky sessions")
    print("• sticky: True for automatic sticky session")
    print("• filter: IP quality (low, medium, high)")
    print("• ipv4: True for IPv4 only, False for mixed")
    
    print("\n" + "=" * 60)
    print("✅ Examples completed!")

if __name__ == "__main__":
    main() 