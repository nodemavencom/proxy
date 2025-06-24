# NodeMaven - 🚀 Professional Proxy API 🚀

[![Python](https://img.shields.io/badge/Python-Ready-brightgreen?style=for-the-badge&logo=python)](https://github.com/nodemavencom/proxy/tree/main/proxy/python)
[![JavaScript](https://img.shields.io/badge/JavaScript-Ready-brightgreen?style=for-the-badge&logo=javascript)](https://github.com/nodemavencom/proxy/tree/main/proxy/javascript)
[![PHP](https://img.shields.io/badge/PHP-Ready-brightgreen?style=for-the-badge&logo=php)](https://github.com/nodemavencom/proxy/tree/main/proxy/php)
[![Go](https://img.shields.io/badge/Go-Ready-brightgreen?style=for-the-badge&logo=go)](https://github.com/nodemavencom/proxy/tree/main/proxy/go)

[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![API](https://img.shields.io/badge/API-v2-orange?style=for-the-badge)](https://dashboard.nodemaven.com?utm_source=github&utm_medium=readme&utm_campaign=developer_outreach&utm_content=api_docs)
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-success?style=for-the-badge)](https://dashboard.nodemaven.com?utm_source=github&utm_medium=readme&utm_campaign=developer_outreach&utm_content=dashboard_link)

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

## ✅ Production-Ready SDKs

All our SDKs are production-ready with comprehensive testing, documentation, and examples:

### 🐍 **Python** - Full-featured & Tested
```python
from nodemaven import Client

client = Client()
proxy = client.getProxyConfig({'country': 'US'})
```

### 🟢 **JavaScript/Node.js** - Zero Dependencies
```javascript
const { NodeMavenClient } = require('@nodemaven/sdk');

const client = new NodeMavenClient();
const proxy = await client.getProxyConfig({ country: 'US' });
```

### 🟣 **PHP** - Modern PHP 8.0+
```php
use NodeMaven\Client;

$client = new Client();
$proxy = $client->getProxyConfig(['country' => 'US']);
```

### 🔷 **Go** - High Performance
```go
client, _ := nodemaven.NewClient(&nodemaven.Config{})
proxy, _ := client.GetProxyConfig(&nodemaven.ProxyOptions{Country: "US"})
```

## 🚀 Quick Start (5 minutes!)

### Step 1: Get Your API Key 🔑
1. **Sign up**: [NodeMaven Dashboard](https://dashboard.nodemaven.com?utm_source=github&utm_medium=readme&utm_campaign=developer_outreach&utm_content=signup_link)
2. **Get API key**: From your dashboard profile

### Step 2: Choose Your Language

<details>
<summary><b>🐍 Python Setup</b></summary>

```bash
# Clone repository
git clone https://github.com/nodemavencom/proxy.git
cd proxy/python

# Setup environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env: NODEMAVEN_APIKEY=your_api_key_here

# Test setup
python quick_test.py
```
</details>

<details>
<summary><b>🟢 JavaScript/Node.js Setup</b></summary>

```bash
# Clone repository
git clone https://github.com/nodemavencom/proxy.git
cd proxy/javascript

# Install dependencies
npm install

# Configure API key
export NODEMAVEN_APIKEY="your_api_key_here"
# or create .env file

# Test setup
node quick_test.js
```
</details>

<details>
<summary><b>🟣 PHP Setup</b></summary>

```bash
# Clone repository
git clone https://github.com/nodemavencom/proxy.git
cd proxy/php

# Install dependencies
composer install

# Configure API key
cp .env.example .env
# Edit .env: NODEMAVEN_APIKEY=your_api_key_here

# Test setup
php quick_test.php
```
</details>

<details>
<summary><b>🔷 Go Setup</b></summary>

```bash
# Clone repository
git clone https://github.com/nodemavencom/proxy.git
cd proxy/go

# Initialize module
go mod init your-project

# Install SDK
go get github.com/nodemavencom/proxy/go/nodemaven

# Configure API key
export NODEMAVEN_APIKEY="your_api_key_here"

# Test setup
go run examples/basic_usage.go
```
</details>

## 💡 Key Features & Examples

### 🔄 **IP Rotation**
Rotate IPs for each request to avoid detection:

**Python:**
```python
for i in range(5):
    proxy = client.getProxyConfig({'country': 'US'})
    # Each call gets a different IP
```

**JavaScript:**
```javascript
for (let i = 0; i < 5; i++) {
    const proxy = await client.getProxyConfig({ country: 'US' });
    // Each call gets a different IP
}
```

### 📌 **Sticky Sessions**
Maintain the same IP across multiple requests:

**PHP:**
```php
$sessionId = 'user_session_' . uniqid();
$proxy = $client->getProxyConfig([
    'country' => 'US',
    'session' => $sessionId
]);
// All requests use the same IP
```

**Go:**
```go
proxy, _ := client.GetProxyConfig(&nodemaven.ProxyOptions{
    Country: "US",
    Session: "my_session_123",
})
// All requests use the same IP
```

### 🌍 **Geo-Targeting**
Target specific locations with precision:

```python
# Country level
us_proxy = client.getProxyConfig({'country': 'US'})

# City level  
nyc_proxy = client.getProxyConfig({
    'country': 'US',
    'city': 'New York'
})

# ISP level
verizon_proxy = client.getProxyConfig({
    'country': 'US',
    'isp': 'Verizon'
})
```

## 🎯 Use Cases

| Use Case | Best Language | Example Configuration |
|----------|---------------|---------------------|
| **Web Scraping** | Python | `{'country': 'US', 'session': 'scraper_1'}` |
| **API Testing** | JavaScript | `{country: 'GB', city: 'London'}` |
| **WordPress/PHP** | PHP | `['country' => 'CA', 'region' => 'Ontario']` |
| **High Performance** | Go | `&ProxyOptions{Country: "DE", Session: "worker_1"}` |
| **Ad Verification** | Any | Target specific cities for localized ads |
| **Price Monitoring** | Any | Rotate between countries for pricing data |

## 📁 Repository Structure

```
nodemaven/
├── 🐍 proxy/python/               # ✅ Python SDK (Fully Tested)
│   ├── 📦 nodemaven/              # Core SDK package
│   ├── 📚 examples/               # Working examples
│   ├── 🧪 tests/                  # Comprehensive tests
│   ├── 🔍 ip_checker/             # IP utilities
│   ├── 🛠️ tools/                 # Location management
│   ├── quick_test.py              # Setup validation
│   └── README.md                  # Full documentation
│
├── 🟢 proxy/javascript/            # ✅ JavaScript/Node.js SDK
│   ├── 📦 src/                    # Core SDK files
│   ├── 📚 examples/               # Usage examples
│   ├── quick_test.js              # Setup validation
│   └── README.md                  # Full documentation
│
├── 🟣 proxy/php/                   # ✅ PHP SDK (8.0+)
│   ├── 📦 src/                    # PSR-4 compliant code
│   ├── 📚 examples/               # Usage examples
│   ├── composer.json              # Package management
│   ├── quick_test.php             # Setup validation
│   └── README.md                  # Full documentation
│
├── 🔷 proxy/go/                    # ✅ Go SDK
│   ├── 📦 nodemaven/              # Go package
│   ├── 📚 examples/               # Usage examples
│   └── README.md                  # Full documentation
│
├── .gitignore                     # Git configuration
├── LICENSE                        # MIT License
└── README.md                      # 📖 This file
```

## ⚙️ Configuration

### Required: API Key Only
```bash
# Set in environment or .env file
NODEMAVEN_APIKEY=your_api_key_here
```

### Optional: Advanced Configuration
```bash
NODEMAVEN_BASE_URL=https://dashboard.nodemaven.com
NODEMAVEN_PROXY_HOST=gate.nodemaven.com
NODEMAVEN_HTTP_PORT=8080
NODEMAVEN_SOCKS5_PORT=1080
REQUEST_TIMEOUT=30
```

## 🧪 Testing & Validation

Each SDK includes a quick test script:

```bash
# Python
python proxy/python/quick_test.py

# JavaScript  
node proxy/javascript/quick_test.js

# PHP
php proxy/php/quick_test.php

# Go
go run proxy/go/examples/basic_usage.go
```

**Expected Output:**
```
✅ API Key found
✅ Connected! User: your@email.com  
✅ Proxy credentials obtained
✅ Proxy working! IP: xxx.xxx.xxx.xxx
🎉 Setup Complete!
```

## 🚨 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `No API key found` | Set `NODEMAVEN_APIKEY` in environment or `.env` file |
| `Could not get proxy credentials` | Verify API key is valid in [dashboard](https://dashboard.nodemaven.com?utm_source=github&utm_medium=readme&utm_campaign=developer_outreach&utm_content=troubleshooting) |
| `Connection failed` | Check internet connectivity and firewall settings |
| `Import/require errors` | Ensure dependencies are installed and virtual environment is active |

### Getting Help
- 📚 **Documentation**: [Complete API Docs](https://dashboard.nodemaven.com/documentation?utm_source=github&utm_medium=readme&utm_campaign=developer_outreach&utm_content=docs_help)
- 💬 **Telegram**: [@node_maven](https://t.me/node_maven)
- 🐛 **Issues**: [GitHub Issues](https://github.com/nodemavencom/proxy/issues)
- 📧 **Email**: [support@nodemaven.com](mailto:support@nodemaven.com)

## 💰 Pricing

| Plan | Monthly Price | Traffic | Features |
|------|---------------|---------|----------|
| **Starter** | $50 | 5GB | All countries, HTTP/SOCKS5 |
| **Professional** | $200 | 25GB | Advanced targeting, Analytics |
| **Enterprise** | Custom | Unlimited | Dedicated IPs, Priority support |

[**View Full Pricing**](https://dashboard.nodemaven.com/pricing?utm_source=github&utm_medium=readme&utm_campaign=developer_outreach&utm_content=pricing_table) • [**Start Free Trial**](https://dashboard.nodemaven.com/register?utm_source=github&utm_medium=readme&utm_campaign=developer_outreach&utm_content=free_trial)

## 🤝 Contributing

We welcome contributions in all languages! Help us improve:

1. **Add Features**: Enhance existing SDKs with new functionality
2. **Improve Examples**: Add more real-world use cases
3. **Documentation**: Better guides and explanations
4. **Bug Reports**: [Create an issue](https://github.com/nodemavencom/proxy/issues) for any bugs
5. **Language Support**: Suggest additional language implementations

### Contribution Guidelines
- Fork the repository and create a feature branch
- Maintain consistent code style within each language
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📚 Resources & Links

| Resource | Description | Link |
|----------|-------------|------|
| 🎯 **Dashboard** | Account management & analytics | [dashboard.nodemaven.com](https://dashboard.nodemaven.com?utm_source=github&utm_medium=readme&utm_campaign=developer_outreach&utm_content=dashboard_resource) |
| 📖 **API Documentation** | Complete API reference | [API Docs](https://dashboard.nodemaven.com/documentation?utm_source=github&utm_medium=readme&utm_campaign=developer_outreach&utm_content=api_docs_resource) |
| 💬 **Support Chat** | 24/7 developer support | [Live Chat](https://dashboard.nodemaven.com?utm_source=github&utm_medium=readme&utm_campaign=developer_outreach&utm_content=support_chat) |
| 📱 **Telegram** | Community & quick help | [@node_maven](https://t.me/node_maven) |
| 🐛 **Bug Reports** | Report issues | [GitHub Issues](https://github.com/nodemavencom/proxy/issues) |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**[🚀 Get Started](https://dashboard.nodemaven.com?utm_source=github&utm_medium=readme&utm_campaign=developer_outreach&utm_content=footer_cta)** • **[📖 Documentation](https://dashboard.nodemaven.com/documentation?utm_source=github&utm_medium=readme&utm_campaign=developer_outreach&utm_content=footer_docs)** • **[💬 Support](https://dashboard.nodemaven.com?utm_source=github&utm_medium=readme&utm_campaign=developer_outreach&utm_content=footer_support)**

Made with ❤️ by the NodeMaven Team

</div>
