# NodeMaven Python Tools 🐍

Python client library and tools for NodeMaven proxy services with built-in IP checking utilities.

## 📁 Contents

- **`nodemaven/`** - Python SDK for NodeMaven proxy API
- **`ip_checker/`** - Standalone IP geolocation checkers
- **`ip_checker.py`** - Enhanced IP checker with merged service data
- **`examples/`** - Usage examples and demos
- **`tests/`** - Simple test files for all functionality
- **`tools/`** - Location data management utilities
- **`quick_test.py`** - Quick proxy testing script

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

## 🔧 Available Tools

### NodeMaven API Client

```python
from nodemaven import NodeMavenClient

# Initialize client
client = NodeMavenClient()

# Get user info
user_info = client.get_user_info()
print(f"Data remaining: {user_info['data']} bytes")

# Get proxy configuration
from nodemaven.utils import get_proxy_config
proxies = get_proxy_config(country="us", city="new_york")
```

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

### Quick Proxy Test

```bash
# Test proxy functionality
python quick_test.py
```

### Location Data Tools

```bash
# Update location database from NodeMaven API
python tools/update_locations.py

# Location data is cached in tools/locations.json
```

## 📚 Examples

Check the `examples/` folder for comprehensive usage examples:

- **`basic_usage.py`** - Simple proxy usage
- **`proxy_examples.py`** - Advanced proxy configurations  
- **`proxy_rotation.py`** - IP rotation techniques

```bash
# Run examples
python examples/basic_usage.py
python examples/proxy_examples.py
```

## 🎯 Key Features

### NodeMaven SDK
- ✅ Residential & mobile proxy access
- ✅ Global country/city targeting
- ✅ Session management 
- ✅ ISP filtering
- ✅ Auto-rotation & sticky sessions

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

## 🤝 Support & Community

- 📧 **Email**: [support@nodemaven.com](mailto:support@nodemaven.com)
- 💬 **Live Chat**: [NodeMaven Dashboard](https://dashboard.nodemaven.com?utm_source=github&utm_medium=python_readme&utm_campaign=developer_outreach&utm_content=support_chat)
- 🐛 **Issues**: [GitHub Issues](https://github.com/nodemavencom/proxy/issues)
- 📖 **API Docs**: [Documentation](https://dashboard.nodemaven.com/documentation?utm_source=github&utm_medium=python_readme&utm_campaign=developer_outreach&utm_content=api_docs)

## 🔗 Other SDKs

- 🟢 **[JavaScript SDK](../javascript/)** - Zero-dependency Node.js implementation
- 🟣 **[PHP SDK](../php/)** - Modern PHP 8.0+ implementation
- 🔷 **[Go SDK](../go/)** - High-performance Go implementation

## 📋 Requirements

- Python 3.7+
- requests, python-dotenv, pydantic
- NodeMaven API key (for proxy features)

---

<div align="center">

**[🚀 Get Started](https://dashboard.nodemaven.com?utm_source=github&utm_medium=python_readme&utm_campaign=developer_outreach&utm_content=footer_cta)** • **[📖 Full Documentation](https://dashboard.nodemaven.com/documentation?utm_source=github&utm_medium=python_readme&utm_campaign=developer_outreach&utm_content=footer_docs)** • **[💬 Support](https://dashboard.nodemaven.com?utm_source=github&utm_medium=python_readme&utm_campaign=developer_outreach&utm_content=footer_support)**

Made with ❤️ by the NodeMaven Team

</div>
