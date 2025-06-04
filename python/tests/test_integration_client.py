"""
Simple test for NodeMaven client functionality
"""

def test_client_initialization():
    """Test client can be initialized"""
    print("🧪 Testing client initialization...")
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from nodemaven import NodeMavenClient
    client = NodeMavenClient()
    assert client is not None
    print("   ✅ Client initialized successfully")

def test_user_info():
    """Test getting user information"""
    print("🧪 Testing user information retrieval...")
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from nodemaven import NodeMavenClient
    client = NodeMavenClient()
    user_info = client.get_user_info()
    print(f"   📧 Email: {user_info.get('email', 'N/A')}")
    print(f"   👤 Proxy Username: {user_info.get('proxy_username', 'N/A')}")
    print(f"   💾 Data Remaining: {user_info.get('data', 'N/A')} bytes")
    assert "email" in user_info
    assert "proxy_username" in user_info
    print("   ✅ User info retrieved successfully")

def test_countries():
    """Test getting countries"""
    print("🧪 Testing countries API...")
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from nodemaven import NodeMavenClient
    client = NodeMavenClient()
    countries = client.get_countries(limit=5)
    print(f"   🌍 Retrieved {len(countries['results'])} countries:")
    for country in countries["results"][:3]:  # Show first 3
        print(f"      • {country.get('name', 'N/A')} ({country.get('code', 'N/A')})")
    if len(countries["results"]) > 3:
        print(f"      ... and {len(countries['results']) - 3} more")
    assert "results" in countries
    assert len(countries["results"]) > 0
    print("   ✅ Countries retrieved successfully")

if __name__ == "__main__":
    print("🚀 Starting NodeMaven Client Tests\n")
    test_client_initialization()
    print()
    test_user_info()
    print()
    test_countries()
    print("\n🎉 All client tests passed!") 