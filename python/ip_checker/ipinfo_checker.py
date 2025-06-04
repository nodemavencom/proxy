#!/usr/bin/env python3
"""
Simple IPInfo.io checker
Returns clean JSON data for IP geolocation
"""

import requests
import json
import sys
from typing import Dict, Any, Optional

def check_ip(ip: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Check IP using ipinfo.io (free tier)
    Returns clean JSON data or error info
    """
    try:
        url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "service": "ipinfo.io",
                "ip": ip,
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country"),
                "location": data.get("loc"),
                "org": data.get("org"),
                "postal": data.get("postal"),
                "timezone": data.get("timezone"),
                "hostname": data.get("hostname"),
                "phone": data.get("phone")
            }
        else:
            return {
                "success": False,
                "service": "ipinfo.io",
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "service": "ipinfo.io",
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