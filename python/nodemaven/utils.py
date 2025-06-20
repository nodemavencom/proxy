"""
Utility functions for NodeMaven API client.
"""

import os
import uuid
from typing import Optional, Dict, Any, Union
from datetime import datetime
import re


def load_env_file(env_path: str = '.env') -> None:
    """Load environment variables from .env file."""
    if not os.path.exists(env_path):
        return
    
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                os.environ[key] = value


# Load .env file when module is imported
load_env_file()
load_env_file('../.env')  # Try parent directory too

# Cache for API credentials
_api_credentials_cache = None


def get_api_key() -> Optional[str]:
    """Get API key from environment variables."""
    return os.getenv('NODEMAVEN_APIKEY')


def get_proxy_username() -> Optional[str]:
    """Get proxy username from environment variables or API."""
    # First try environment variable
    env_username = os.getenv('NODEMAVEN_USERNAME')
    if env_username:
        return env_username
    
    # If not in environment, try to get from API
    try:
        credentials = get_api_credentials()
        return credentials.get('proxy_username')
    except:
        return None


def get_proxy_password() -> Optional[str]:
    """Get proxy password from environment variables or API."""
    # First try environment variable
    env_password = os.getenv('NODEMAVEN_PASSWORD')
    if env_password:
        return env_password
    
    # If not in environment, try to get from API
    try:
        credentials = get_api_credentials()
        return credentials.get('proxy_password')
    except:
        return None


def get_api_credentials() -> Dict[str, Any]:
    """Get proxy credentials from API (cached)."""
    global _api_credentials_cache
    
    if _api_credentials_cache:
        return _api_credentials_cache
    
    # Import here to avoid circular imports
    try:
        from .client import NodeMavenClient
        client = NodeMavenClient()
        user_info = client.get_user_info()
        _api_credentials_cache = user_info
        return user_info
    except Exception:
        return {}


def get_correct_proxy_credentials() -> tuple:
    """Get the correct proxy credentials from API."""
    try:
        credentials = get_api_credentials()
        username = credentials.get('proxy_username')
        password = credentials.get('proxy_password')
        return username, password
    except Exception:
        # Fallback to environment variables
        return get_proxy_username(), get_proxy_password()


def get_base_url() -> str:
    """Get base API URL from environment or default."""
    return os.getenv('NODEMAVEN_BASE_URL', 'https://dashboard.nodemaven.com')


def get_proxy_host() -> str:
    """Get proxy host from environment or default."""
    return os.getenv('NODEMAVEN_PROXY_HOST', 'gate.nodemaven.com')


def get_http_port() -> int:
    """Get HTTP proxy port from environment or default."""
    try:
        return int(os.getenv('NODEMAVEN_HTTP_PORT', '8080'))
    except ValueError:
        return 8080


def get_socks5_port() -> int:
    """Get SOCKS5 proxy port from environment or default."""
    try:
        return int(os.getenv('NODEMAVEN_SOCKS5_PORT', '1080'))
    except ValueError:
        return 1080


def get_timeout() -> int:
    """Get request timeout from environment or default."""
    try:
        return int(os.getenv('REQUEST_TIMEOUT', '30'))
    except ValueError:
        return 30


def is_debug_enabled() -> bool:
    """Check if debug mode is enabled."""
    return os.getenv('DEBUG', '').lower() in ('true', '1', 'yes', 'on')


def format_bytes(bytes_value: int) -> str:
    """Format bytes into human-readable string."""
    if bytes_value == 0:
        return "0 B"
    
    sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    size_index = 0
    value = float(bytes_value)
    
    while value >= 1024 and size_index < len(sizes) - 1:
        value /= 1024
        size_index += 1
    
    if size_index == 0:
        return f"{int(value)} {sizes[size_index]}"
    else:
        return f"{value:.2f} {sizes[size_index]}"


def validate_proxy_username(username: str) -> bool:
    """Validate proxy username format."""
    if not username:
        return False
    
    # Username must be alphanumeric and underscores only, 9-100 characters
    pattern = r'^[a-zA-Z0-9_]{9,100}$'
    return bool(re.match(pattern, username))


def validate_proxy_password(password: str) -> bool:
    """Validate proxy password format."""
    if not password:
        return False
    
    # Password must be alphanumeric and underscores only, 9-100 characters
    pattern = r'^[a-zA-Z0-9_]{9,100}$'
    return bool(re.match(pattern, password))


def validate_date_format(date_string: str) -> None:
    """Validate date string in ``dd-mm-yyyy`` format.

    Raises:
        ValueError: If the date string does not match the expected format.
    """
    try:
        datetime.strptime(date_string, "%d-%m-%Y")
    except ValueError as exc:
        raise ValueError(
            f"Invalid date format for '{date_string}'. Expected dd-mm-yyyy"
        ) from exc


def generate_session_id() -> str:
    """Generate a random session ID."""
    return str(uuid.uuid4()).replace('-', '')[:13]  # Match website format (13 chars)


def validate_ttl_format(ttl_string: str) -> bool:
    """
    Validate TTL format according to how-api-works.md specification.
    
    Valid formats: 60s, 1m, 5m, 1h, 24h
    """
    import re
    pattern = r'^(\d+)(s|m|h)$'
    return bool(re.match(pattern, ttl_string))


def build_proxy_username(base_username: str, **targeting) -> str:
    """
    Build NodeMaven proxy username with targeting parameters.
    
    Format matches how-api-works.md exactly with full TTL support.
    Examples:
    - aa101d91571b74-country-us-region-new_york-city-brooklyn
    - aa101d91571b74-country-any-type-mobile-ipv4-true-sid-a49c071423294-ttl-24h-filter-medium
    """
    parts = [base_username]
    
    # Country targeting
    if 'country' in targeting and targeting['country']:
        parts.extend(['country', targeting['country'].lower()])
    
    # Region targeting  
    if 'region' in targeting and targeting['region']:
        # Preserve underscores, only replace spaces with underscores (per how-api-works.md)
        region = targeting['region'].lower().replace(' ', '_')
        parts.extend(['region', region])
    
    # City targeting
    if 'city' in targeting and targeting['city']:
        # Preserve underscores, only replace spaces with underscores 
        city = targeting['city'].lower().replace(' ', '_')
        parts.extend(['city', city])
    
    # ISP targeting
    if 'isp' in targeting and targeting['isp']:
        # For ISP, replace spaces and keep underscores
        isp = targeting['isp'].lower().replace(' ', '_')
        parts.extend(['isp', isp])
    
    # Connection type (mobile, residential)
    if 'type' in targeting and targeting['type']:
        parts.extend(['type', targeting['type'].lower()])
    
    # IP version (only add if explicitly requested or not default)
    if 'ipv4' in targeting:
        ipv4_value = targeting['ipv4']
        if ipv4_value is True:
            parts.extend(['ipv4', 'true'])
        elif ipv4_value is False:
            parts.extend(['ipv4', 'false'])
    
    # Session ID for sticky sessions
    session_id = None
    if 'session' in targeting and targeting['session']:
        session_id = str(targeting['session'])
        parts.extend(['sid', session_id])
    elif targeting.get('sticky', False):
        # Generate random session ID for sticky sessions
        session_id = generate_session_id()
        parts.extend(['sid', session_id])
    
    # TTL (Time-To-Live) for sticky sessions - NEW FUNCTIONALITY
    if 'ttl' in targeting and targeting['ttl'] and session_id:
        ttl_value = targeting['ttl']
        if validate_ttl_format(ttl_value):
            parts.extend(['ttl', ttl_value])
        else:
            raise ValueError(f"Invalid TTL format: {ttl_value}. Valid formats: 60s, 1m, 5m, 1h, 24h")
    
    # IP filter quality (only add if explicitly requested)
    if 'filter' in targeting and targeting['filter']:
        parts.extend(['filter', targeting['filter']])
    
    return '-'.join(parts)


def build_proxy_url(protocol: str = 'http', **targeting) -> str:
    """
    Build complete proxy URL for NodeMaven using correct API credentials.
    
    Examples:
    - HTTP: http://username-country-us-ipv4-true-filter-medium:password@gate.nodemaven.com:8080
    - SOCKS5: socks5://username-country-us-ipv4-true-filter-medium:password@gate.nodemaven.com:1080
    """
    # Get correct credentials from API
    base_username, password = get_correct_proxy_credentials()
    host = get_proxy_host()
    
    if not base_username or not password:
        raise ValueError("Could not get proxy credentials. Please check your API key and connection.")
    
    # Build complex username with targeting (matching website format exactly)
    proxy_username = build_proxy_username(base_username, **targeting)
    
    # Get port based on protocol
    if protocol.lower() == 'socks5':
        port = get_socks5_port()
    else:
        port = get_http_port()
        protocol = 'http'  # Normalize to http for HTTP/HTTPS
    
    return f"{protocol}://{proxy_username}:{password}@{host}:{port}"


def get_proxy_config(**targeting) -> Dict[str, str]:
    """
    Get proxy configuration dictionary for requests library.
    
    Args:
        **targeting: Targeting parameters (country, region, city, isp, type, session, etc.)
    
    Returns:
        Dict with 'http' and 'https' proxy URLs
    """
    proxy_url = build_proxy_url(protocol='http', **targeting)
    
    return {
        'http': proxy_url,
        'https': proxy_url
    }


def get_socks5_proxy(**targeting) -> str:
    """
    Get SOCKS5 proxy URL.
    
    Args:
        **targeting: Targeting parameters
    
    Returns:
        SOCKS5 proxy URL string
    """
    return build_proxy_url(protocol='socks5', **targeting)


def clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values from dictionary."""
    return {k: v for k, v in data.items() if v is not None}


def parse_error_message(response_data: Dict[str, Any]) -> str:
    """Parse error message from API response."""
    if 'error' in response_data:
        return str(response_data['error'])
    elif 'detail' in response_data:
        return str(response_data['detail'])
    elif 'errors' in response_data:
        errors = response_data['errors']
        if isinstance(errors, dict):
            # Handle validation errors
            error_messages = []
            for field, messages in errors.items():
                if isinstance(messages, list):
                    error_messages.extend([f"{field}: {msg}" for msg in messages])
                else:
                    error_messages.append(f"{field}: {messages}")
            return "; ".join(error_messages)
        elif isinstance(errors, list):
            return "; ".join(str(error) for error in errors)
        else:
            return str(errors)
    else:
        return "Unknown error occurred"


def get_current_ip(proxies: Optional[Dict[str, str]] = None, timeout: int = 10) -> Optional[str]:
    """
    Get current public IP address using reliable endpoints.
    
    Args:
        proxies: Optional proxy configuration for requests
        timeout: Request timeout in seconds
    
    Returns:
        IP address string or None if failed
    """
    # Try to import requests, fall back to urllib if not available
    try:
        import requests
        HAS_REQUESTS = True
    except ImportError:
        import urllib.request
        import urllib.error
        HAS_REQUESTS = False
    
    # Reliable IP checking endpoints
    endpoints = [
        "https://api.ipify.org",
        "https://checkip.amazonaws.com",
        "https://ipecho.net/plain",
        "https://myexternalip.com/raw"
    ]
    
    for endpoint in endpoints:
        try:
            if HAS_REQUESTS:
                response = requests.get(endpoint, proxies=proxies, timeout=timeout)
                if response.status_code == 200:
                    return response.text.strip()
            else:
                # Use urllib as fallback
                req = urllib.request.Request(endpoint)
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    if response.status == 200:
                        return response.read().decode('utf-8').strip()
        except Exception:
            continue
    
    return None


def check_ip_with_details(ip_address: Optional[str] = None, proxies: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Check IP address with detailed information using free APIs.
    
    Args:
        ip_address: IP to check (if None, checks current IP)
        proxies: Optional proxy configuration for requests
    
    Returns:
        Dictionary with IP details or error information
    """
    try:
        import requests
        HAS_REQUESTS = True
    except ImportError:
        HAS_REQUESTS = False
    
    if not ip_address:
        ip_address = get_current_ip(proxies=proxies)
        if not ip_address:
            return {"error": "Could not determine IP address"}
    
    if not HAS_REQUESTS:
        return {
            "ip": ip_address,
            "error": "requests library not available for detailed IP checking"
        }
    
    # Use ip-api.com for detailed information (free, no key needed)
    try:
        url = f"http://ip-api.com/json/{ip_address}?fields=66846719"
        response = requests.get(url, proxies=proxies, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "ip": ip_address,
                    "country": data.get("country"),
                    "country_code": data.get("countryCode"),
                    "region": data.get("regionName"),
                    "city": data.get("city"),
                    "isp": data.get("isp"),
                    "org": data.get("org"),
                    "proxy": data.get("proxy", False),
                    "hosting": data.get("hosting", False),
                    "mobile": data.get("mobile", False)
                }
    except Exception as e:
        pass
    
    # Fallback to basic IP only
    return {"ip": ip_address} 