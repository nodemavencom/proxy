#!/usr/bin/env python3
"""
Example usage of all IP checker scripts
Demonstrates how to use each service and compare results
"""

import json
from ipapi_checker import check_ip as check_ipapi
from ipinfo_checker import check_ip as check_ipinfo

def check_ip_all_services(ip: str):
    """
    Check IP using all available services
    Returns a dictionary with results from each service
    """
    results = {
        "ip": ip,
        "services": {}
    }
    
    # Check with IP-API (free, no key)
    print(f"Checking {ip} with IP-API...")
    ipapi_result = check_ipapi(ip)
    results["services"]["ipapi"] = ipapi_result
    
    # Check with IPInfo (free, no key) 
    print(f"Checking {ip} with IPInfo...")
    ipinfo_result = check_ipinfo(ip)
    results["services"]["ipinfo"] = ipinfo_result
    
    return results

def main():
    """Example usage"""
    # Test IP (Google DNS)
    test_ip = "8.8.8.8"
    
    print(f"=== IP Checker Example ===")
    print(f"Testing IP: {test_ip}")
    print()
    
    # Check with all services
    results = check_ip_all_services(test_ip)
    
    print("\n=== Results ===")
    print(json.dumps(results, indent=2))
    
    # Show a summary comparison
    print("\n=== Summary Comparison ===")
    services = results["services"]
    
    for service_name, data in services.items():
        if data.get("success"):
            country = data.get("country") or data.get("country_name", "Unknown")
            city = data.get("city", "Unknown")  
            isp = data.get("isp", "Unknown")
            print(f"{service_name:12}: {country}, {city} | ISP: {isp}")
        else:
            print(f"{service_name:12}: ERROR - {data.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main() 