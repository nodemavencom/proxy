# IP Checker Scripts

Simple, reliable IP geolocation checkers that return clean JSON data. Each script can be used independently or imported as modules.

## Available Services

### 1. IP-API.com (`ipapi_checker.py`) ⭐
- **Free**: No API key required
- **Features**: Comprehensive geolocation data including proxy detection
- **Limits**: 1000 requests/month for free
- **Advantages**: Detailed information, proxy detection

### 2. IPInfo.io (`ipinfo_checker.py`) 🌐
- **Free**: No API key required for basic usage
- **Features**: Good coverage, reliable service
- **Limits**: 50,000 requests/month for free
- **Advantages**: High rate limits, good uptime

## Usage Examples

### Command Line Usage

```bash
# Check current IP using IP-API (most detailed)
python ip_checker/ipapi_checker.py

# Check current IP using IPInfo (reliable)
python ip_checker/ipinfo_checker.py

# Check specific IP using IP-API
python ip_checker/ipapi_checker.py 8.8.8.8

# Check specific IP using IPInfo
python ip_checker/ipinfo_checker.py 1.1.1.1
```

### Python Import Usage

```python
# Import individual checkers
from ip_checker.ipapi_checker import check_ip as check_ipapi
from ip_checker.ipinfo_checker import check_ip as check_ipinfo

# Check IP using different services
ip = "8.8.8.8"

# IP-API (comprehensive data)
result1 = check_ipapi(ip)
print(f"Location: {result1['city']}, {result1['country']}")
print(f"ISP: {result1['isp']}")
print(f"Proxy: {result1.get('proxy', 'No')}")

# IPInfo (reliable data)
result2 = check_ipinfo(ip)
print(f"Location: {result2['city']}, {result2['country']}")
```

### Package Imports (Recommended)

```python
# Import from the package (cleaner)
from ip_checker import check_ip_ipapi, check_ip_ipinfo

ip = "8.8.8.8"

# Use IP-API for detailed analysis
result = check_ip_ipapi(ip)
if result['success']:
    print(f"IP: {result['ip']}")
    print(f"Country: {result['country']}")
    print(f"City: {result['city']}")
    print(f"ISP: {result['isp']}")
    print(f"Timezone: {result['timezone']}")
    print(f"Is Proxy: {result.get('proxy', False)}")

# Use IPInfo for reliable checking
result = check_ip_ipinfo(ip)
if result['success']:
    print(f"Location: {result['city']}, {result['region']}, {result['country']}")
```

### Testing with NodeMaven Proxies

```python
from nodemaven.utils import get_proxy_config
from ip_checker import check_ip_ipapi
import requests

# Get a US proxy
proxies = get_proxy_config(country="us")

# Check IP through proxy
response = requests.get("http://httpbin.org/ip", proxies=proxies)
proxy_ip = response.json()['origin']

# Get detailed info about the proxy IP
ip_info = check_ip_ipapi(proxy_ip)
print(f"Proxy IP: {proxy_ip}")
print(f"Proxy Location: {ip_info['city']}, {ip_info['country']}")
print(f"Proxy ISP: {ip_info['isp']}")
```

## Response Format

All checkers return a consistent JSON structure:

### Successful Response
```json
{
  "success": true,
  "service": "service_name",
  "ip": "8.8.8.8",
  "country": "United States",
  "country_code": "US",
  "region": "California",
  "city": "Mountain View",
  "latitude": 37.4056,
  "longitude": -122.0775,
  "timezone": "America/Los_Angeles",
  "isp": "Google LLC"
}
```

### Error Response
```json
{
  "success": false,
  "service": "service_name",
  "error": "Error description",
  "ip": "requested_ip"
}
```

### Service-Specific Fields

**IP-API.com** includes additional fields:
- `proxy`: Boolean indicating if IP is a proxy
- `hosting`: Boolean indicating if IP is from hosting provider
- `mobile`: Boolean indicating if connection is mobile

**IPInfo.io** includes:
- `hostname`: Reverse DNS hostname
- `postal`: Postal/ZIP code
- `org`: Organization information

## Advanced Usage

### Batch IP Checking
```python
from ip_checker import check_ip_ipapi

ips_to_check = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]

for ip in ips_to_check:
    result = check_ip_ipapi(ip)
    if result['success']:
        print(f"{ip}: {result['city']}, {result['country']} ({result['isp']})")
    else:
        print(f"{ip}: Error - {result['error']}")
```

### Error Handling Best Practices
```python
from ip_checker import check_ip_ipapi
import time

def check_ip_with_retry(ip, max_retries=3):
    for attempt in range(max_retries):
        result = check_ip_ipapi(ip)
        if result['success']:
            return result
        else:
            print(f"Attempt {attempt + 1} failed: {result['error']}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retry
    
    return {"success": False, "error": "Max retries exceeded"}

# Usage
result = check_ip_with_retry("8.8.8.8")
```

### Service Selection Strategy
```python
from ip_checker import check_ip_ipapi, check_ip_ipinfo

def get_ip_info(ip):
    # Try IP-API first (more detailed)
    result = check_ip_ipapi(ip)
    if result['success']:
        return result
    
    # Fallback to IPInfo
    print("IP-API failed, trying IPInfo...")
    result = check_ip_ipinfo(ip)
    if result['success']:
        return result
    
    return {"success": False, "error": "All services failed"}

# Usage
info = get_ip_info("8.8.8.8")
```

## Dependencies

- `requests` - HTTP library (required)
- `json` - JSON handling (built-in)
- `sys` - System access (built-in)
- `typing` - Type hints (built-in)

### Installation
```bash
# Install required dependency
pip install requests

# Or install from requirements
pip install -r requirements.txt
```

## Rate Limiting

### IP-API.com
- **Free**: 1,000 requests/month
- **Rate**: ~45 requests/minute
- **Upgrade**: Available with API key

### IPInfo.io  
- **Free**: 50,000 requests/month
- **Rate**: ~1,000 requests/day
- **Upgrade**: Available with API key

### Best Practices
- Cache results when possible
- Use appropriate delays between requests
- Implement retry logic with exponential backoff
- Monitor your usage to avoid limits

## Integration with NodeMaven

These IP checkers work perfectly with NodeMaven proxies:

```python
from nodemaven.utils import get_proxy_config
from ip_checker import check_ip_ipapi
import requests

# Test proxy from different countries
countries = ["us", "gb", "ca", "au"]

for country in countries:
    try:
        # Get proxy for country
        proxies = get_proxy_config(country=country)
        
        # Make request through proxy
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10)
        proxy_ip = response.json()['origin']
        
        # Get location details
        location = check_ip_ipapi(proxy_ip)
        if location['success']:
            print(f"{country.upper()}: {proxy_ip} -> {location['city']}, {location['country']}")
        
    except Exception as e:
        print(f"{country.upper()}: Error - {e}")
```

---

**Simple, reliable IP geolocation for your applications!** 🌍 