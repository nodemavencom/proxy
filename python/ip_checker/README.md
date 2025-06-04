# IP Checker Scripts

Simple, clean IP geolocation checkers that return JSON data without emojis or formatting. Each script can be used independently or imported as modules.

## Available Services

### 1. IP-API.com (`ipapi_checker.py`)
- **Free**: No API key required
- **Features**: Comprehensive data including proxy detection
- **Limits**: 1000 requests/month for free

### 2. IPInfo.io (`ipinfo_checker.py`)
- **Free**: No API key required for basic usage
- **Features**: Good coverage, reliable
- **Limits**: 50,000 requests/month for free

## Usage Examples

### Command Line Usage

```bash
# Check current IP using IP-API
python ipapi_checker.py

# Check specific IP using IP-API  
python ipapi_checker.py 8.8.8.8

# Check current IP using IPInfo
python ipinfo_checker.py

# Check specific IP using IPInfo
python ipinfo_checker.py 8.8.8.8
```

### Python Import Usage

```python
# Import individual checkers
from ip_checker.ipapi_checker import check_ip as check_ipapi
from ip_checker.ipinfo_checker import check_ip as check_ipinfo

# Check IP using different services
ip = "8.8.8.8"

# IP-API (no key needed)
result1 = check_ipapi(ip)
print(result1)

# IPInfo (no key needed)
result2 = check_ipinfo(ip)
print(result2)
```

### Using the package imports

```python
# Import from the package
from ip_checker import check_ip_ipapi, check_ip_ipinfo

ip = "8.8.8.8"
result = check_ip_ipapi(ip)
print(result)
```

## Response Format

All checkers return a consistent JSON structure:

```json
{
  "success": true,
  "service": "service_name",
  "ip": "8.8.8.8",
  "country": "United States",
  "city": "Mountain View",
  // ... other service-specific fields
}
```

On error:

```json
{
  "success": false,
  "service": "service_name", 
  "error": "Error description"
}
```

## Dependencies

- `requests`
- `json` (built-in)
- `sys` (built-in)
- `typing` (built-in)

Install dependencies:
```bash
pip install requests
``` 