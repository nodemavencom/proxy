"""
IP Checker Package

Simple IP geolocation checkers for different services.
Each checker returns clean JSON data without formatting.

Available checkers:
- ipapi_checker: Uses ip-api.com (free, no API key required)
- ipinfo_checker: Uses ipinfo.io (free tier, no API key required)
"""

from .ipapi_checker import check_ip as check_ip_ipapi
from .ipinfo_checker import check_ip as check_ip_ipinfo

__version__ = "1.0.0"
__all__ = ["check_ip_ipapi", "check_ip_ipinfo"] 