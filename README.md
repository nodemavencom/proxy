# NodeMaven - 🚀 Professional Proxy API 🚀

[![Python](https://img.shields.io/badge/Python-Testing-yellow?style=for-the-badge&logo=python)](https://github.com/nodemavencom/proxy/tree/main/proxy/python)
[![JavaScript](https://img.shields.io/badge/JavaScript-Testing-yellow?style=for-the-badge&logo=javascript)](https://github.com/nodemavencom/proxy/tree/main/proxy/javascript)
[![PHP](https://img.shields.io/badge/PHP-Testing-yellow?style=for-the-badge&logo=php)](https://github.com/nodemavencom/proxy/tree/main/proxy/php)
[![Go](https://img.shields.io/badge/Go-Testing-yellow?style=for-the-badge&logo=go)](https://github.com/nodemavencom/proxy/tree/main/proxy/go)

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

## 🧪 SDK Development Status

All our SDKs are currently in **active testing phase** with basic functionality implemented:

### 🐍 **Python** - In Testing
```python
from nodemaven import Client

client = Client()
proxy = client.getProxyConfig({'country': 'US'})
```

### 🟢 **JavaScript/Node.js** - In Testing
```javascript
const { NodeMavenClient } = require('@nodemaven/sdk');

const client = new NodeMavenClient();
const proxy = await client.getProxyConfig({ country: 'US' });
```

### 🟣 **PHP** - In Testing
```php
use NodeMaven\Client;

$client = new Client();
$proxy = $client->getProxyConfig(['country' => 'US']);
```

### 🔷 **Go** - In Testing
```go
client, _ := nodemaven.NewClient(&nodemaven.Config{})
proxy, _ := client.GetProxyConfig(&nodemaven.ProxyOptions{Country: "US"})
```

## 🚀 Quick Start

### Step 1: Get Your API Key 🔑
1. **Sign up**: [NodeMaven Dashboard](https://dashboard.nodemaven.com?utm_source=github&utm_medium=readme&utm_campaign=developer_outreach&utm_content=signup_link)
2. **Get API key**: From your dashboard profile

### Step 2: Test an SDK

<details>
<summary><b>🐍 Python Testing</b></summary>

```bash
cd python
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

pip install -r requirements.txt
export NODEMAVEN_APIKEY="your_api_key_here"
python quick_test.py
```
</details>

<details>
<summary><b>🟢 JavaScript Testing</b></summary>

```bash
cd javascript
npm install
export NODEMAVEN_APIKEY="your_api_key_here"
node quick_test.js
```
</details>

<details>
<summary><b>🟣 PHP Testing</b></summary>

```bash
cd php
composer install
export NODEMAVEN_APIKEY="your_api_key_here"
php quick_test.php
```
</details>

<details>
<summary><b>🔷 Go Testing</b></summary>

```bash
cd go
go mod tidy
export NODEMAVEN_APIKEY="your_api_key_here"
go run examples/basic_usage.go
```
</details>

## 📁 Repository Structure

```
nodemaven-proxy/
├── 🐍 python/                     # Python SDK (Testing)
│   ├── src/nodemaven/             # Core package
│   ├── examples/                  # Basic examples
│   └── quick_test.py              # Setup test
│
├── 🟢 javascript/                  # JavaScript SDK (Testing)
│   ├── src/                       # Core files
│   ├── examples/                  # Basic examples
│   └── quick_test.js              # Setup test
│
├── 🟣 php/                         # PHP SDK (Testing)
│   ├── src/                       # Core classes
│   ├── examples/                  # Basic examples
│   └── quick_test.php             # Setup test
│
├── 🔷 go/                          # Go SDK (Testing)
│   ├── nodemaven/                 # Go package
│   ├── examples/                  # Basic examples
│   └── README.md                  # Go-specific docs
│
└── README.md                      # This file
```

## 💡 Basic Usage Examples

### 🔄 **IP Rotation**
```python
for i in range(3):
    proxy = client.getProxyConfig({'country': 'US'})
    # Each call gets a different IP
```

### 📌 **Sticky Sessions**
```javascript
const sessionId = 'session_' + Date.now();
const proxy = await client.getProxyConfig({ 
    country: 'US', 
    session: sessionId 
});
// Maintains same IP for session
```

### 🌍 **Geo-Targeting**
```php
$proxy = $client->getProxyConfig([
    'country' => 'US',
    'city' => 'New York'
]);
```

## 🧪 Testing & Setup

Each SDK includes a quick test to verify setup:

```bash
# Expected output for all tests:
✅ API Key found
✅ Connected! User: your@email.com  
✅ Proxy credentials obtained
✅ Test complete - SDK working!
```

## ⚠️ Development Status

**Important**: These SDKs are currently in testing phase and not ready for production use.

- ✅ Basic functionality implemented
- 🧪 Currently undergoing testing
- 📝 Documentation being refined
- 🔧 APIs may change

For production use, please check back later or contact support.

## 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| `No API key found` | Set `NODEMAVEN_APIKEY` environment variable |
| `Connection failed` | Check API key validity in [dashboard](https://dashboard.nodemaven.com) |
| `Import errors` | Ensure dependencies are installed |

## 📚 Resources

- 🎯 **Dashboard**: [dashboard.nodemaven.com](https://dashboard.nodemaven.com)
- 📖 **API Docs**: [Complete reference](https://dashboard.nodemaven.com/documentation)
- 💬 **Support**: [@node_maven](https://t.me/node_maven)
- 🐛 **Issues**: [GitHub Issues](https://github.com/nodemavencom/proxy/issues)

## 💰 Pricing

| Plan | Monthly | Traffic | Features |
|------|---------|---------|----------|
| **Starter** | $50 | 5GB | All countries, HTTP/SOCKS5 |
| **Professional** | $200 | 25GB | Advanced targeting |
| **Enterprise** | Custom | Unlimited | Dedicated support |

[**View Pricing**](https://dashboard.nodemaven.com/pricing) • [**Free Trial**](https://dashboard.nodemaven.com/register)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**[🚀 Get Started](https://dashboard.nodemaven.com)** • **[📖 Documentation](https://dashboard.nodemaven.com/documentation)** • **[💬 Support](https://t.me/node_maven)**

Made with ❤️ by the NodeMaven Team

</div>
