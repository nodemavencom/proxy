"""
Main NodeMaven API client.
"""

import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Optional, Dict, Any, List
import os

# Try to import requests, fall back to urllib if not available
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Try to import dotenv, but don't fail if not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from .exceptions import get_exception_for_status_code
from .utils import (
    get_api_key, get_base_url, get_timeout, clean_dict, 
    parse_error_message, validate_date_format
)


class NodeMavenClient:
    """
    NodeMaven API client for managing residential and mobile proxies.
    Works with or without the requests library.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None,
                 timeout: Optional[int] = None):
        """Initialize NodeMaven client."""
        self.api_key = api_key or get_api_key()
        if not self.api_key:
            raise ValueError("API key is required. Set NODEMAVEN_APIKEY environment variable or pass api_key parameter.")
        
        self.base_url = base_url or get_base_url()
        self.timeout = timeout or get_timeout()
        
        # Set up session if requests is available
        if HAS_REQUESTS:
            self.session = requests.Session()
            self.session.headers.update({
                'Authorization': f'x-api-key {self.api_key}',
                'Content-Type': 'application/json',
                'User-Agent': 'NodeMaven-Python-Client/1.0.0'
            })
        else:
            self.session = None
    
    def _make_request_urllib(self, method: str, url: str, params: Optional[Dict] = None,
                           json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request using urllib (fallback when requests not available)."""
        # Add query parameters to URL
        if params:
            clean_params = clean_dict(params)
            if clean_params:
                url += '?' + urllib.parse.urlencode(clean_params)
        
        # Prepare request data
        data = None
        if json_data:
            data = json.dumps(json_data).encode('utf-8')
        
        # Create request
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                'Authorization': f'x-api-key {self.api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'NodeMaven-Python-Client/1.0.0'
            }
        )
        req.get_method = lambda: method.upper()
        
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                response_data = response.read().decode('utf-8')
                if response_data:
                    return json.loads(response_data)
                return {}
                
        except urllib.error.HTTPError as e:
            try:
                error_data = json.loads(e.read().decode('utf-8'))
                error_message = parse_error_message(error_data)
            except (ValueError, AttributeError):
                error_message = f"HTTP {e.code}: {e.reason}"
                error_data = {}
            
            raise get_exception_for_status_code(e.code, error_message, error_data)
            
        except urllib.error.URLError as e:
            raise get_exception_for_status_code(500, f"Request failed: {str(e)}")
        except Exception as e:
            raise get_exception_for_status_code(500, f"Unexpected error: {str(e)}")
    
    def _make_request_requests(self, method: str, endpoint: str, params: Optional[Dict] = None,
                             json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request using requests library."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=clean_dict(params or {}),
                json=json_data,
                timeout=self.timeout
            )
            
            # Handle successful responses
            if response.status_code < 400:
                try:
                    return response.json()
                except ValueError:
                    return {}
            
            # Handle error responses
            try:
                error_data = response.json()
                error_message = parse_error_message(error_data)
            except ValueError:
                error_message = f"HTTP {response.status_code}: {response.reason}"
                error_data = {}
            
            raise get_exception_for_status_code(response.status_code, error_message, error_data)
            
        except requests.exceptions.RequestException as e:
            raise get_exception_for_status_code(500, f"Request failed: {str(e)}")
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None,
                     json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to NodeMaven API using available library."""
        if HAS_REQUESTS and self.session:
            return self._make_request_requests(method, endpoint, params, json_data)
        else:
            url = f"{self.base_url}{endpoint}"
            return self._make_request_urllib(method, url, params, json_data)
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get current user information including proxy credentials and usage data."""
        return self._make_request('GET', '/api/v2/base/users/me')
    
    def get_countries(self, limit: int = 50, offset: int = 0, name: Optional[str] = None,
                     code: Optional[str] = None, connection_type: str = "residential") -> Dict[str, Any]:
        """Get list of available countries for proxy connections."""
        params = {
            'limit': limit,
            'offset': offset,
            'name': name,
            'code': code,
            'connection_type': connection_type
        }
        return self._make_request('GET', '/api/v2/base/locations/countries/', params)
    
    def get_regions(self, limit: int = 50, offset: int = 0, country_code: Optional[str] = None,
                   name: Optional[str] = None, code: Optional[str] = None, 
                   connection_type: str = "residential") -> Dict[str, Any]:
        """Get list of regions in specified countries."""
        params = {
            'limit': limit,
            'offset': offset,
            'country__code': country_code,
            'name': name,
            'code': code,
            'connection_type': connection_type
        }
        return self._make_request('GET', '/api/v2/base/locations/regions/', params)
    
    def get_cities(self, limit: int = 50, offset: int = 0, country_code: Optional[str] = None,
                  region_code: Optional[str] = None, name: Optional[str] = None,
                  code: Optional[str] = None, connection_type: str = "residential") -> Dict[str, Any]:
        """Get list of cities in specified regions/countries."""
        params = {
            'limit': limit,
            'offset': offset,
            'country__code': country_code,
            'region__code': region_code,
            'name': name,
            'code': code,
            'connection_type': connection_type
        }
        return self._make_request('GET', '/api/v2/base/locations/cities/', params)
    
    def get_isps(self, limit: int = 50, offset: int = 0, country_code: Optional[str] = None,
                region_code: Optional[str] = None, city_code: Optional[str] = None,
                name: Optional[str] = None, connection_type: str = "residential") -> Dict[str, Any]:
        """Get list of ISPs in specified locations."""
        params = {
            'limit': limit,
            'offset': offset,
            'country__code': country_code,
            'region__code': region_code,
            'city__code': city_code,
            'name': name,
            'connection_type': connection_type
        }
        return self._make_request('GET', '/api/v2/base/locations/isps/', params)
    
    def get_zip_codes(self, limit: int = 50, offset: int = 0, country_code: Optional[str] = None,
                     region_code: Optional[str] = None, city_code: Optional[str] = None,
                     code: Optional[str] = None, connection_type: str = "residential") -> Dict[str, Any]:
        """Get list of ZIP codes in specified locations."""
        params = {
            'limit': limit,
            'offset': offset,
            'country__code': country_code,
            'region__code': region_code,
            'city__code': city_code,
            'code': code,
            'connection_type': connection_type
        }
        return self._make_request('GET', '/api/v2/base/locations/zip-codes/', params)
    
    def get_statistics(self, start_date: Optional[str] = None, end_date: Optional[str] = None,
                      group_by: str = "day") -> Dict[str, Any]:
        """Get usage statistics for specified date range."""
        params = {}
        if start_date:
            validate_date_format(start_date)
            params['start_date'] = start_date
        if end_date:
            validate_date_format(end_date)
            params['end_date'] = end_date
        params['group_by'] = group_by
        
        return self._make_request('GET', '/api/v2/base/statistics/', params)
    
    def get_domain_statistics(self, start_date: Optional[str] = None, end_date: Optional[str] = None,
                            limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """Get domain-specific usage statistics."""
        params = {
            'limit': limit,
            'offset': offset
        }
        if start_date:
            validate_date_format(start_date)
            params['start_date'] = start_date
        if end_date:
            validate_date_format(end_date)
            params['end_date'] = end_date
        
        return self._make_request('GET', '/api/v2/base/statistics/domains/', params)
    
    def get_sub_users(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """Get list of sub-users."""
        params = {'limit': limit, 'offset': offset}
        return self._make_request('GET', '/api/v2/base/sub-users/', params)
    
    def create_sub_user(self, username: str, password: str, traffic_limit: Optional[int] = None,
                       expiry_date: Optional[str] = None) -> Dict[str, Any]:
        """Create a new sub-user."""
        data = {
            'username': username,
            'password': password
        }
        if traffic_limit is not None:
            data['traffic_limit'] = traffic_limit
        if expiry_date:
            validate_date_format(expiry_date)
            data['expiry_date'] = expiry_date
        
        return self._make_request('POST', '/api/v2/base/sub-users/', json_data=data)
    
    def update_sub_user(self, sub_user_id: str, username: Optional[str] = None,
                       password: Optional[str] = None, traffic_limit: Optional[int] = None,
                       expiry_date: Optional[str] = None) -> Dict[str, Any]:
        """Update an existing sub-user."""
        data = {}
        if username is not None:
            data['username'] = username
        if password is not None:
            data['password'] = password
        if traffic_limit is not None:
            data['traffic_limit'] = traffic_limit
        if expiry_date is not None:
            validate_date_format(expiry_date)
            data['expiry_date'] = expiry_date
        
        return self._make_request('PATCH', f'/api/v2/base/sub-users/{sub_user_id}/', json_data=data)
    
    def delete_sub_user(self, sub_user_id: str) -> Dict[str, Any]:
        """Delete a sub-user."""
        return self._make_request('DELETE', f'/api/v2/base/sub-users/{sub_user_id}/')
    
    def get_whitelist_ips(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """Get list of whitelisted IP addresses."""
        params = {'limit': limit, 'offset': offset}
        return self._make_request('GET', '/api/v2/base/whitelist-ips/', params)
    
    def add_whitelist_ip(self, ip_address: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Add an IP address to the whitelist."""
        data = {'ip_address': ip_address}
        if description:
            data['description'] = description
        
        return self._make_request('POST', '/api/v2/base/whitelist-ips/', json_data=data)
    
    def delete_whitelist_ip(self, ip_id: str) -> Dict[str, Any]:
        """Remove an IP address from the whitelist."""
        return self._make_request('DELETE', f'/api/v2/base/whitelist-ips/{ip_id}/')
    
    def getProxyConfig(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get proxy configuration for HTTP/HTTPS usage with targeting options.
        
        Args:
            options (Dict, optional): Targeting options including:
                - country (str): Country code (e.g., 'US', 'GB')
                - region (str): Region/state name
                - city (str): City name
                - session (str): Session ID for sticky sessions
                - type (str): Connection type ('residential' or 'mobile')
                - format (str): Output format ('username_password' or 'endpoint')
        
        Returns:
            Dict containing proxy configuration with host, ports, username, password
        """
        # Use the utility function if options provided, otherwise call API directly
        if options:
            from .utils import get_proxy_config
            return get_proxy_config(**options)
        else:
            # Default API call for basic proxy config
            return self._make_request('GET', '/api/v2/residential/sticky-session/')

    def getSocks5ProxyUrl(self, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Get SOCKS5 proxy URL with targeting options.
        
        Args:
            options (Dict, optional): Same targeting options as getProxyConfig
        
        Returns:
            String containing the SOCKS5 proxy URL
        """
        from .utils import get_socks5_proxy
        if options:
            return get_socks5_proxy(**options)
        else:
            # Default SOCKS5 proxy
            return get_socks5_proxy() 