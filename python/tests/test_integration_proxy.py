"""
Simple test for proxy functionality
"""

def test_proxy_request():
    """Test actual proxy request"""
    print("🧪 Testing actual proxy request...")
    import requests
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from nodemaven.utils import get_proxy_config
    
    proxies = get_proxy_config(country="us")
    print(f"   🔧 Using proxy: {proxies['http']}")
    print("   🌐 Making request to httpbin.org/ip...")
    
    response = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=10)
    assert response.status_code == 200
    
    ip_data = response.json()
    print(f"   📍 Response IP: {ip_data.get('origin', 'N/A')}")
    print(f"   ✅ Status Code: {response.status_code}")
    
    assert "origin" in ip_data
    print("   ✅ Proxy request completed successfully")

def test_proxy_authentication():
    """Test proxy authentication"""
    print("🧪 Testing proxy authentication...")
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from nodemaven.utils import get_correct_proxy_credentials
    username, password = get_correct_proxy_credentials()
    print(f"   👤 Username: {username}")
    print(f"   🔐 Password: {'*' * len(password) if password else 'None'}")
    assert username is not None
    assert password is not None
    print("   ✅ Proxy credentials retrieved successfully")

def test_proxy_targeting():
    """Test proxy geo-targeting"""
    print("🧪 Testing proxy geo-targeting...")
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from nodemaven.utils import get_proxy_config
    
    us_proxies = get_proxy_config(country="us")
    uk_proxies = get_proxy_config(country="gb")
    
    print("   🇺🇸 US Proxy Config:")
    print(f"      HTTP: {us_proxies['http']}")
    print("   🇬🇧 UK Proxy Config:")
    print(f"      HTTP: {uk_proxies['http']}")
    
    assert us_proxies != uk_proxies
    print("   ✅ Geo-targeting working correctly (different configs generated)")

if __name__ == "__main__":
    print("🚀 Starting Proxy Functionality Tests\n")
    test_proxy_authentication()
    print()
    test_proxy_targeting()
    print()
    test_proxy_request()  # This one last as it makes network call
    print("\n🎉 All proxy functionality tests passed!") 