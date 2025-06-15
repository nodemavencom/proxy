#!/usr/bin/env python3
"""
NodeMaven CLI Tools

Command-line interface for NodeMaven Python SDK.
Provides easy access to common operations like testing connectivity,
checking IP, and listing available countries.
"""

import argparse
import json
import sys
from typing import Optional, Dict, Any

from . import NodeMavenClient
from .utils import get_current_ip, build_proxy_url

# Import IP checkers
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ip_checker import check_ip_ipapi, check_ip_ipinfo


def print_json(data: Dict[str, Any], indent: int = 2) -> None:
    """Pretty print JSON data."""
    print(json.dumps(data, indent=indent, ensure_ascii=False))


def main() -> None:
    """Main CLI entry point for general testing."""
    parser = argparse.ArgumentParser(
        description="NodeMaven Python SDK - Test your proxy connection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nodemaven-test                    # Test API connectivity
  nodemaven-test --country us       # Test US proxy
  nodemaven-test --country gb --city london  # Test London proxy
  nodemaven-test --mobile           # Test mobile proxy
  nodemaven-test --socks5           # Test SOCKS5 proxy
        """
    )
    
    parser.add_argument(
        "--country", "-c",
        help="Country code for proxy (e.g., us, gb, ca)"
    )
    parser.add_argument(
        "--region", "-r",
        help="Region/state for proxy (e.g., california, london)"
    )
    parser.add_argument(
        "--city",
        help="City for proxy (e.g., los_angeles, new_york)"
    )
    parser.add_argument(
        "--mobile", "-m",
        action="store_true",
        help="Use mobile proxy"
    )
    parser.add_argument(
        "--socks5", "-s",
        action="store_true",
        help="Use SOCKS5 protocol (default: HTTP)"
    )
    parser.add_argument(
        "--session",
        help="Session ID for sticky sessions"
    )
    parser.add_argument(
        "--ttl",
        help="Time-to-live for session (e.g., 1h, 30m, 60s)"
    )
    parser.add_argument(
        "--filter",
        choices=["low", "medium", "high"],
        help="Quality filter"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Quiet mode - less output"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize client
        if not args.quiet:
            print("🔍 Initializing NodeMaven client...")
        
        client = NodeMavenClient()
        
        # Test API connectivity
        if not args.quiet:
            print("🌐 Testing API connectivity...")
        
        user_info = client.get_user_info()
        
        if not args.quiet:
            print(f"✅ Connected! User: {user_info['email']}")
            print(f"✅ Proxy Username: {user_info.get('proxy_username', 'N/A')}")
        
        # Build proxy configuration
        proxy_config = {}
        if args.country:
            proxy_config['country'] = args.country
        if args.region:
            proxy_config['region'] = args.region  
        if args.city:
            proxy_config['city'] = args.city
        if args.mobile:
            proxy_config['type'] = 'mobile'
        if args.session:
            proxy_config['session'] = args.session
        if args.ttl:
            proxy_config['ttl'] = args.ttl
        if args.filter:
            proxy_config['filter'] = args.filter
            
        # Test proxy if configuration provided
        if proxy_config:
            protocol = 'socks5' if args.socks5 else 'http'
            
            if not args.quiet:
                config_str = ', '.join([f"{k}={v}" for k, v in proxy_config.items()])
                print(f"🔧 Testing {protocol.upper()} proxy with: {config_str}")
            
            proxy_url = build_proxy_url(protocol=protocol, **proxy_config)
            
            if not args.quiet:
                print(f"🌍 Testing proxy connection...")
            
            # Test the proxy
            import requests
            proxies = {'http': proxy_url, 'https': proxy_url}
            
            try:
                response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=30)
                if response.status_code == 200:
                    ip_data = response.json()
                    if not args.quiet:
                        print(f"✅ Proxy working! IP: {ip_data['origin']}")
                        print(f"✅ Proxy URL: {proxy_url}")
                    else:
                        print(ip_data['origin'])
                else:
                    print(f"❌ Proxy test failed with status: {response.status_code}")
                    sys.exit(1)
            except Exception as e:
                print(f"❌ Proxy connection failed: {e}")
                sys.exit(1)
        else:
            if not args.quiet:
                print("ℹ️  API test complete. Use --country to test proxy connections.")
            else:
                print("OK")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def check_ip() -> None:
    """CLI tool for checking IP information."""
    parser = argparse.ArgumentParser(
        description="Check IP address geolocation information",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nodemaven-ip                    # Check your current IP
  nodemaven-ip 8.8.8.8           # Check specific IP
  nodemaven-ip --service ipinfo   # Use specific service
        """
    )
    
    parser.add_argument(
        "ip",
        nargs="?",
        help="IP address to check (default: your current IP)"
    )
    parser.add_argument(
        "--service", "-s",
        choices=["ipapi", "ipinfo", "both"],
        default="both",
        help="Which service to use"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output raw JSON"
    )
    
    args = parser.parse_args()
    
    try:
        # Get IP to check
        if args.ip:
            target_ip = args.ip
        else:
            print("🔍 Getting your current IP...")
            target_ip = get_current_ip()
            if not target_ip:
                print("❌ Could not determine your current IP")
                sys.exit(1)
        
        print(f"🌍 Checking IP: {target_ip}")
        
        # Check with requested services
        if args.service in ["ipapi", "both"]:
            print("\n📍 IP-API.com results:")
            try:
                ipapi_data = check_ip_ipapi(target_ip)
                if args.json:
                    print_json(ipapi_data)
                else:
                    print(f"  Country: {ipapi_data.get('country', 'N/A')}")
                    print(f"  Region: {ipapi_data.get('regionName', 'N/A')}")
                    print(f"  City: {ipapi_data.get('city', 'N/A')}")
                    print(f"  ISP: {ipapi_data.get('isp', 'N/A')}")
                    print(f"  Organization: {ipapi_data.get('org', 'N/A')}")
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        if args.service in ["ipinfo", "both"]:
            print("\n📍 IPInfo.io results:")
            try:
                ipinfo_data = check_ip_ipinfo(target_ip)
                if args.json:
                    print_json(ipinfo_data)
                else:
                    print(f"  Country: {ipinfo_data.get('country', 'N/A')}")
                    print(f"  Region: {ipinfo_data.get('region', 'N/A')}")
                    print(f"  City: {ipinfo_data.get('city', 'N/A')}")
                    print(f"  Organization: {ipinfo_data.get('org', 'N/A')}")
                    print(f"  Location: {ipinfo_data.get('loc', 'N/A')}")
            except Exception as e:
                print(f"  ❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def list_countries() -> None:
    """CLI tool for listing available countries."""
    parser = argparse.ArgumentParser(
        description="List available countries for NodeMaven proxies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nodemaven-countries              # List all countries
  nodemaven-countries --limit 10   # List first 10 countries
  nodemaven-countries --json       # Output as JSON
        """
    )
    
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=50,
        help="Maximum number of countries to show (default: 50)"
    )
    parser.add_argument(
        "--offset", "-o", 
        type=int,
        default=0,
        help="Number of countries to skip (default: 0)"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output raw JSON"
    )
    
    args = parser.parse_args()
    
    try:
        print("🔍 Fetching available countries...")
        
        client = NodeMavenClient()
        countries_data = client.get_countries(limit=args.limit, offset=args.offset)
        
        if args.json:
            print_json(countries_data)
        else:
            countries = countries_data.get('results', [])
            total = countries_data.get('count', len(countries))
            
            print(f"\n🌍 Available Countries ({len(countries)} of {total}):")
            print("=" * 50)
            
            for country in countries:
                code = country.get('code', 'N/A')
                name = country.get('name', 'N/A')
                print(f"  {code.upper():3} - {name}")
            
            if len(countries) < total:
                remaining = total - len(countries) - args.offset
                print(f"\n... and {remaining} more countries available")
                print("Use --limit and --offset to see more")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 