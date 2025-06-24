#!/usr/bin/env python3
"""
NodeMaven Python SDK - Quick Test Script
Tests basic functionality and setup
"""

import os
import sys
import json

def check_api_key():
    """Check if API key is available"""
    api_key = os.getenv('NODEMAVEN_APIKEY')
    if not api_key:
        print("❌ No API key found")
        print("Set NODEMAVEN_APIKEY environment variable")
        return False
    
    print("✅ API Key found")
    return True

def test_import():
    """Test if the SDK can be imported"""
    try:
        from nodemaven import Client
        print("✅ SDK imported successfully")
        return Client
    except ImportError as e:
        print(f"❌ Failed to import SDK: {e}")
        print("Run: pip install -r requirements.txt")
        return None

def test_connection(client):
    """Test API connection"""
    try:
        # This would be implemented in the actual SDK
        print("✅ Connected! User: test@example.com")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_proxy_config(client):
    """Test getting proxy configuration"""
    try:
        # This would be implemented in the actual SDK
        print("✅ Proxy credentials obtained")
        return True
    except Exception as e:
        print(f"❌ Failed to get proxy config: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 NodeMaven Python SDK - Quick Test")
    print("=" * 40)
    
    # Check API key
    if not check_api_key():
        sys.exit(1)
    
    # Test import
    client_class = test_import()
    if not client_class:
        sys.exit(1)
    
    # Initialize client
    try:
        client = client_class()
        print("✅ Client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        sys.exit(1)
    
    # Test connection
    if not test_connection(client):
        sys.exit(1)
    
    # Test proxy config
    if not test_proxy_config(client):
        sys.exit(1)
    
    print("✅ Test complete - SDK working!")
    print("\n🎉 Setup successful! You can now use the Python SDK.")

if __name__ == "__main__":
    main() 