# NodeMaven PHP SDK 🟣

[![PHP](https://img.shields.io/badge/PHP-Coming%20Soon-purple?style=for-the-badge&logo=php)](https://github.com/nodemaven/nodemaven/issues)
[![Composer](https://img.shields.io/badge/Composer-Coming%20Soon-orange?style=for-the-badge)](https://getcomposer.org/)
[![Packagist](https://img.shields.io/badge/Packagist-Coming%20Soon-blue?style=for-the-badge)](https://packagist.org/)

> **PHP SDK for NodeMaven Proxy API** - Coming Soon!

## 🚧 Under Development

We're building a comprehensive PHP SDK for NodeMaven with modern PHP practices:

### 🎯 Planned Features
- **PHP 8.0+** - Modern PHP with type declarations
- **Composer Package** - Easy installation via Composer
- **PSR Standards** - Following PSR-4, PSR-7, PSR-18
- **Guzzle Integration** - HTTP client with proxy support
- **Laravel Support** - Service provider and facades

### 📦 Expected API
```php
<?php
use NodeMaven\Client;
use NodeMaven\ProxyConfig;

$client = new Client([
    'api_key' => 'your_api_key_here'
]);

// Get user information
$userInfo = $client->getUserInfo();
echo "Username: " . $userInfo['proxy_username'];

// Get countries
$countries = $client->getCountries(['limit' => 10]);
foreach ($countries['results'] as $country) {
    echo $country['name'] . " (" . $country['code'] . ")\n";
}

// Use with Guzzle
$proxy = ProxyConfig::create(['country' => 'US', 'city' => 'new_york']);
$response = $client->request('GET', 'https://httpbin.org/ip', [
    'proxy' => $proxy->toArray()
]);
```

### 🎨 Laravel Integration
```php
// config/services.php
'nodemaven' => [
    'api_key' => env('NODEMAVEN_API_KEY'),
],

// Usage
use NodeMaven\Facades\NodeMaven;

$userInfo = NodeMaven::getUserInfo();
$countries = NodeMaven::getCountries();
```

## 🤝 Want to Help?

We'd love your contribution! Here's how you can help:

1. **⭐ Star this repo** to show interest
2. **💬 Join the discussion** in [GitHub Issues](https://github.com/nodemaven/nodemaven/issues)
3. **🔧 Contribute code** - we welcome pull requests!
4. **📝 Share feedback** on Laravel/Symfony integration needs

## 📞 Stay Updated

- 📧 **Email**: [support@nodemaven.com](mailto:support@nodemaven.com)
- 💬 **Live Chat**: [NodeMaven Support](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=php_support)
- 🐛 **Issues**: [GitHub Issues](https://github.com/nodemaven/nodemaven/issues)

## 🐍 Available Now: Python SDK

While you wait for the PHP SDK, check out our fully-featured [Python SDK](../python/) that's ready to use today!

---

<div align="center">

**[🚀 Get Started with Python](../python/)** • **[📖 API Docs](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=php_docs)** • **[💬 Request Features](https://github.com/nodemaven/nodemaven/issues)**

</div> 