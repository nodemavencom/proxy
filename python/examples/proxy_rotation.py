#!/usr/bin/env python3
"""
Advanced proxy rotation examples for NodeMaven.
Demonstrates IP rotation, sticky sessions, geo-targeting, and parallel sessions.
"""

import os
import sys
import time
from typing import List, Dict, Set

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from nodemaven.client import NodeMavenClient
    from nodemaven.utils import get_proxy_config, format_bytes, get_current_ip, generate_session_id
    from nodemaven.exceptions import NodeMavenAPIError
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Make sure you're in the python/ directory and have the nodemaven package")
    sys.exit(1)


class ProxyRotator:
    """Helper class for managing proxy rotation and testing."""
    
    def __init__(self):
        self.client = NodeMavenClient()
        self.user_info = self.client.get_user_info()
        
    def get_user_info(self) -> Dict:
        """Get user information."""
        return self.user_info
        
    def test_ip_rotation(self, num_requests: int = 5, **targeting) -> List[str]:
        """Test IP rotation by making multiple requests."""
        ips = []
        unique_ips = set()
        
        for i in range(num_requests):
            try:
                # Get new proxy config for each request (no session = rotation)
                proxy_config = get_proxy_config(**targeting)
                ip = get_current_ip(proxies=proxy_config, timeout=10)
                
                if ip:
                    ips.append(ip)
                    is_new = ip not in unique_ips
                    unique_ips.add(ip)
                    status = "NEW" if is_new else "REPEAT"
                    print(f"   Request {i+1}: {ip} ({status})")
                else:
                    print(f"   Request {i+1}: Failed to get IP")
                    
            except Exception as e:
                print(f"   Request {i+1}: Error - {e}")
                
        return ips
    
    def test_sticky_session(self, session_id: str, num_requests: int = 3, **targeting) -> List[str]:
        """Test sticky session by making multiple requests with same session."""
        ips = []
        
        for i in range(num_requests):
            try:
                # Use same session ID for all requests
                proxy_config = get_proxy_config(session=session_id, **targeting)
                ip = get_current_ip(proxies=proxy_config, timeout=10)
                
                if ip:
                    ips.append(ip)
                    print(f"   Request {i+1}: {ip}")
                else:
                    print(f"   Request {i+1}: Failed to get IP")
                    
            except Exception as e:
                print(f"   Request {i+1}: Error - {e}")
                
        return ips
    
    def test_geo_targeting(self, countries: List[str]) -> Dict[str, str]:
        """Test geo-targeting across multiple countries."""
        results = {}
        
        for country in countries:
            try:
                proxy_config = get_proxy_config(country=country)
                ip = get_current_ip(proxies=proxy_config, timeout=10)
                
                if ip:
                    results[country] = ip
                    print(f"   {country}: {ip}")
                else:
                    print(f"   {country}: Failed to get IP")
                    
            except Exception as e:
                print(f"   {country}: Error - {e}")
                
        return results
    
    def test_parallel_sessions(self, num_sessions: int = 3, requests_per_session: int = 2) -> Dict[str, List[str]]:
        """Test multiple parallel sticky sessions."""
        results = {}
        
        for i in range(num_sessions):
            session_id = f"parallel_{i}_{int(time.time())}"
            print(f"\n   Session {i+1} ({session_id}):")
            
            session_ips = []
            for j in range(requests_per_session):
                try:
                    proxy_config = get_proxy_config(session=session_id, country="US")
                    ip = get_current_ip(proxies=proxy_config, timeout=10)
                    
                    if ip:
                        session_ips.append(ip)
                        print(f"     Request {j+1}: {ip}")
                    else:
                        print(f"     Request {j+1}: Failed to get IP")
                        
                except Exception as e:
                    print(f"     Request {j+1}: Error - {e}")
                    
            results[session_id] = session_ips
            
        return results


def main():
    """Demonstrate advanced proxy rotation features."""
    print("🔄 NodeMaven Proxy Rotation Example")
    print("=" * 60)
    
    try:
        # Initialize rotator
        rotator = ProxyRotator()
        print("✅ Proxy rotator initialized")
        
        # Show user info
        user_info = rotator.get_user_info()
        username = user_info.get('proxy_username', 'Unknown')
        traffic_used = user_info.get('traffic_used', 0)
        traffic_limit = user_info.get('traffic_limit', 0)
        
        if traffic_limit > 0:
            remaining = max(0, traffic_limit - traffic_used)
            print(f"   👤 Username: {username}")
            print(f"   📊 Data remaining: {format_bytes(remaining)}")
        
        # Test 1: IP Rotation
        print("\n🔄 Testing IP rotation (5 requests)...")
        rotation_ips = rotator.test_ip_rotation(5, country="US")
        unique_rotation_ips = set(rotation_ips)
        print(f"   📊 Total unique IPs seen: {len(unique_rotation_ips)}")
        
        # Test 2: Sticky Session
        print("\n📌 Testing sticky session (3 requests)...")
        session_id = f"demo_session_{int(time.time())}"
        sticky_ips = rotator.test_sticky_session(session_id, 3, country="US")
        
        if sticky_ips:
            unique_sticky_ips = set(sticky_ips)
            if len(unique_sticky_ips) == 1:
                print(f"   ✅ Sticky session working! All requests used same IP: {sticky_ips[0]}")
            else:
                print(f"   ⚠️  Sticky session inconsistent - got {len(unique_sticky_ips)} different IPs")
        
        # Test 3: Geo-targeting
        print("\n🌍 Testing geo-targeting...")
        countries = ["US", "CA", "GB", "DE", "FR"]
        geo_results = rotator.test_geo_targeting(countries)
        
        # Test 4: Parallel sticky sessions
        print("\n🔀 Testing parallel sticky sessions...")
        parallel_results = rotator.test_parallel_sessions(3, 2)
        
        # Analyze parallel session results
        print("\n   📊 Session analysis:")
        for session_id, ips in parallel_results.items():
            if ips:
                unique_ips = set(ips)
                if len(unique_ips) == 1:
                    print(f"     ✅ {session_id}: Consistent IP {ips[0]}")
                else:
                    print(f"     ⚠️  {session_id}: Inconsistent - {len(unique_ips)} different IPs")
            else:
                print(f"     ❌ {session_id}: No successful requests")
        
        print("\n" + "=" * 60)
        print("🎉 Proxy rotation example completed!")
        
    except NodeMavenAPIError as e:
        print(f"❌ NodeMaven API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    main() 