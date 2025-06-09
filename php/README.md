# NodeMaven PHP SDK 🟣

[![PHP](https://img.shields.io/badge/PHP-Ready-purple?style=for-the-badge&logo=php)](https://github.com/nodemavencom/proxy)
[![Composer](https://img.shields.io/badge/Composer-Available-orange?style=for-the-badge)](https://getcomposer.org/)
[![Packagist](https://img.shields.io/badge/Packagist-Coming%20Soon-blue?style=for-the-badge)](https://packagist.org/)

> **Professional PHP SDK for NodeMaven Proxy API** - Production Ready!

## ✅ Production Ready

A comprehensive PHP SDK for NodeMaven's residential and mobile proxy service. Modern PHP 8.0+ with full type declarations and PSR standards compliance.

### 🎯 Features
- **PHP 8.0+** - Modern PHP with strict typing and null safety
- **Composer Package** - Easy installation and dependency management
- **PSR Standards** - Following PSR-4, PSR-7, PSR-18 for maximum compatibility
- **Guzzle Integration** - Built-in HTTP client with comprehensive proxy support
- **Multiple Integrations** - Works with Guzzle, cURL, and stream contexts
- **Exception Handling** - Comprehensive error types and handling

### 🚀 Quick Start
```php
<?php
use NodeMaven\Client;

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

// Create HTTP client with proxy
$proxyConfig = $client->getProxyConfig(['country' => 'US', 'city' => 'New York']);
$httpClient = $proxyConfig->createHttpClient();

$response = $httpClient->get('https://httpbin.org/ip');
echo $response->getBody()->getContents();
```

## 📦 Installation

### Requirements
- PHP 8.0 or higher
- Composer
- cURL extension
- JSON extension
- OpenSSL extension

### Install via Composer
```bash
composer require nodemaven/sdk
```

Or clone this repository:
```bash
git clone https://github.com/nodemavencom/proxy.git
cd proxy/php
composer install
```

## 🔧 Setup

### Environment Variables (Recommended)
```bash
export NODEMAVEN_APIKEY="your-api-key-here"
```

### Or Configuration Object
```php
$client = new Client([
    'api_key' => 'your-api-key-here',
    'timeout' => 30
]);
```

### Using .env File
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
NODEMAVEN_APIKEY=your_api_key_here
```

## 📖 Documentation

### Core Methods

#### `getUserInfo()`
Get account information and proxy credentials:
```php
$userInfo = $client->getUserInfo();
echo "Traffic used: " . $userInfo['traffic_used'] . " bytes";
```

#### `getCountries($options)`
List available countries:
```php
$countries = $client->getCountries(['limit' => 10]);
foreach ($countries['results'] as $country) {
    echo $country['name'] . " (" . $country['code'] . ")\n";
}
```

#### `getRegions($options)` & `getCities($options)`
Get regions and cities for geo-targeting:
```php
$regions = $client->getRegions(['country_code' => 'US']);
$cities = $client->getCities(['country_code' => 'US', 'region_code' => 'CA']);
```

#### `getProxyConfig($options)`
Generate proxy configuration:
```php
$proxyConfig = $client->getProxyConfig([
    'country' => 'US',
    'city' => 'New York'
]);
```

#### `getSocks5ProxyUrl($options)`
Get SOCKS5 proxy URL:
```php
$proxyUrl = $client->getSocks5ProxyUrl(['country' => 'UK']);
// Returns: socks5://username:password@gate.nodemaven.com:1080
```

### Error Handling
```php
use NodeMaven\Client;
use NodeMaven\Exceptions\AuthenticationException;
use NodeMaven\Exceptions\RateLimitException;

try {
    $client = new Client();
    $userInfo = $client->getUserInfo();
} catch (AuthenticationException $e) {
    echo 'Invalid API key: ' . $e->getMessage();
} catch (RateLimitException $e) {
    echo 'Rate limit exceeded: ' . $e->getMessage();
}
```

## 🛠️ Examples

See the [`examples/`](./examples/) directory for comprehensive usage examples:

- **[Basic Usage](./examples/basic_usage.php)** - Core functionality and setup
- **[Proxy Integration](./examples/proxy_integration.php)** - Advanced integration patterns

```bash
# Run examples
php examples/basic_usage.php
php examples/proxy_integration.php
```

## 🌐 Integration with HTTP Libraries

### Guzzle HTTP Client
```php
$proxyConfig = $client->getProxyConfig(['country' => 'US']);
$httpClient = $proxyConfig->createHttpClient();

$response = $httpClient->get('https://httpbin.org/ip');
```

### Direct cURL
```php
$proxyConfig = $client->getProxyConfig(['country' => 'US']);
$curlOptions = $proxyConfig->getCurlOptions();

$ch = curl_init();
curl_setopt_array($ch, array_merge($curlOptions, [
    CURLOPT_URL => 'https://httpbin.org/ip',
    CURLOPT_RETURNTRANSFER => true,
]));

$response = curl_exec($ch);
curl_close($ch);
```

### Stream Context (file_get_contents)
```php
$proxyConfig = $client->getProxyConfig(['country' => 'US']);
$context = $proxyConfig->getStreamContext();

$response = file_get_contents('https://httpbin.org/ip', false, $context);
```

## 🔧 Advanced Usage

### Sticky Sessions
```php
$sessionId = 'user_session_' . uniqid();
$proxyConfig = $client->getProxyConfig([
    'country' => 'US',
    'session' => $sessionId
]);

// All requests with this proxy will use the same IP
$httpClient = $proxyConfig->createHttpClient();
```

### Concurrent Requests
```php
use GuzzleHttp\Promise;

$promises = [];
for ($i = 0; $i < 5; $i++) {
    $sessionId = "worker_{$i}";
    $proxyConfig = $client->getProxyConfig([
        'country' => 'US',
        'session' => $sessionId
    ]);
    
    $httpClient = $proxyConfig->createHttpClient();
    $promises[] = $httpClient->getAsync('https://httpbin.org/ip');
}

$responses = Promise\settle($promises)->wait();
```

### Geo-targeting
```php
// Country targeting
$usProxy = $client->getProxyConfig(['country' => 'US']);

// City targeting
$nyProxy = $client->getProxyConfig([
    'country' => 'US',
    'city' => 'New York'
]);

// ISP targeting
$ispProxy = $client->getProxyConfig([
    'country' => 'US',
    'isp' => 'Verizon'
]);
```

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

### Programmatic Configuration

```php
$client = new Client([
    'api_key' => 'your_api_key',
    'base_url' => 'https://dashboard.nodemaven.com',
    'proxy_host' => 'gate.nodemaven.com',
    'http_port' => 8080,
    'socks5_port' => 1080,
    'timeout' => 30
]);
```

## 🧪 Testing

### Quick Test
```bash
php quick_test.php
```

### Composer Scripts
```bash
# Run all tests
composer test

# Check code style
composer cs

# Run linting
composer lint
```

### Manual Testing
```php
use NodeMaven\Utils;

// Check system requirements
$missing = Utils::checkRequiredExtensions();
if (!empty($missing)) {
    echo "Missing extensions: " . implode(', ', $missing);
}

// Test proxy connection
$proxyConfig = $client->getProxyConfig(['country' => 'US']);
$result = $proxyConfig->testConnection();

if ($result['success']) {
    echo "Proxy working! IP: " . $result['ip'];
} else {
    echo "Proxy failed: " . $result['error'];
}
```

## 🔍 Utilities

### Helper Functions
```php
use NodeMaven\Utils;

// Format bytes
echo Utils::formatBytes(1024 * 1024); // "1.00 MB"

// Generate session ID
$sessionId = Utils::generateSessionId(12);

// Get current IP
$ip = Utils::getCurrentIp();

// Validate proxy options
$validation = Utils::validateProxyOptions(['country' => 'US']);
if (!$validation['valid']) {
    echo "Validation errors: " . implode(', ', $validation['errors']);
}
```

### System Information
```php
$sysInfo = Utils::getSystemInfo();
echo "PHP Version: " . $sysInfo['php_version'];
echo "OS: " . $sysInfo['os'];
```

## 🐛 Troubleshooting

### Common Issues

**Composer autoload not found**
```bash
composer install
```

**Missing PHP extensions**
```bash
# Ubuntu/Debian
sudo apt-get install php-curl php-json php-openssl

# CentOS/RHEL
sudo yum install php-curl php-json php-openssl

# Check extensions
php -m | grep -E "(curl|json|openssl)"
```

**API key errors**
```bash
# Set environment variable
export NODEMAVEN_APIKEY="your-key-here"

# Or create .env file
echo "NODEMAVEN_APIKEY=your-key-here" > .env
```

**Proxy connection issues**
- Verify API key is valid
- Check account has proxy access enabled
- Test network connectivity
- Try different target countries

### Debug Mode
```php
$client = new Client([
    'api_key' => 'your_key',
    'debug' => true
]);
```

## 🤝 Support & Community

- 📧 **Email**: [support@nodemaven.com](mailto:support@nodemaven.com)
- 💬 **Live Chat**: [NodeMaven Dashboard](https://dashboard.nodemaven.com?utm_source=github&utm_medium=php_readme&utm_campaign=developer_outreach&utm_content=support_chat)
- 🐛 **Issues**: [GitHub Issues](https://github.com/nodemavencom/proxy/issues)
- 📖 **API Docs**: [Documentation](https://dashboard.nodemaven.com/documentation?utm_source=github&utm_medium=php_readme&utm_campaign=developer_outreach&utm_content=api_docs)

## 🔗 Other SDKs

- 🐍 **[Python SDK](../python/)** - Full-featured Python implementation  
- 🟢 **[JavaScript SDK](../javascript/)** - Zero-dependency Node.js implementation
- 🔷 **[Go SDK](../go/)** - High-performance Go implementation

---

<div align="center">

**[🚀 Get Started](https://dashboard.nodemaven.com?utm_source=github&utm_medium=php_readme&utm_campaign=developer_outreach&utm_content=footer_cta)** • **[📖 Full Documentation](https://dashboard.nodemaven.com/documentation?utm_source=github&utm_medium=php_readme&utm_campaign=developer_outreach&utm_content=footer_docs)** • **[💬 Support](https://dashboard.nodemaven.com?utm_source=github&utm_medium=php_readme&utm_campaign=developer_outreach&utm_content=footer_support)**

</div> 