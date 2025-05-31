# NodeMaven Python SDK 🐍

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](../LICENSE)
[![API](https://img.shields.io/badge/API-v2-orange?style=for-the-badge)](https://dashboard.nodemaven.com/documentation/v2/swagger?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=python_api_docs)

> **Professional Python client for NodeMaven's residential and mobile proxy API** - Global coverage, advanced targeting, and enterprise-grade reliability.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/nodemaven/nodemaven.git
cd nodemaven/python

# Install dependencies (optional - works without requests)
pip install -r requirements.txt

# Set up environment variables
cp ../env.example .env
# Edit .env with your credentials
```

### Environment Setup

Create a `.env` file with your NodeMaven credentials:

```bash
NODEMAVEN_APIKEY = "your_api_key_here"
NODEMAVEN_USERNAME = "your_username_here"
NODEMAVEN_PASSWORD = "your_password_here"

# Optional settings
NODEMAVEN_BASE_URL = "https://api.nodemaven.com"
NODEMAVEN_PROXY_HOST = "gate.nodemaven.com"
NODEMAVEN_HTTP_PORT = "8080"
NODEMAVEN_SOCKS5_PORT = "1080"
REQUEST_TIMEOUT = "30"
```

### Basic Usage

```python
from nodemaven import NodeMavenClient
from nodemaven.utils import get_proxy_config, get_socks5_proxy

# Initialize client
client = NodeMavenClient()

# Get user information
user_info = client.get_user_info()
print(f"Email: {user_info['email']}")
print(f"Data remaining: {user_info['data']} bytes")

# Get available countries
countries = client.get_countries(limit=10)
for country in countries['results']:
    print(f"{country['name']} ({country['code']}) - {country['availability']}")
```

## 🌐 Proxy Usage

### HTTP/HTTPS Proxies

```python
from nodemaven.utils import get_proxy_config
import requests

# Basic country targeting
proxies = get_proxy_config(country="us")

# Advanced targeting
proxies = get_proxy_config(
    country="gb",
    city="london", 
    session="my_session_123",
    filter="high"
)

# Make request through proxy
response = requests.get('https://httpbin.org/ip', proxies=proxies)
print(f"Your IP: {response.json()['origin']}")
```

## 🎯 Targeting Options

| Parameter | Description | Example Values |
|-----------|-------------|----------------|
| `country` | 2-letter country code | `us`, `gb`, `ca`, `de` |
| `region` | Region/state name | `california`, `texas`, `alabama` |
| `city` | City name | `new_york`, `london`, `birmingham` |
| `isp` | ISP name | `verizon`, `comcast`, `bt` |
| `type` | Connection type | `mobile`, `residential` |
| `session` | Custom session ID | `my_session_123` |
| `sticky` | Auto sticky session | `True`, `False` |
| `filter` | IP quality filter | `low`, `medium`, `high` |
| `ipv4` | IPv4 only | `True` (default), `False` |

## 🔧 API Methods

### User Management
```python
# Get user information
user_info = client.get_user_info()

# Check data usage
print(f"Data used: {user_info['data']} bytes")
print(f"Proxy username: {user_info['proxy_username']}")
print(f"Proxy password: {user_info['proxy_password']}")
```

### Location Data
```python
# Get countries
countries = client.get_countries(limit=50)

# Get regions for a country
regions = client.get_regions(country_code='us', limit=20)

# Get cities in a region
cities = client.get_cities(country_code='us', region_code='california')

# Get ISPs in a location
isps = client.get_isps(country_code='us', city_code='new_york')
```

## 📊 Proxy URL Format

NodeMaven uses a complex username format for targeting:

```
Protocol: http:// or socks5://
Username: base_username-country-ca-ipv4-true-sid-session123-filter-medium
Password: base_password
Host: gate.nodemaven.com
Port: 8080 (HTTP) or 1080 (SOCKS5)
```

**Example URLs:**
```
# Residential Canada (sticky)
socks5://aa101d91571b74-country-ca-ipv4-true-sid-abc123-filter-medium:aa101d91571b74@gate.nodemaven.com:1080

# Mobile US (rotating)
socks5://aa101d91571b74-country-us-type-mobile-ipv4-true-filter-medium:aa101d91571b74@gate.nodemaven.com:1080

# HTTP with targeting
http://aa101d91571b74-country-gb-city-london-ipv4-true-filter-medium:aa101d91571b74@gate.nodemaven.com:8080
```

## 🛠️ Advanced Features

### Session Management
```python
# Sticky sessions for consistent IP
proxy_url = get_socks5_proxy(country="us", session="my_session_1")

# Auto-generate session ID
proxy_url = get_socks5_proxy(country="us", sticky=True)
```

### Connection Types
```python
# Residential proxies (default)
proxy_url = get_socks5_proxy(country="us")

# Mobile proxies
proxy_url = get_socks5_proxy(country="us", type="mobile")
```

### IP Quality Filtering
```python
# High quality IPs
proxy_url = get_socks5_proxy(country="us", filter="high")

# Medium quality (default)
proxy_url = get_socks5_proxy(country="us", filter="medium")

# Low cost option
proxy_url = get_socks5_proxy(country="us", filter="low")
```

## 🔗 Links

- [🌐 NodeMaven Dashboard](https://dashboard.nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=python_dashboard)
- [📖 API Documentation](https://dashboard.nodemaven.com/documentation/v2/swagger?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=python_api_docs)
- [💬 Support](https://dashboard.nodemaven.com/support?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=python_support)
- [🚀 Get Started](https://dashboard.nodemaven.com/register?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=python_signup)

---

**Need help?** Contact our support team at [@node_maven](https://t.me/node_maven) or visit our [documentation](https://dashboard.nodemaven.com/documentation?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=python_help). 
