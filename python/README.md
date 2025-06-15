# NodeMaven Python SDK 🐍

Official Python client library for NodeMaven proxy services with comprehensive testing and IP checking utilities.

## 📁 Project Structure

- **`nodemaven/`** - Core Python SDK for NodeMaven proxy API
- **`ip_checker/`** - Standalone IP geolocation checkers
- **`ip_checker.py`** - Enhanced IP checker with merged service data
- **`examples/`** - Complete usage examples and demos
- **`tests/`** - Comprehensive test suite (48 tests total)
- **`tools/`** - Location data management utilities

## 🚀 Quick Setup

### 1. Create Virtual Environment

```bash
# Navigate to python directory
cd proxy/python

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your NodeMaven credentials
# NODEMAVEN_APIKEY=your_api_key_here
```

## 🔧 NodeMaven SDK Usage

### Basic Client Usage

```python
from nodemaven import NodeMavenClient

# Initialize client
client = NodeMavenClient()

# Get user info
user_info = client.get_user_info()
print(f"Email: {user_info['email']}")
print(f"Data remaining: {user_info.get('data_remaining', 'N/A')} bytes")

# Get available countries
countries = client.get_countries(limit=10)
for country in countries['results']:
    print(f"- {country['name']} ({country['code']})")
```

### Proxy Configuration

```python
from nodemaven.utils import build_proxy_url, get_proxy_config

# HTTP proxy with targeting
proxy_url = build_proxy_url(
    protocol="http",
    country="us",
    region="california", 
    city="los_angeles",
    type="residential",
    session="my_session_123",
    ttl="1h",
    filter="high"
)

# Get proxy config for requests library
proxies = get_proxy_config(country="us", city="new_york")

# Use with requests
import requests
response = requests.get("http://httpbin.org/ip", proxies=proxies)
print(f"Your IP: {response.json()['origin']}")
```

### SOCKS5 Proxy

```python
# SOCKS5 proxy configuration
socks5_url = client.getSocks5ProxyUrl({
    'country': 'gb',
    'type': 'mobile',
    'filter': 'medium'
})
```

## 🛠️ Available Tools

### IP Checker Tools

```bash
# Check current IP with merged data from multiple services
python ip_checker.py

# Check specific IP
python ip_checker.py 8.8.8.8

# Use individual checkers
python ip_checker/ipapi_checker.py 1.1.1.1
python ip_checker/ipinfo_checker.py 1.1.1.1
```

### Location Data Tools

```bash
# Update location database from NodeMaven API
python tools/update_locations.py

# Location data is cached in tools/locations.json
```

## 📚 Examples

Check the `examples/` folder for comprehensive usage examples:

- **`basic_usage.py`** - Simple proxy usage and API basics
- **`proxy_examples.py`** - Advanced proxy configurations and targeting
- **`proxy_rotation.py`** - IP rotation and session management techniques
- **`generate_mobile_proxy.py`** - Mobile proxy specific examples

```bash
# Run examples
python examples/basic_usage.py
python examples/proxy_examples.py
python examples/proxy_rotation.py
```

## 🧪 Testing

### Comprehensive Test Suite
**48 tests total** covering all functionality:

```bash
# Run all tests (requires API key)
python -m pytest tests/ -v

# Unit tests only (no API key needed)
python -m pytest tests/test_unit.py -v

# Integration tests (requires API key)
python -m pytest tests/test_integration.py -v
```

### Test Coverage
- **31 Unit Tests**: Proxy username building, TTL validation, utilities
- **17 Integration Tests**: Real API calls, proxy connections, error handling
- **All targeting options tested**: Country, region, city, ISP, type, IPv4, session, TTL, filter

## 🎯 Key Features

### Proxy Targeting Options
- ✅ **Geographic**: Country, region, city targeting
- ✅ **ISP Filtering**: Target specific internet service providers
- ✅ **Connection Types**: Residential & mobile proxies
- ✅ **Session Management**: Sticky sessions with TTL support
- ✅ **Quality Filters**: High, medium, low quality filtering
- ✅ **Protocol Support**: HTTP, HTTPS, SOCKS5

### Advanced Features
- ✅ **TTL Support**: Time-to-live for sticky sessions (1h, 30m, 120s, etc.)
- ✅ **Auto-rotation**: Automatic IP rotation
- ✅ **Session Persistence**: Maintain same IP across requests
- ✅ **IPv4/IPv6**: IP version targeting
- ✅ **Error Handling**: Comprehensive error management

### IP Checking
- ✅ Multiple free API sources (IP-API, IPInfo)
- ✅ Intelligent data merging
- ✅ Clean JSON output
- ✅ Proxy detection
- ✅ Geolocation data

## ⚙️ Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NODEMAVEN_APIKEY` | Your API key (required) | - |
| `NODEMAVEN_BASE_URL` | API base URL | `https://dashboard.nodemaven.com` |
| `NODEMAVEN_PROXY_HOST` | Proxy host | `gate.nodemaven.com` |
| `NODEMAVEN_HTTP_PORT` | HTTP proxy port | `8080` |
| `NODEMAVEN_SOCKS5_PORT` | SOCKS5 proxy port | `1080` |
| `REQUEST_TIMEOUT` | Request timeout (seconds) | `30` |
| `DEBUG` | Enable debug mode | `false` |

### Proxy Username Building
The SDK automatically builds complex proxy usernames:
```
alex_worldmediabuy_com-country-us-region-california-city-los_angeles-type-residential-ipv4-true-sid-test123-ttl-1h-filter-high
```

## 🤝 Support & Community

- 📧 **Email**: [support@nodemaven.com](mailto:support@nodemaven.com)
- 💬 **Live Chat**: [NodeMaven Dashboard](https://dashboard.nodemaven.com?utm_source=github&utm_medium=python_readme&utm_campaign=developer_outreach&utm_content=support_chat)
- 🐛 **Issues**: [GitHub Issues](https://github.com/nodemavencom/proxy/issues)
- 📖 **API Docs**: [Documentation](https://dashboard.nodemaven.com/documentation?utm_source=github&utm_medium=python_readme&utm_campaign=developer_outreach&utm_content=api_docs)

## 🔗 Other SDKs

Our multi-language proxy SDK collection:
- 🟢 **[JavaScript SDK](../javascript/)** - Zero-dependency Node.js implementation
- 🟣 **[PHP SDK](../php/)** - Modern PHP 8.0+ implementation
- 🔷 **[Go SDK](../go/)** - High-performance Go implementation

## 📋 Requirements

- **Python**: 3.8+ (tested with 3.10+)
- **Dependencies**:
  - `requests` - HTTP library (optional, falls back to urllib)
  - `python-dotenv` - Environment variable loading (optional)
- **NodeMaven API key** - Required for proxy features

## 🏆 Production Ready

This SDK has been thoroughly tested and validated:
- ✅ **48 comprehensive tests** covering all functionality
- ✅ **Real proxy connections tested** across multiple countries
- ✅ **Error handling** for all failure scenarios
- ✅ **Fallback support** when dependencies unavailable
- ✅ **CI/CD ready** with GitHub Actions integration

---

<div align="center">

**[🚀 Get Started](https://dashboard.nodemaven.com?utm_source=github&utm_medium=python_readme&utm_campaign=developer_outreach&utm_content=footer_cta)** • **[📖 Full Documentation](https://dashboard.nodemaven.com/documentation?utm_source=github&utm_medium=python_readme&utm_campaign=developer_outreach&utm_content=footer_docs)** • **[💬 Support](https://dashboard.nodemaven.com?utm_source=github&utm_medium=python_readme&utm_campaign=developer_outreach&utm_content=footer_support)**

Made with ❤️ by the NodeMaven Team

</div>
