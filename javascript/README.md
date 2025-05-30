# NodeMaven JavaScript SDK 🟨

[![JavaScript](https://img.shields.io/badge/JavaScript-Coming%20Soon-yellow?style=for-the-badge&logo=javascript)](https://github.com/nodemaven/nodemaven/issues)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green?style=for-the-badge&logo=node.js)](https://nodejs.org/)
[![npm](https://img.shields.io/badge/npm-Coming%20Soon-red?style=for-the-badge)](https://www.npmjs.com/)

> **JavaScript/Node.js SDK for NodeMaven Proxy API** - Coming Soon!

## 🚧 Under Development

We're working hard to bring you a comprehensive JavaScript SDK for NodeMaven. This will include:

### 🎯 Planned Features
- **Node.js Support** - Full server-side implementation
- **Browser Support** - Client-side proxy configuration
- **TypeScript** - Full type definitions included
- **Modern Syntax** - ES6+ with async/await
- **Zero Dependencies** - Lightweight and fast

### 📦 Expected API
```javascript
import { NodeMavenClient } from '@nodemaven/sdk';

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

// Use with axios or fetch
const proxy = client.getProxyConfig({ country: 'US', city: 'new_york' });
const response = await fetch('https://httpbin.org/ip', { proxy });
```

## 🤝 Want to Help?

We'd love your contribution! Here's how you can help:

1. **⭐ Star this repo** to show interest
2. **💬 Join the discussion** in [GitHub Issues](https://github.com/nodemaven/nodemaven/issues)
3. **🔧 Contribute code** - we welcome pull requests!
4. **📝 Share feedback** on what features you need most

## 📞 Stay Updated

- 📧 **Email**: [support@nodemaven.com](mailto:support@nodemaven.com)
- 💬 **Live Chat**: [Dashboard Support](https://dashboard.nodemaven.com/support/?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=javascript_support)
- 🐛 **Issues**: [GitHub Issues](https://github.com/nodemaven/nodemaven/issues)

## 🐍 Available Now: Python SDK

While you wait for the JavaScript SDK, check out our fully-featured [Python SDK](../python/) that's ready to use today!

---

<div align="center">

**[🚀 Get Started with Python](../python/)** • **[📖 API Docs](https://dashboard.nodemaven.com/documentation/?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=javascript_docs)** • **[💬 Request Features](https://github.com/nodemaven/nodemaven/issues)**

</div> 