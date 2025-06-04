#!/usr/bin/env python3
"""
Simple IP-API.com checker
Returns clean JSON data for IP geolocation
"""

import requests
import json
import sys
from typing import Dict, Any, Optional

def check_ip(ip: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Check IP using ip-api.com (free, comprehensive)
    Returns clean JSON data or error info
    """
    try:
        url = f"http://ip-api.com/json/{ip}?fields=66846719"
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "success": True,
                    "service": "ip-api.com",
                    "ip": ip,
                    "country": data.get("country"),
                    "country_code": data.get("countryCode"),
                    "region": data.get("regionName"),
                    "city": data.get("city"),
                    "zip": data.get("zip"),
                    "lat": data.get("lat"),
                    "lon": data.get("lon"),
                    "timezone": data.get("timezone"),
                    "isp": data.get("isp"),
                    "org": data.get("org"),
                    "as": data.get("as"),
                    "proxy": data.get("proxy", False),
                    "hosting": data.get("hosting", False),
                    "mobile": data.get("mobile", False)
                }
            else:
                return {
                    "success": False,
                    "service": "ip-api.com",
                    "error": data.get("message", "Query failed")
                }
        else:
            return {
                "success": False,
                "service": "ip-api.com",
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "service": "ip-api.com",
            "error": str(e)
        }

def get_current_ip() -> Optional[str]:
    """Get current public IP address"""
    endpoints = [
        "https://api.ipify.org",
        "https://icanhazip.com",
        "https://ipinfo.io/ip"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=5)
            if response.status_code == 200:
                return response.text.strip()
        except:
            continue
    
    return None

def main():
    """Command line interface"""
    if len(sys.argv) > 1:
        ip_to_check = sys.argv[1]
    else:
        ip_to_check = get_current_ip()
        if not ip_to_check:
            print(json.dumps({"success": False, "error": "Could not determine IP address"}))
            return
    
    result = check_ip(ip_to_check)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main() 