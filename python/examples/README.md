# NodeMaven Python Examples 🚀

This directory contains comprehensive working examples for using the NodeMaven proxy API.

## 📁 Available Examples

### `basic_usage.py` - Getting Started
Complete introduction to NodeMaven functionality:
- ✅ API client initialization
- ✅ User account information
- ✅ Available countries and regions
- ✅ Basic proxy usage
- ✅ Geo-targeted proxies
- ✅ Sticky sessions demonstration

### `proxy_rotation.py` - Advanced Features
Advanced proxy management and rotation:
- ✅ IP rotation strategies
- ✅ Sticky session management
- ✅ Multi-country geo-targeting
- ✅ Parallel session testing
- ✅ Performance analysis

### `proxy_examples.py` - Configuration Guide
Comprehensive proxy configuration examples:
- ✅ All targeting options explained
- ✅ HTTP and SOCKS5 configurations
- ✅ Code snippets for common use cases
- ✅ Best practices and tips

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Make sure you're in the python/ directory
cd python/

# Activate virtual environment
source venv/bin/activate  # (macOS/Linux)
# or
venv\Scripts\activate     # (Windows)

# Ensure dependencies are installed
pip install requests python-dotenv
```

### 2. Configure API Key
Make sure your `.env` file in the parent directory contains:
```bash
NODEMAVEN_APIKEY = "your_api_key_here"
```

### 3. Run Examples
```bash
# Start with basic usage
python examples/basic_usage.py

# Try advanced rotation features
python examples/proxy_rotation.py

# Explore configuration options
python examples/proxy_examples.py
```

## 🎯 Key Features Demonstrated

| Feature | basic_usage.py | proxy_rotation.py | proxy_examples.py |
|---------|:--------------:|:-----------------:|:-----------------:|
| **API Connection** | ✅ | ✅ | ✅ |
| **User Info** | ✅ | ✅ | ✅ |
| **Basic Proxies** | ✅ | ✅ | ✅ |
| **Geo-targeting** | ✅ | ✅ | ✅ |
| **Sticky Sessions** | ✅ | ✅ | ✅ |
| **IP Rotation** | ❌ | ✅ | ❌ |
| **Parallel Sessions** | ❌ | ✅ | ❌ |
| **Configuration Guide** | ❌ | ❌ | ✅ |

## 💡 Usage Patterns

### Simple Proxy Usage
```python
from nodemaven.utils import get_proxy_config, get_current_ip

# Get proxy configuration
proxies = get_proxy_config(country="US")

# Check your IP through the proxy
ip = get_current_ip(proxies=proxies)
print(f"Your IP: {ip}")
```

### Geo-targeting
```python
# Target specific locations
us_proxies = get_proxy_config(country="US")
uk_proxies = get_proxy_config(country="GB", city="london")
ca_proxies = get_proxy_config(country="CA", region="ontario")
```

### Sticky Sessions
```python
# Same IP for multiple requests
session_proxies = get_proxy_config(session="my_session_123")

for i in range(3):
    ip = get_current_ip(proxies=session_proxies)
    print(f"Request {i+1}: {ip}")  # Same IP each time
```

### IP Rotation
```python
# Different IP for each request
for i in range(3):
    proxies = get_proxy_config(country="US")  # New proxy each time
    ip = get_current_ip(proxies=proxies)
    print(f"Request {i+1}: {ip}")  # Different IPs
```

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Import Error` | Make sure you're in the `python/` directory with activated virtual environment |
| `No API key found` | Set `NODEMAVEN_APIKEY` in your `.env` file |
| `Could not get proxy credentials` | Check API key validity in dashboard |
| `Proxy connection failed` | Check internet connection and account status |

## 📚 Next Steps

1. **Start Simple**: Run `basic_usage.py` to understand the fundamentals
2. **Explore Advanced**: Try `proxy_rotation.py` for complex scenarios
3. **Reference Guide**: Use `proxy_examples.py` as a configuration reference
4. **Build Your App**: Integrate the patterns into your own projects

## 🔗 Resources

- 📖 [API Documentation](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=python_examples)
- 🎯 [NodeMaven Website](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=python_examples_dashboard)
- 💬 [Support](https://t.me/node_maven)
- 🐛 [Issues](https://github.com/nodemavencom/proxy/issues) 