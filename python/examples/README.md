# NodeMaven Python Examples 🚀

Comprehensive working examples demonstrating all features of the NodeMaven Python SDK.

## 📁 Available Examples

### `basic_usage.py` - Getting Started ⭐
**Perfect starting point** - Complete introduction to NodeMaven functionality:
- ✅ API client initialization and authentication
- ✅ User account information retrieval
- ✅ Available countries, regions, and cities
- ✅ Basic HTTP and SOCKS5 proxy usage
- ✅ Geo-targeted proxy connections
- ✅ Simple error handling

### `proxy_examples.py` - Configuration Guide 📖
**Comprehensive reference** - All proxy configuration options explained:
- ✅ All targeting options (country, region, city, ISP)
- ✅ HTTP and SOCKS5 configurations
- ✅ Session management and TTL settings
- ✅ Quality filtering (high, medium, low)
- ✅ Mobile vs residential proxy types
- ✅ Code snippets for common use cases

### `proxy_rotation.py` - Advanced Techniques 🔄
**Advanced proxy management** - IP rotation and session strategies:
- ✅ Automatic IP rotation strategies
- ✅ Sticky session management with TTL
- ✅ Multi-country geo-targeting
- ✅ Parallel session testing
- ✅ Performance monitoring and analysis
- ✅ Session persistence verification

### `generate_mobile_proxy.py` - Mobile Proxies 📱
**Mobile-specific examples** - Mobile proxy configurations:
- ✅ Mobile proxy targeting
- ✅ Mobile-specific session handling
- ✅ Mobile proxy URL generation
- ✅ Mobile proxy testing and validation

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Navigate to python directory
cd python/

# Activate virtual environment
source venv/bin/activate  # (macOS/Linux)
# or
venv\Scripts\activate     # (Windows)

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key
Ensure your `.env` file contains your NodeMaven API key:
```bash
NODEMAVEN_APIKEY=your_api_key_here
```

### 3. Run Examples
```bash
# Start with basic usage (recommended first)
python examples/basic_usage.py

# Explore comprehensive configurations
python examples/proxy_examples.py

# Try advanced rotation techniques
python examples/proxy_rotation.py

# Test mobile proxy features
python examples/generate_mobile_proxy.py
```

## 🎯 Features Demonstrated

| Feature | basic_usage.py | proxy_examples.py | proxy_rotation.py | generate_mobile_proxy.py |
|---------|:--------------:|:-----------------:|:-----------------:|:------------------------:|
| **API Connection** | ✅ | ✅ | ✅ | ✅ |
| **User Account Info** | ✅ | ✅ | ✅ | ✅ |
| **Basic HTTP Proxies** | ✅ | ✅ | ✅ | ✅ |
| **SOCKS5 Proxies** | ✅ | ✅ | ✅ | ✅ |
| **Geo-targeting** | ✅ | ✅ | ✅ | ✅ |
| **Session Management** | ✅ | ✅ | ✅ | ✅ |
| **TTL Configuration** | ❌ | ✅ | ✅ | ✅ |
| **IP Rotation** | ❌ | ❌ | ✅ | ❌ |
| **Parallel Sessions** | ❌ | ❌ | ✅ | ❌ |
| **Mobile Proxies** | ❌ | ✅ | ❌ | ✅ |
| **Quality Filtering** | ❌ | ✅ | ✅ | ✅ |
| **Performance Analysis** | ❌ | ❌ | ✅ | ❌ |

## 💡 Common Usage Patterns

### Simple Proxy Usage
```python
from nodemaven.utils import get_proxy_config, get_current_ip

# Get proxy configuration for US
proxies = get_proxy_config(country="us")

# Check your IP through the proxy
ip = get_current_ip(proxies=proxies)
print(f"Your US IP: {ip}")
```

### Advanced Geo-targeting
```python
from nodemaven.utils import build_proxy_url

# Target specific location with full options
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
```

### Session Persistence
```python
# Same IP for multiple requests
session_proxies = get_proxy_config(
    country="gb", 
    session="persistent_session",
    ttl="30m"
)

for i in range(3):
    ip = get_current_ip(proxies=session_proxies)
    print(f"Request {i+1}: {ip}")  # Same IP each time
```

### IP Rotation
```python
# Different IP for each request
for i in range(3):
    proxies = get_proxy_config(country="us")  # New proxy each time
    ip = get_current_ip(proxies=proxies)
    print(f"Request {i+1}: {ip}")  # Different IPs
```

### Mobile Proxies
```python
# Mobile proxy configuration
mobile_proxies = get_proxy_config(
    country="gb",
    type="mobile",
    filter="high"
)
```

## 📚 Learning Path

### 1. **Beginner**: Start with `basic_usage.py`
- Learn API basics and simple proxy usage
- Understand authentication and user info
- Try basic geo-targeting

### 2. **Intermediate**: Explore `proxy_examples.py`
- Master all configuration options
- Learn about TTL and session management
- Understand quality filtering

### 3. **Advanced**: Study `proxy_rotation.py`
- Implement rotation strategies
- Master parallel sessions
- Analyze performance metrics

### 4. **Specialized**: Try `generate_mobile_proxy.py`
- Learn mobile proxy specifics
- Understand mobile vs residential differences

## 🔧 Customization Tips

### Environment Variables
You can customize behavior with environment variables:
```bash
# Optional configuration
NODEMAVEN_PROXY_HOST=gate.nodemaven.com
NODEMAVEN_HTTP_PORT=8080
NODEMAVEN_SOCKS5_PORT=1080
REQUEST_TIMEOUT=30
DEBUG=false
```

### Error Handling
All examples include proper error handling patterns:
```python
try:
    proxies = get_proxy_config(country="us")
    response = requests.get("http://httpbin.org/ip", proxies=proxies)
    print(f"Success: {response.json()['origin']}")
except Exception as e:
    print(f"Error: {e}")
```

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Import Error` | Run from `python/` directory with activated virtual environment |
| `No API key found` | Set `NODEMAVEN_APIKEY` in your `.env` file |
| `Authentication failed` | Verify API key validity in dashboard |
| `Proxy connection failed` | Check internet connection and account status |
| `Module not found` | Install dependencies: `pip install -r requirements.txt` |

## 🎯 Best Practices Demonstrated

### 1. **Resource Management**
- Proper session reuse
- Connection pooling examples
- Timeout handling

### 2. **Error Handling**
- Graceful degradation patterns
- Retry mechanisms
- Comprehensive error logging

### 3. **Performance Optimization**
- Efficient proxy rotation
- Session persistence strategies
- Parallel request handling

### 4. **Security Considerations**
- API key management
- Credential handling
- Request validation

## 🔗 Resources

- 📖 [NodeMaven Dashboard](https://dashboard.nodemaven.com?utm_source=github&utm_medium=python_examples&utm_campaign=developer_outreach)
- 📋 [API Documentation](https://dashboard.nodemaven.com/documentation?utm_source=github&utm_medium=python_examples&utm_campaign=developer_outreach)
- 💬 [Support Chat](https://dashboard.nodemaven.com?utm_source=github&utm_medium=python_examples&utm_campaign=developer_outreach)
- 🐛 [GitHub Issues](https://github.com/nodemavencom/proxy/issues)

---

**Ready to build amazing applications with NodeMaven proxies!** 🚀 