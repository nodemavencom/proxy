#!/usr/bin/env python3
"""
Example: Generate Mobile Proxy with Specific ISP and Configuration
This example shows how to generate a mobile proxy with specific requirements:
- Verizon 5G Home Internet ISP
- New York City location
- IPv4 only
- 12-hour sticky session
- Medium quality filter
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from nodemaven.utils import build_proxy_username, get_socks5_proxy

def generate_mobile_proxy_example():
    """Generate a mobile proxy with specific configuration"""
    print('📱 Mobile Proxy Generation Example')
    print('=' * 40)
    
    print('🎯 Configuration:')
    print('   • Country: US')
    print('   • Region: New York')
    print('   • City: New York City')
    print('   • ISP: Verizon 5G Home Internet')
    print('   • Type: Mobile')
    print('   • IPv4 Only: Yes')
    print('   • Session: 12-hour sticky')
    print('   • Filter: Medium quality')
    
    # Method 1: Direct username building (always works)
    print(f'\n🔧 Method 1: Direct username building')
    username = build_proxy_username(
        'alex_worldmediabuy_com',
        country='us',
        region='new york',
        city='new york city',           # Creates city-new_york_city
        isp='verizon g home internet',  # Creates isp-verizon_g_home_internet
        type='mobile',
        ipv4=True,                      # Creates ipv4-true
        sticky=True,                    # Auto-generates session ID
        ttl='12h',
        filter='medium'
    )
    
    proxy_url = f'socks5://{username}:gh9z4n0a3r@gate.nodemaven.com:1080'
    print(f'✅ Generated proxy: {proxy_url}')
    
    # Extract session ID
    if 'sid-' in username:
        session_id = username.split('sid-')[1].split('-')[0]
        print(f'🆔 Session ID: {session_id} (13 chars, random)')
    
    # Method 2: High-level API (requires API credentials)
    print(f'\n🚀 Method 2: High-level API (requires credentials)')
    try:
        api_proxy = get_socks5_proxy(
            country='us',
            region='new york',
            city='new york city',
            isp='verizon g home internet',
            type='mobile',
            ipv4=True,
            sticky=True,
            ttl='12h',
            filter='medium'
        )
        print(f'✅ API generated: {api_proxy}')
    except Exception as e:
        print(f'❌ API method requires credentials: {e}')
        print(f'   Set NODEMAVEN_APIKEY environment variable')
    
    return proxy_url

def show_usage_examples(proxy_url):
    """Show practical usage examples"""
    print(f'\n💻 Usage Examples')
    print('=' * 20)
    
    print(f'🐍 Python with requests-socks:')
    print(f'```python')
    print(f'import requests')
    print(f'from requests_socks import ProxyAdapter')
    print(f'')
    print(f'session = requests.Session()')
    print(f'proxy_url = "{proxy_url}"')
    print(f'session.mount("http://", ProxyAdapter(proxy_url))')
    print(f'session.mount("https://", ProxyAdapter(proxy_url))')
    print(f'')
    print(f'# Test the proxy')
    print(f'response = session.get("http://ip-api.com/json/")')
    print(f'data = response.json()')
    print(f'print("IP:", data["query"])')
    print(f'print("Location:", data["city"], data["regionName"])')
    print(f'print("ISP:", data["isp"])')
    print(f'```')

if __name__ == "__main__":
    print('🚀 NodeMaven Mobile Proxy Example')
    print('=' * 35)
    
    proxy_url = generate_mobile_proxy_example()
    show_usage_examples(proxy_url)
    
    print(f'\n✅ Example completed successfully!')
    print(f'📝 Modify the parameters above to create different proxy configurations.') 