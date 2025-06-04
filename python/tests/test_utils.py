"""
Simple test for utility functions
"""

def test_proxy_config():
    """Test proxy configuration generation"""
    print("🧪 Testing proxy configuration generation...")
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from nodemaven.utils import get_proxy_config
    proxies = get_proxy_config(country="us")
    print(f"   🌐 HTTP Proxy: {proxies.get('http', 'N/A')}")
    print(f"   🔒 HTTPS Proxy: {proxies.get('https', 'N/A')}")
    assert "http" in proxies
    assert "https" in proxies
    print("   ✅ Proxy configuration generated successfully")

def test_socks5_proxy():
    """Test SOCKS5 proxy URL generation"""
    print("🧪 Testing SOCKS5 proxy URL generation...")
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from nodemaven.utils import get_socks5_proxy
    proxy_url = get_socks5_proxy(country="us")
    print(f"   🔧 SOCKS5 URL: {proxy_url}")
    assert proxy_url.startswith("socks5://")
    print("   ✅ SOCKS5 proxy URL generated successfully")

def test_session_id_generation():
    """Test session ID generation"""
    print("🧪 Testing session ID generation...")
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from nodemaven.utils import generate_session_id
    session_id = generate_session_id()
    print(f"   🆔 Generated Session ID: {session_id}")
    print(f"   📏 Length: {len(session_id)} characters")
    print(f"   🔤 Alphanumeric: {session_id.isalnum()}")
    assert len(session_id) == 13
    assert session_id.isalnum()
    print("   ✅ Session ID generated successfully")

if __name__ == "__main__":
    print("🚀 Starting Utility Function Tests\n")
    test_proxy_config()
    print()
    test_socks5_proxy() 
    print()
    test_session_id_generation()
    print("\n🎉 All utility tests passed!") 