# NodeMaven JavaScript SDK 🟢

[![JavaScript](https://img.shields.io/badge/JavaScript-Ready-green?style=for-the-badge&logo=javascript)](https://github.com/nodemavencom/proxy)
[![Node.js](https://img.shields.io/badge/Node.js-16%2B-green?style=for-the-badge&logo=node.js)](https://nodejs.org/)
[![npm](https://img.shields.io/badge/npm-Available-green?style=for-the-badge)](https://www.npmjs.com/)

> **Professional JavaScript/Node.js SDK for NodeMaven Proxy API**

## ✅ Production Ready

A comprehensive JavaScript SDK for NodeMaven's residential and mobile proxy service. Get started in minutes!

### 🎯 Features
- **Node.js Support** - Full server-side implementation with native modules
- **Zero Dependencies** - Lightweight and fast, no external dependencies
- **TypeScript** - Full type definitions included
- **Modern Syntax** - ES6+ with async/await
- **Error Handling** - Comprehensive error types and handling

### 🚀 Quick Start
```javascript
const { NodeMavenClient } = require('@nodemaven/sdk');

const client = new NodeMavenClient({
  apiKey: 'your_api_key_here'
});

// Get user information
const userInfo = await client.getUserInfo();
console.log(`Username: ${userInfo.proxy_username}`);

// Get countries
const countries = await client.getCountries({ limit: 10 });
countries.results.forEach(country => {
  console.log(`${country.name} (${country.code})`);
});

// Get proxy configuration
const proxyConfig = await client.getProxyConfig({ 
  country: 'US', 
  city: 'new_york' 
});
console.log(`Proxy: ${proxyConfig.host}:${proxyConfig.http_port}`);
```

## 📦 Installation

```bash
npm install @nodemaven/sdk
```

## 🔧 Setup

### Environment Variables (Recommended)
```bash
export NODEMAVEN_APIKEY="your-api-key-here"
```

### Or Configuration Object
```javascript
const client = new NodeMavenClient({
  apiKey: 'your-api-key-here'
});
```

## 📖 Documentation

### Core Methods

#### `getUserInfo()`
Get account information and proxy credentials:
```javascript
const userInfo = await client.getUserInfo();
console.log(`Traffic used: ${userInfo.traffic_used} MB`);
```

#### `getCountries(options)`
List available countries:
```javascript
const countries = await client.getCountries({ limit: 10 });
countries.results.forEach(country => {
  console.log(`${country.name} (${country.code})`);
});
```

#### `getRegions(options)` & `getCities(options)`
Get regions and cities for geo-targeting:
```javascript
const regions = await client.getRegions({ countryCode: 'US' });
const cities = await client.getCities({ countryCode: 'US', regionCode: 'CA' });
```

#### `getProxyConfig(options)`
Generate proxy configuration:
```javascript
const proxyConfig = await client.getProxyConfig({
  country: 'US',
  city: 'new_york'
});
```

#### `getSocks5ProxyUrl(options)`
Get SOCKS5 proxy URL:
```javascript
const proxyUrl = await client.getSocks5ProxyUrl({ country: 'UK' });
// Returns: socks5://username:password@gate.nodemaven.com:1080
```

### Error Handling
```javascript
const { 
  NodeMavenClient, 
  AuthenticationError, 
  RateLimitError 
} = require('@nodemaven/sdk');

try {
  const client = new NodeMavenClient();
  const userInfo = await client.getUserInfo();
} catch (error) {
  if (error instanceof AuthenticationError) {
    console.error('Invalid API key');
  } else if (error instanceof RateLimitError) {
    console.error('Rate limit exceeded');
  }
}
```

## 🛠️ Examples

See the [`examples/`](./examples/) directory for comprehensive usage examples:

- **[Basic Usage](./examples/basic_usage.js)** - Core functionality and setup
- **[Proxy Integration](./examples/proxy_integration.js)** - Real-world proxy usage patterns

```bash
# Run examples
node examples/basic_usage.js
node examples/proxy_integration.js
```

## 🌐 Integration with HTTP Libraries

### Native http/https modules
```javascript
const proxyConfig = await client.getProxyConfig({ country: 'US' });
// Use proxyConfig.host, proxyConfig.http_port, etc.
```

### With Axios
```javascript
const axios = require('axios');
const proxyConfig = await client.getProxyConfig({ country: 'US' });

const response = await axios.get('https://httpbin.org/ip', {
  proxy: {
    host: proxyConfig.host,
    port: proxyConfig.http_port,
    auth: {
      username: proxyConfig.username,
      password: proxyConfig.password
    }
  }
});
```

## 🤝 Support & Community

- 📧 **Email**: [support@nodemaven.com](mailto:support@nodemaven.com)
- 💬 **Live Chat**: [NodeMaven Dashboard](https://dashboard.nodemaven.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/nodemavencom/proxy/issues)
- 📖 **API Docs**: [Documentation](https://dashboard.nodemaven.com/documentation)

## 🔗 Other SDKs

- 🐍 **[Python SDK](../python/)** - Full-featured Python implementation  
- 🔷 **[Go SDK](../go/)** - High-performance Go implementation

---

<div align="center">

**[🚀 Get Started](https://dashboard.nodemaven.com)** • **[📖 Full Documentation](https://dashboard.nodemaven.com/documentation)** • **[💬 Support](https://dashboard.nodemaven.com)**

</div> 