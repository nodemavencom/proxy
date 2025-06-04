#!/usr/bin/env python3
"""
Enhanced IP Checker for NodeMaven Proxy Testing
Uses multiple free APIs and merges reliable data for comprehensive IP analysis.
"""

import json
import sys
import time
import os
from typing import Dict, Any, Optional

# Import our clean checker modules
try:
    from ip_checker.ipapi_checker import check_ip as check_ipapi, get_current_ip
    from ip_checker.ipinfo_checker import check_ip as check_ipinfo
except ImportError:
    print("Error: Could not import ip_checker modules. Make sure ip_checker folder is available.")
    sys.exit(1)

class EnhancedIPChecker:
    def __init__(self):
        self.timeout = 10
        
    def check_ip(self, ip_address: str = None) -> Dict[str, Any]:
        """
        Check IP address using multiple services and merge reliable data
        If no IP provided, checks the current public IP
        """
        
        if not ip_address:
            ip_address = get_current_ip()
            if not ip_address:
                return {"error": "Could not determine IP address"}
        
        print(f"Checking IP: {ip_address}")
        
        # Get data from both services
        ipapi_result = check_ipapi(ip_address)
        ipinfo_result = check_ipinfo(ip_address)
        
        # Check if at least one service succeeded
        if not ipapi_result.get("success") and not ipinfo_result.get("success"):
            return {
                "error": "All IP checking services failed",
                "ipapi_error": ipapi_result.get("error", "Unknown"),
                "ipinfo_error": ipinfo_result.get("error", "Unknown")
            }
        
        # Merge data intelligently, preferring data that exists in both services
        merged_data = self._merge_service_data(ip_address, ipapi_result, ipinfo_result)
        
        return merged_data
    
    def _merge_service_data(self, ip: str, ipapi_data: Dict[str, Any], ipinfo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge data from both services, keeping only reliable and consistent information
        """
        result = {
            "ip": ip,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "services_used": []
        }
        
        # Track which services provided data
        if ipapi_data.get("success"):
            result["services_used"].append("ip-api.com")
        if ipinfo_data.get("success"):
            result["services_used"].append("ipinfo.io")
        
        # Core location data - prefer data that exists in both services
        # Country
        ipapi_country = ipapi_data.get("country") if ipapi_data.get("success") else None
        ipinfo_country = ipinfo_data.get("country") if ipinfo_data.get("success") else None
        if ipapi_country:
            result["country"] = ipapi_country
            result["country_code"] = ipapi_data.get("country_code")
        
        # City - prefer ipapi as it's more reliable for this
        ipapi_city = ipapi_data.get("city") if ipapi_data.get("success") else None
        ipinfo_city = ipinfo_data.get("city") if ipinfo_data.get("success") else None
        if ipapi_city:
            result["city"] = ipapi_city
        elif ipinfo_city:
            result["city"] = ipinfo_city
        
        # Region/State
        ipapi_region = ipapi_data.get("region") if ipapi_data.get("success") else None
        ipinfo_region = ipinfo_data.get("region") if ipinfo_data.get("success") else None
        if ipapi_region:
            result["region"] = ipapi_region
        elif ipinfo_region:
            result["region"] = ipinfo_region
        
        # ISP/Organization info
        ipapi_isp = ipapi_data.get("isp") if ipapi_data.get("success") else None
        ipinfo_org = ipinfo_data.get("org") if ipinfo_data.get("success") else None
        
        if ipapi_isp and ipinfo_org:
            # Both services have org info - include both
            result["isp"] = ipapi_isp
            result["organization"] = ipinfo_org
        elif ipapi_isp:
            result["isp"] = ipapi_isp
        elif ipinfo_org:
            result["organization"] = ipinfo_org
        
        # Additional reliable data from ipapi
        if ipapi_data.get("success"):
            # Coordinates if available
            if ipapi_data.get("lat") and ipapi_data.get("lon"):
                result["coordinates"] = {
                    "latitude": ipapi_data.get("lat"),
                    "longitude": ipapi_data.get("lon")
                }
            
            # Timezone if available
            if ipapi_data.get("timezone"):
                result["timezone"] = ipapi_data.get("timezone")
            
            # Proxy/hosting detection (unique to ipapi)
            if "proxy" in ipapi_data:
                result["proxy"] = ipapi_data["proxy"]
            if "hosting" in ipapi_data:
                result["hosting"] = ipapi_data["hosting"]
            if "mobile" in ipapi_data:
                result["mobile"] = ipapi_data["mobile"]
            
            # AS information
            if ipapi_data.get("as"):
                result["as"] = ipapi_data["as"]
        
        # Additional data from ipinfo
        if ipinfo_data.get("success"):
            # Postal code
            if ipinfo_data.get("postal"):
                result["postal"] = ipinfo_data["postal"]
            
            # Location coordinates (if not already set)
            if not result.get("coordinates") and ipinfo_data.get("location"):
                try:
                    lat, lon = ipinfo_data["location"].split(",")
                    result["coordinates"] = {
                        "latitude": float(lat.strip()),
                        "longitude": float(lon.strip())
                    }
                except:
                    pass
        
        # Add service-specific raw data for reference
        result["raw_data"] = {}
        if ipapi_data.get("success"):
            result["raw_data"]["ipapi"] = ipapi_data
        if ipinfo_data.get("success"):
            result["raw_data"]["ipinfo"] = ipinfo_data
        
        return result
    
    def format_results(self, results: Dict[str, Any]) -> str:
        """Format results in a clean, readable way"""
        if "error" in results:
            return f"Error: {results['error']}"
        
        output = []
        output.append(f"IP Address: {results.get('ip', 'Unknown')}")
        output.append(f"Checked: {results.get('timestamp', 'Unknown')}")
        output.append(f"Services: {', '.join(results.get('services_used', []))}")
        output.append("")
        
        # Location info
        location_parts = []
        if results.get('city'):
            location_parts.append(results['city'])
        if results.get('region'):
            location_parts.append(results['region'])
        if results.get('country'):
            location_parts.append(results['country'])
        
        if location_parts:
            output.append("Location:")
            output.append(f"   {', '.join(location_parts)}")
            
            if results.get('coordinates'):
                coords = results['coordinates']
                output.append(f"   Coordinates: {coords['latitude']}, {coords['longitude']}")
        
        # Network info
        network_info = []
        if results.get('isp'):
            network_info.append(f"ISP: {results['isp']}")
        if results.get('organization'):
            network_info.append(f"Org: {results['organization']}")
        if results.get('as'):
            network_info.append(f"AS: {results['as']}")
        
        if network_info:
            output.append("")
            output.append("Network:")
            for info in network_info:
                output.append(f"   {info}")
        
        # Detection results
        detection_info = []
        if 'proxy' in results:
            detection_info.append(f"Proxy: {'Yes' if results['proxy'] else 'No'}")
        if 'hosting' in results:
            detection_info.append(f"Hosting: {'Yes' if results['hosting'] else 'No'}")
        if 'mobile' in results:
            detection_info.append(f"Mobile: {'Yes' if results['mobile'] else 'No'}")
        
        if detection_info:
            output.append("")
            output.append("Detection:")
            for info in detection_info:
                output.append(f"   {info}")
        
        # Additional info
        additional_info = []
        if results.get('postal'):
            additional_info.append(f"Postal: {results['postal']}")
        if results.get('timezone'):
            additional_info.append(f"Timezone: {results['timezone']}")
        
        if additional_info:
            output.append("")
            output.append("Additional:")
            for info in additional_info:
                output.append(f"   {info}")
        
        return "\n".join(output)
    


def main():
    """Main function for command line usage"""
    checker = EnhancedIPChecker()
    
    # Check if IP was provided as argument
    if len(sys.argv) > 1:
        ip_to_check = sys.argv[1]
        print(f"Checking provided IP: {ip_to_check}")
    else:
        ip_to_check = None
        print("Checking current public IP...")
    
    # Perform the check
    results = checker.check_ip(ip_to_check)
    
    # Display results
    print("\n" + "="*50)
    print(checker.format_results(results))
    print("="*50)

if __name__ == "__main__":
    main() 