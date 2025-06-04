# NodeMaven - Professional Proxy API 🚀

[![Python](https://img.shields.io/badge/Python-3.7%2B%20✅%20TESTED-brightgreen?style=for-the-badge&logo=python)](https://github.com/nodemavencom/proxy/tree/main/python)
[![JavaScript](https://img.shields.io/badge/JavaScript-Coming%20Soon-yellow?style=for-the-badge&logo=javascript)](https://github.com/nodemavencom/proxy/issues)
[![PHP](https://img.shields.io/badge/PHP-Coming%20Soon-purple?style=for-the-badge&logo=php)](https://github.com/nodemavencom/proxy/issues)
[![Go](https://img.shields.io/badge/Go-Coming%20Soon-cyan?style=for-the-badge&logo=go)](https://github.com/nodemavencom/proxy/issues)

[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![API](https://img.shields.io/badge/API-v2-orange?style=for-the-badge)](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=api_docs)
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-success?style=for-the-badge)](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=dashboard_link)
[![Tests](https://img.shields.io/badge/Tests-12%2F12%20Passing-brightgreen?style=for-the-badge&logo=github-actions)](https://github.com/nodemavencom/proxy/actions)

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

## 🚀 Quick Start (5 minutes!)

### Step 1: Get Your API Key 🔑
1. **Sign up**: [NodeMaven Website](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=signup_link)
2. **Get API key**: [Dashboard Profile](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=api_key)

### Step 2: Setup Environment 📁

```bash
# Clone or download this repository
git clone https://github.com/nodemavencom/proxy.git
cd proxy

# Copy environment template
cd python && cp env.example .env

# Edit .env file and add your API key:
# NODEMAVEN_APIKEY = "your_api_key_here"
```

### Step 3: Choose Your Language & Setup

#### 🐍 **Python (Ready to Use!)**

**For macOS/Linux:**
```bash
cd python/

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install requests python-dotenv

# Test your setup
python quick_test.py
```

**For Windows:**
```bash
cd python/

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install requests python-dotenv

# Test your setup
python quick_test.py
```

**If something goes wrong:**
```bash
# Delete virtual environment and start over
rm -rf venv  # (macOS/Linux)
rmdir /s venv  # (Windows)

# Then repeat the steps above
```

## 🧪 Testing Status

### ✅ Python Package - FULLY TESTED & VERIFIED

- **🎯 12/12 Tests Passing** - Complete test suite with pytest
- **🔌 API Client Verified** - All endpoints tested and working  
- **🌐 Proxy Functionality** - US & UK proxies confirmed working
- **📍 IP Checker Tools** - Multiple service integration tested
- **📋 Examples Validated** - All syntax checked and working
- **📦 Package Ready** - PyPI-ready setup verified
- **⚡ Console Scripts** - `nodemaven-test` command working
- **📚 Requirements Organized** - Separated dev/prod dependencies

**Last Tested:** December 2024  
**Test Coverage:** Core functionality, API integration, proxy operations, IP checking

### 🚧 Other Languages
- **JavaScript**: Basic implementation available, needs testing
- **PHP/Go**: Coming soon

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

### Step 4: Test Your Connection ✅

```bash
# Make sure you're in the python/ directory with activated virtual environment
cd python/
source venv/bin/activate  # (macOS/Linux) or venv\Scripts\activate (Windows)

# Run the quick test
python quick_test.py
```

**Expected output:**
```
🚀 NodeMaven Quick Test Starting...
✅ API Key found: your_api_key_here...
✅ Connected! User: your@email.com
✅ Proxy credentials obtained!
✅ Proxy working! Your IP: xxx.xxx.xxx.xxx
🎉 Quick Test Complete!
```

## 🎉 You're Ready! Next Steps

### Run Examples
```bash
# Basic usage patterns
python examples/basic_usage.py

# Advanced IP rotation and geo-targeting
python examples/proxy_rotation.py

# Common usage scenarios
python examples/proxy_examples.py
```

### Use in Your Code
```python
from nodemaven.utils import get_proxy_config, get_current_ip

# Simple proxy usage (auto-gets credentials from API)
proxies = get_proxy_config(country="US")
ip = get_current_ip(proxies=proxies)
print(f"Your proxy IP: {ip}")
```

## 💡 Key Features & Examples

### 🔄 **IP Rotation**
```python
from nodemaven.utils import get_proxy_config, get_current_ip

# Different IP for each request
for i in range(5):
    proxies = get_proxy_config(country="US")
    ip = get_current_ip(proxies=proxies)
    print(f"Request {i+1}: {ip}")
```

### 📌 **Sticky Sessions**
```python
from nodemaven.utils import get_proxy_config, get_current_ip

# Same IP for multiple requests
session_id = "my_session_123"
proxies = get_proxy_config(session=session_id)

# All requests use same IP
for i in range(3):
    ip = get_current_ip(proxies=proxies)
    print(f"Request {i+1}: {ip}")  # Same IP!
```

### 🌍 **Geo-Targeting**
```python
from nodemaven.utils import get_proxy_config

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
from nodemaven.utils import get_socks5_proxy, get_current_ip

socks_proxies = {'http': get_socks5_proxy(country="CA"), 'https': get_socks5_proxy(country="CA")}
ip = get_current_ip(proxies=socks_proxies)
print(f"Your IP: {ip}")
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

## 📁 Repository Structure

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
│   ├── 🧪 tests/                 # Simple test files
│   │   ├── test_client.py        # API client tests
│   │   ├── test_utils.py         # Utility function tests
│   │   ├── test_ip_checker.py    # IP checker tests
│   │   ├── test_proxy_functionality.py # Proxy operation tests
│   │   └── README.md             # Test documentation
│   ├── 🔍 ip_checker/            # IP checking utilities
│   │   ├── ipapi_checker.py      # IP-API.com checker
│   │   ├── ipinfo_checker.py     # IPInfo.io checker
│   │   ├── __init__.py           # Package initialization
│   │   └── README.md             # IP checker documentation
│   ├── 🛠️ tools/                 # Utilities & Location Database
│   │   ├── update_locations.py   # Location data updater
│   │   ├── locations.json        # Cached location data
│   │   └── README.md             # Tools documentation
│   ├── ip_checker.py             # Enhanced IP checker
│   ├── quick_test.py             # 🚀 Instant setup test
│   ├── setup.py                  # PyPI package setup
│   ├── requirements.txt          # Core dependencies
│   ├── requirements-dev.txt      # Development dependencies (testing, linting)
│   ├── env.example               # Environment template
│   └── README.md                 # Python SDK documentation
│
├── 🟨 javascript/                # 🚧 COMING SOON
├── 🟣 php/                       # 🚧 COMING SOON  
├── 🔵 go/                        # 🚧 COMING SOON
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
└── readme.md                     # 📖 This file
```

## 🔧 Configuration

### Required Configuration
```bash
# Only one variable needed in .env file:
NODEMAVEN_APIKEY = "your_api_key_here"
```

**That's it!** The SDK automatically:
- ✅ Fetches your proxy username/password from the API
- ✅ Configures proxy endpoints and ports
- ✅ Handles authentication and targeting

### Optional Configuration
```bash
# Advanced users only (usually not needed):
# NODEMAVEN_BASE_URL = "https://api.nodemaven.com"
# NODEMAVEN_PROXY_HOST = "gate.nodemaven.com"
# NODEMAVEN_HTTP_PORT = "8080"
# NODEMAVEN_SOCKS5_PORT = "1080"
# REQUEST_TIMEOUT = "30"
```

## 🚨 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `No API key found` | Set `NODEMAVEN_APIKEY` in `.env` file |
| `Could not get proxy credentials` | Check API key validity in dashboard |
| `Import Error` | Activate virtual environment: `source venv/bin/activate` |
| `Module not found` | Install dependencies: `pip install requests python-dotenv` |
| `Permission denied` | Make sure virtual environment is activated |

### Virtual Environment Issues

**If virtual environment doesn't work:**
```bash
# Delete and recreate
rm -rf venv  # (macOS/Linux) or rmdir /s venv (Windows)
python3 -m venv venv  # (macOS/Linux) or python -m venv venv (Windows)
source venv/bin/activate  # (macOS/Linux) or venv\Scripts\activate (Windows)
pip install requests python-dotenv
```

**Check if virtual environment is active:**
```bash
which python  # Should show path with 'venv' in it
```

## 💰 Pricing

| Plan | Price | Traffic | Features |
|------|-------|---------|----------|
| **Starter** | $50/month | 5GB | Basic targeting, HTTP/SOCKS5 |
| **Professional** | $200/month | 25GB | Advanced targeting, Analytics |
| **Enterprise** | Custom | Unlimited | Dedicated IPs, Priority support |

[View Full Pricing](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=pricing_table) • [Start Free Trial](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=free_trial)

## 📚 Documentation & Resources

| Resource | Description | Link |
|----------|-------------|------|
| 🔗 **API Reference** | Complete API documentation | [View Docs](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=api_reference) |
| 🎯 **Dashboard** | Manage account & usage | [Open Dashboard](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=dashboard) |
| 💬 **Support** | 24/7 developer support | [Get Help](https://t.me/node_maven) |
| 🐛 **Issues** | Report bugs | [GitHub Issues](https://github.com/nodemavencom/proxy/issues) |

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/nodemavencom/proxy.git
cd proxy/python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # (Linux/Mac) or venv\Scripts\activate (Windows)

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/ -v

# Run code quality checks
black --check .
flake8 .
mypy nodemaven/
```

### Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=nodemaven --cov-report=html

# Run specific test files
python -m pytest tests/test_client.py -v
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Add Language Support**: Implement SDKs for JavaScript, PHP, Go
2. **Improve Examples**: Add more use cases and tutorials  
3. **Enhance Documentation**: Better guides and explanations
4. **Report Issues**: Found a bug? [Create an issue](https://github.com/nodemavencom/proxy/issues)
5. **Feature Requests**: Suggest new features or improvements

### Contribution Guidelines
- Fork the repository and create a feature branch
- Write tests for new functionality
- Ensure all tests pass (`python -m pytest tests/ -v`)
- Follow code style guidelines (`black` and `flake8`)
- Update documentation as needed

## 📞 Support

- 📱 **Telegram**: [t.me/node_maven](https://t.me/node_maven)
- 💬 **Live Chat**: [Dashboard Support](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=live_chat)
- 📖 **Documentation**: [API Docs](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=documentation)
- 🐛 **Issues**: [GitHub Issues](https://github.com/nodemavencom/proxy/issues)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**[🚀 Get Started](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=footer_cta)** • **[📖 Documentation](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=footer_docs)** • **[💬 Support](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=footer_support)**

Made with ❤️ by the NodeMaven Team

</div>
