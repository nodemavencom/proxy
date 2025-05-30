# NodeMaven - Professional Proxy API 🚀

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python)](https://github.com/nodemaven/nodemaven/tree/main/python)
[![JavaScript](https://img.shields.io/badge/JavaScript-Coming%20Soon-yellow?style=for-the-badge&logo=javascript)](https://github.com/nodemavencom/proxy/issues)
[![PHP](https://img.shields.io/badge/PHP-Coming%20Soon-purple?style=for-the-badge&logo=php)](https://github.com/nodemavencom/proxy/issues)
[![Go](https://img.shields.io/badge/Go-Coming%20Soon-cyan?style=for-the-badge&logo=go)](https://github.com/nodemavencom/proxy/issues)

[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![API](https://img.shields.io/badge/API-v2-orange?style=for-the-badge)](https://dashboard.nodemaven.com/documentation/v2/swagger?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=api_docs)
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-success?style=for-the-badge)](https://dashboard.nodemaven.com/dashboard?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=dashboard_link)

> **Enterprise-Grade Residential & Mobile Proxy API** - Global coverage, sticky sessions, and advanced geo-targeting for developers and businesses.

## 🎯 Why NodeMaven?

- 🌍 **164+ Countries** - Global proxy coverage with 1,455+ regions and 6,811+ cities
- 🏠 **Residential IPs** - Real ISP addresses from 63,726+ providers worldwide
- 📱 **Mobile Proxies** - 4G/5G connections for mobile-specific applications
- 🔒 **HTTP & SOCKS5** - Full protocol support for any use case
- 📍 **Precision Targeting** - Country, region, city, and ISP-level targeting
- 🔄 **Sticky Sessions** - Maintain same IP for session duration
- ⚡ **99.9% Uptime** - Enterprise-grade infrastructure and reliability
- 📊 **Real-time Analytics** - Monitor usage, performance, and success rates

## 🚀 Quick Start (30 seconds!)

### 1. Get Your API Key 
1. **Sign up**: [NodeMaven Dashboard](https://dashboard.nodemaven.com/accounts/signup?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=signup_link)
2. **Get API key**: [Profile → API Keys](https://dashboard.nodemaven.com/profile?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=api_key)

### 2. Choose Your Language

#### 🐍 **Python (Ready to Use!)**
```bash
cd python/
pip install requests python-dotenv  # Optional dependencies
python quick_test.py                # Instant test!
```

#### 🟨 **JavaScript (Coming Soon)**
```bash
cd javascript/
npm install @nodemaven/sdk
```

#### 🟣 **PHP (Coming Soon)**
```bash
cd php/
composer require nodemaven/sdk
```

#### 🔵 **Go (Coming Soon)**
```bash
cd go/
go get github.com/nodemaven/sdk
```

### 3. Set Your Credentials
```bash
# Copy example environment file
cp env.example .env

# Edit with your credentials:
NODEMAVEN_APIKEY = "your_api_key_here"
NODEMAVEN_USERNAME = "your_username_here" 
NODEMAVEN_PASSWORD = "your_password_here"
```

### 4. Test Your Connection
```bash
# Python
cd python && python quick_test.py

# Or run advanced examples
python examples/proxy_rotation.py    # Full rotation demo
python examples/basic_usage.py       # Simple usage patterns
```

## 📁 Repository Structure & File Guide

```
nodemaven/
├── 🐍 python/                    # ✅ READY - Full Python SDK
│   ├── 📦 nodemaven/             # Core SDK package
│   │   ├── client.py             # Main API client class
│   │   ├── utils.py              # Proxy configuration utilities
│   │   ├── exceptions.py         # Custom exception classes
│   │   └── __init__.py           # Package initialization
│   ├── 📚 examples/              # Working examples
│   │   ├── proxy_rotation.py     # 🔥 Advanced rotation demo
│   │   ├── basic_usage.py        # Simple getting started guide
│   │   ├── proxy_examples.py     # Common usage patterns
│   │   └── README.md             # Examples documentation
│   ├── quick_test.py             # 🚀 Instant setup test
│   ├── setup.py                  # PyPI package setup
│   ├── requirements.txt          # Python dependencies
│   └── README.md                 # Python SDK documentation
│
├── 🟨 javascript/                # 🚧 COMING SOON
│   └── README.md                 # JavaScript roadmap
│
├── 🟣 php/                       # 🚧 COMING SOON  
│   └── README.md                 # PHP roadmap
│
├── 🔵 go/                        # 🚧 COMING SOON
│   └── README.md                 # Go roadmap
│
├── 🛠️ tools/                     # Utilities & Location Database
│   ├── update_locations.py       # Download location database
│   └── locations.json            # 164 countries, 6,811+ cities
│
├── 🎨 assets/                    # Images & Resources (empty)
├── 📚 docs/                      # Documentation (empty)
├── env.example                   # Environment template
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
└── readme.md                     # 📖 This file

Note: Create `.env` from `env.example` with your credentials
```

## 🔧 Key Components Explained

### 📦 **Python SDK (`python/`)**
**Status**: ✅ **Production Ready**

| File | Purpose | What It Does |
|------|---------|--------------|
| `client.py` | Core API Client | Handles authentication, API calls, user management |
| `utils.py` | Proxy Configuration | Creates proxy URLs, handles geo-targeting |
| `exceptions.py` | Error Handling | Custom exceptions for API errors |
| `quick_test.py` | **🚀 Instant Test** | **Test your setup in 30 seconds** |
| `requirements.txt` | Dependencies | Optional packages (requests, python-dotenv) |

### 📚 **Examples (`python/examples/`)**

| Example | Demonstrates | Best For |
|---------|-------------|----------|
| **`proxy_rotation.py`** | **🔥 Advanced Features** | **IP rotation, sticky sessions, geo-targeting** |
| `basic_usage.py` | Simple Usage | Getting started, basic requests |
| `proxy_examples.py` | Common Patterns | Real-world usage scenarios |

### 🛠️ **Tools (`tools/`)**

| Tool | Purpose | Usage |
|------|---------|-------|
| `update_locations.py` | Location Database | Download 164 countries, 6,811+ cities |
| `locations.json` | Location Data | Offline lookup for targeting |

```bash
# Download latest location data
cd tools/
python update_locations.py

# Show statistics  
python update_locations.py info

# Search locations
python update_locations.py search "los angeles"
```

## 💡 Usage Examples

### 🔄 **IP Rotation**
```python
from nodemaven import NodeMavenClient
from nodemaven.utils import get_proxy_config

client = NodeMavenClient()

# Different IP for each request
for i in range(5):
    proxies = get_proxy_config(country="US")
    response = requests.get("https://httpbin.org/ip", proxies=proxies)
    print(f"Request {i+1}: {response.json()['origin']}")
```

### 📌 **Sticky Sessions**
```python
# Same IP for multiple requests
session_id = "my_session_123"
proxies = get_proxy_config(session=session_id)

# All requests use same IP
for i in range(3):
    response = requests.get("https://httpbin.org/ip", proxies=proxies)
    print(f"Request {i+1}: {response.json()['origin']}")  # Same IP!
```

### 🌍 **Geo-Targeting**
```python
# Target specific countries
us_proxies = get_proxy_config(country="US")
uk_proxies = get_proxy_config(country="GB") 
de_proxies = get_proxy_config(country="DE")

# Target specific cities
london_proxies = get_proxy_config(country="GB", city="london")
nyc_proxies = get_proxy_config(country="US", region="new york", city="new york")
```

### 🔒 **SOCKS5 Support**
```python
from nodemaven.utils import get_socks5_proxy

socks_proxies = get_socks5_proxy(country="CA")
response = requests.get("https://httpbin.org/ip", proxies=socks_proxies)
```

## 🎯 Use Cases

| Use Case | Example | Targeting |
|----------|---------|-----------|
| **Web Scraping** | E-commerce data | `country="US", filter="fast"` |
| **Ad Verification** | Check ad placements | `country="GB", city="london"` |
| **Price Monitoring** | Compare regional prices | `country="DE", region="bavaria"` |
| **Social Media** | Multi-account management | `session="account_1"` |
| **SEO Research** | Localized search results | `country="CA", city="toronto"` |
| **Market Research** | Geographic analysis | `country="FR", region="paris"` |

## 🔧 Environment Configuration

### Required Variables
```bash
NODEMAVEN_APIKEY = "your_api_key_here"      # From dashboard
NODEMAVEN_USERNAME = "your_username_here"    # Proxy username  
NODEMAVEN_PASSWORD = "your_password_here"    # Proxy password
```

### Optional Variables
```bash
NODEMAVEN_BASE_URL = "https://api.nodemaven.com"     # API endpoint
NODEMAVEN_PROXY_HOST = "gate.nodemaven.com"          # Proxy host
NODEMAVEN_HTTP_PORT = "8080"                         # HTTP port
NODEMAVEN_SOCKS5_PORT = "1080"                       # SOCKS5 port
REQUEST_TIMEOUT = "30"                               # Request timeout
```

## 📊 Testing & Verification

### 🚀 **Quick Test**
```bash
cd python/
python quick_test.py    # Tests API connection + proxy
```

### 🔥 **Advanced Demo**
```bash
python examples/proxy_rotation.py    # Full feature demonstration
```

### 📦 **Package Installation**
```bash
cd python/
pip install -e .        # Install as development package
```

## 📚 Documentation & Resources

| Resource | Description | Link |
|----------|-------------|------|
| 🔗 **API Reference** | Complete API documentation | [View Docs](https://dashboard.nodemaven.com/documentation/v2/swagger?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=api_reference) |
| 🎯 **Dashboard** | Manage account & usage | [Open Dashboard](https://dashboard.nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=dashboard) |
| 💬 **Support** | 24/7 developer support | [Get Help](https://t.me/node_maven) |
| 🐛 **Issues** | Report bugs | [GitHub Issues](https://github.com/nodemavencom/proxy/issues) |

## 💰 Pricing (prices may vary)

| Plan | Price | Traffic | Features |
|------|-------|---------|----------|
| **Starter** | $50/month | 5GB | Basic targeting, HTTP/SOCKS5 |
| **Professional** | $200/month | 25GB | Advanced targeting, Analytics |
| **Enterprise** | Custom | Unlimited | Dedicated IPs, Priority support |

[View Full Pricing](https://nodemaven.com/pricing?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=pricing_table) • [Start Free Trial](https://dashboard.nodemaven.com/register/?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=free_trial)

## 🌟 Advanced Features

### Targeting Options
- **Country**: 164+ countries available
- **Region**: 1,455+ regions for precise targeting  
- **City**: 6,811+ cities worldwide
- **ISP**: 63,726+ internet service providers
- **Session**: Sticky sessions for consistent IPs

### Protocols
- **HTTP/HTTPS**: Standard web proxy protocol
- **SOCKS5**: Full TCP/UDP proxy support  
- **Authentication**: Username/password and IP whitelist

### Management
- **Sub-users**: Create and manage multiple proxy users
- **IP Whitelist**: Secure access control
- **Real-time Stats**: Monitor usage and performance
- **API Access**: Full programmatic control

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Add Language Support**: Implement SDKs for JavaScript, PHP, Go
2. **Improve Examples**: Add more use cases and tutorials  
3. **Enhance Documentation**: Better guides and explanations
4. **Report Issues**: Found a bug? [Create an issue](https://github.com/nodemavencom/proxy/issues)
5. **Feature Requests**: Suggest new features or improvements

## 🚨 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `No API key found` | Set `NODEMAVEN_APIKEY` in `.env` file |
| `Could not get proxy credentials` | Check API key validity in dashboard |
| `Proxy connection failed` | Verify username/password are correct |
| `403 Forbidden` | API key expired or invalid |
| `503 Service Unavailable` | Temporary network issue, retry |

### Getting Help

1. **Check your credentials** in the [dashboard](https://dashboard.nodemaven.com/profile/)
2. **Run quick test**: `python quick_test.py`
3. **Check API status**: [Status Page](https://status.nodemaven.com)

## 📞 Support

- 📱 **Telegram**: [t.me/node_maven](https://t.me/node_maven)
- 💬 **Live Chat**: [Dashboard Support](https://dashboard.nodemaven.com/support?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=live_chat)
- 📖 **Documentation**: [API Docs](https://dashboard.nodemaven.com/documentation?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=documentation)
- 🐛 **Issues**: [GitHub Issues](https://github.com/nodemavencom/proxy/issues)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**[🚀 Get Started](https://dashboard.nodemaven.com/register?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=footer_cta)** • **[📖 Documentation](https://dashboard.nodemaven.com/documentation?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=footer_docs)** • **[💬 Support](https://dashboard.nodemaven.com/support?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=footer_support)**

Made with ❤️ by the NodeMaven Team

</div>
