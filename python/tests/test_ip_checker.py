"""
Simple test for IP checker functionality
"""

def test_ipapi_checker():
    """Test IP-API checker"""
    print("🧪 Testing IP-API checker...")
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from ip_checker.ipapi_checker import check_ip
    result = check_ip("8.8.8.8")
    print(f"   🌐 Service: {result.get('service', 'N/A')}")
    print(f"   📍 IP: {result.get('ip', 'N/A')}")
    print(f"   🏳️ Country: {result.get('country', 'N/A')}")
    print(f"   🏙️ City: {result.get('city', 'N/A')}")
    assert result.get("success") == True
    assert result.get("service") == "ip-api.com"
    print("   ✅ IP-API checker working correctly")

def test_ipinfo_checker():
    """Test IPInfo checker"""
    print("🧪 Testing IPInfo checker...")
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from ip_checker.ipinfo_checker import check_ip
    result = check_ip("8.8.8.8")
    print(f"   🌐 Service: {result.get('service', 'N/A')}")
    print(f"   📍 IP: {result.get('ip', 'N/A')}")
    print(f"   🏳️ Country: {result.get('country', 'N/A')}")
    print(f"   🏙️ City: {result.get('city', 'N/A')}")
    assert result.get("success") == True
    assert result.get("service") == "ipinfo.io"
    print("   ✅ IPInfo checker working correctly")

def test_enhanced_ip_checker():
    """Test enhanced IP checker"""
    print("🧪 Testing Enhanced IP checker...")
    import importlib.util
    import os
    
    spec = importlib.util.spec_from_file_location("ip_checker_module", 
                                                  os.path.join(os.path.dirname(__file__), "..", "ip_checker.py"))
    ip_checker_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ip_checker_module)
    
    checker = ip_checker_module.EnhancedIPChecker()
    result = checker.check_ip("8.8.8.8")
    print(f"   📍 IP: {result.get('ip', 'N/A')}")
    print(f"   🏳️ Country: {result.get('country', 'N/A')}")
    print(f"   🏙️ City: {result.get('city', 'N/A')}")
    print(f"   🔧 Services Used: {', '.join(result.get('services_used', []))}")
    print(f"   🛡️ Proxy Detection: {result.get('proxy', 'N/A')}")
    assert "ip" in result
    assert "services_used" in result
    print("   ✅ Enhanced IP checker working correctly")

if __name__ == "__main__":
    print("🚀 Starting IP Checker Tests\n")
    test_ipapi_checker()
    print()
    test_ipinfo_checker()
    print()
    test_enhanced_ip_checker()
    print("\n🎉 All IP checker tests passed!") 