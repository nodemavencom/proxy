#!/usr/bin/env python3
"""
Simple IP Checker for NodeMaven Proxy Testing
Uses multiple free APIs to verify proxy functionality and get IP details.
"""

import requests
import json
import sys
import time
from typing import Dict, Any, Optional

class SimpleIPChecker:
    def __init__(self):
        self.timeout = 10
        
    def check_ip(self, ip_address: str = None) -> Dict[str, Any]:
        """
        Check IP address details using multiple free APIs
        If no IP provided, checks the current public IP
        """
        
        if not ip_address:
            # Get current public IP
            ip_address = self._get_current_ip()
            if not ip_address:
                return {"error": "Could not determine IP address"}
        
        print(f"🔍 Checking IP: {ip_address}")
        
        # Get data from multiple sources
        results = {
            "ip": ip_address,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        # Source 1: ip-api.com (free, no key needed)
        ipapi_data = self._check_ipapi(ip_address)
        if ipapi_data:
            results.update(ipapi_data)
        
        # Source 2: ipinfo.io (free tier, no key needed)
        ipinfo_data = self._check_ipinfo(ip_address)
        if ipinfo_data:
            results["ipinfo"] = ipinfo_data
        
        # Source 3: ipgeolocation.io (free tier)
        ipgeo_data = self._check_ipgeolocation(ip_address)
        if ipgeo_data:
            results["ipgeolocation"] = ipgeo_data
        
        return results
    
    def _get_current_ip(self) -> Optional[str]:
        """Get current public IP address"""
        endpoints = [
            "https://api.ipify.org",
            "https://icanhazip.com",
            "https://ipinfo.io/ip",
            "https://api.myip.com"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=5)
                if response.status_code == 200:
                    if endpoint == "https://api.myip.com":
                        return response.json().get("ip")
                    else:
                        return response.text.strip()
            except:
                continue
        
        return None
    
    def _check_ipapi(self, ip: str) -> Dict[str, Any]:
        """Check IP using ip-api.com (free, comprehensive)"""
        try:
            url = f"http://ip-api.com/json/{ip}?fields=66846719"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return {
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
        except Exception as e:
            print(f"❌ ip-api.com error: {e}")
        
        return {}
    
    def _check_ipinfo(self, ip: str) -> Dict[str, Any]:
        """Check IP using ipinfo.io (free tier)"""
        try:
            url = f"https://ipinfo.io/{ip}/json"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "city": data.get("city"),
                    "region": data.get("region"),
                    "country": data.get("country"),
                    "location": data.get("loc"),
                    "org": data.get("org"),
                    "postal": data.get("postal"),
                    "timezone": data.get("timezone")
                }
        except Exception as e:
            print(f"❌ ipinfo.io error: {e}")
        
        return {}
    
    def _check_ipgeolocation(self, ip: str) -> Dict[str, Any]:
        """Check IP using ipgeolocation.io (free tier)"""
        try:
            url = f"https://api.ipgeolocation.io/ipgeo?apiKey=&ip={ip}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "country_name": data.get("country_name"),
                    "state_prov": data.get("state_prov"),
                    "city": data.get("city"),
                    "isp": data.get("isp"),
                    "connection_type": data.get("connection_type"),
                    "organization": data.get("organization")
                }
        except Exception as e:
            print(f"❌ ipgeolocation.io error: {e}")
        
        return {}
    
    def format_results(self, results: Dict[str, Any]) -> str:
        """Format results in a readable way"""
        if "error" in results:
            return f"❌ Error: {results['error']}"
        
        output = []
        output.append(f"🌐 IP Address: {results.get('ip', 'Unknown')}")
        output.append(f"📅 Checked: {results.get('timestamp', 'Unknown')}")
        output.append("")
        
        # Location info
        country = results.get('country', 'Unknown')
        city = results.get('city', 'Unknown')
        region = results.get('region', 'Unknown')
        
        output.append("📍 Location:")
        output.append(f"   Country: {country}")
        output.append(f"   Region: {region}")
        output.append(f"   City: {city}")
        
        # ISP info
        isp = results.get('isp', 'Unknown')
        org = results.get('org', 'Unknown')
        as_info = results.get('as', 'Unknown')
        
        output.append("")
        output.append("🏢 Network:")
        output.append(f"   ISP: {isp}")
        output.append(f"   Organization: {org}")
        output.append(f"   AS: {as_info}")
        
        # Proxy detection
        is_proxy = results.get('proxy', False)
        is_hosting = results.get('hosting', False)
        is_mobile = results.get('mobile', False)
        
        output.append("")
        output.append("🔍 Detection:")
        output.append(f"   Proxy: {'✅ Yes' if is_proxy else '❌ No'}")
        output.append(f"   Hosting: {'✅ Yes' if is_hosting else '❌ No'}")
        output.append(f"   Mobile: {'✅ Yes' if is_mobile else '❌ No'}")
        
        # Additional info from other sources
        if "ipinfo" in results:
            ipinfo = results["ipinfo"]
            if ipinfo.get("org"):
                output.append(f"   IPInfo Org: {ipinfo['org']}")
        
        if "ipgeolocation" in results:
            ipgeo = results["ipgeolocation"]
            if ipgeo.get("connection_type"):
                output.append(f"   Connection Type: {ipgeo['connection_type']}")
        
        return "\n".join(output)

def main():
    """Main function for command line usage"""
    checker = SimpleIPChecker()
    
    # Check if IP was provided as argument
    if len(sys.argv) > 1:
        ip_to_check = sys.argv[1]
        print(f"🎯 Checking provided IP: {ip_to_check}")
    else:
        ip_to_check = None
        print("🎯 Checking current public IP...")
    
    # Perform the check
    results = checker.check_ip(ip_to_check)
    
    # Display results
    print("\n" + "="*50)
    print(checker.format_results(results))
    print("="*50)
    
    # Also save as JSON for programmatic use
    with open("last_ip_check.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: last_ip_check.json")

if __name__ == "__main__":
    main() 