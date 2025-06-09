# NodeMaven PHP SDK Examples

This directory contains comprehensive examples demonstrating how to use the NodeMaven PHP SDK for various proxy integration scenarios.

## 📁 Examples

### [`basic_usage.php`](./basic_usage.php)
**Beginner-friendly introduction to the SDK**

Learn the core functionality including:
- Client initialization and configuration
- Getting user account information
- Basic proxy configuration
- Geo-targeting (country-level)
- Sticky sessions for consistent IPs
- Testing proxy connections
- Making HTTP requests through proxies

```bash
php examples/basic_usage.php
```

### [`proxy_integration.php`](./proxy_integration.php)
**Advanced integration patterns and techniques**

Explore advanced features such as:
- Session management and IP rotation
- Concurrent requests with different proxies
- Error handling and retry mechanisms
- Multiple HTTP client integration methods (Guzzle, cURL, stream)
- City-level geo-targeting
- Performance testing and monitoring

```bash
php examples/proxy_integration.php
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd proxy/php
composer install
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API key
# NODEMAVEN_APIKEY=your_api_key_here
```

### 3. Run Examples
```bash
# Start with basic usage
php examples/basic_usage.php

# Then try advanced integration
php examples/proxy_integration.php
```

## 🎯 Common Use Cases

### Basic Proxy Usage
```php
use NodeMaven\Client;

$client = new Client();
$proxyConfig = $client->getProxyConfig(['country' => 'US']);
$httpClient = $proxyConfig->createHttpClient();

$response = $httpClient->get('https://api.example.com/data');
```

### Sticky Sessions
```php
$sessionId = 'user_' . uniqid();
$proxyConfig = $client->getProxyConfig([
    'country' => 'US',
    'session' => $sessionId
]);
```

### Geo-targeting
```php
// Country level
$usProxy = $client->getProxyConfig(['country' => 'US']);

// City level
$nyProxy = $client->getProxyConfig([
    'country' => 'US',
    'city' => 'New York'
]);
```

### Error Handling
```php
use NodeMaven\Exceptions\NodeMavenException;
use NodeMaven\Exceptions\AuthenticationException;

try {
    $client = new Client();
    $userInfo = $client->getUserInfo();
} catch (AuthenticationException $e) {
    echo "Invalid API key: " . $e->getMessage();
} catch (NodeMavenException $e) {
    echo "API error: " . $e->getMessage();
}
```

## 🔧 Integration Methods

### Guzzle HTTP Client
```php
$proxyConfig = $client->getProxyConfig(['country' => 'US']);
$httpClient = $proxyConfig->createHttpClient();

$response = $httpClient->get('https://httpbin.org/ip');
```

### Direct cURL
```php
$curlOptions = $proxyConfig->getCurlOptions();

$ch = curl_init();
curl_setopt_array($ch, array_merge($curlOptions, [
    CURLOPT_URL => 'https://httpbin.org/ip',
    CURLOPT_RETURNTRANSFER => true,
]));

$response = curl_exec($ch);
curl_close($ch);
```

### Stream Context
```php
$context = $proxyConfig->getStreamContext();
$response = file_get_contents('https://httpbin.org/ip', false, $context);
```

## 📊 Testing Your Setup

Use the quick test script to verify everything is working:

```bash
php quick_test.php
```

This will check:
- ✅ PHP version and extensions
- ✅ Environment configuration
- ✅ API connectivity
- ✅ Proxy functionality
- ✅ Connection testing

## 🔗 Additional Resources

- **[Main README](../README.md)** - Complete SDK documentation
- **[API Documentation](https://dashboard.nodemaven.com/documentation)** - Full API reference
- **[NodeMaven Dashboard](https://dashboard.nodemaven.com)** - Account management
- **[Support](https://dashboard.nodemaven.com)** - Get help and support

## 💡 Tips

1. **Always use sessions** for consistent IP addresses across requests
2. **Handle errors gracefully** with try-catch blocks
3. **Test your proxy configurations** before production use
4. **Monitor response times** for performance optimization
5. **Use appropriate timeouts** for your use case

## 🐛 Troubleshooting

### Common Issues

**"Composer autoload not found"**
```bash
composer install
```

**"API key is required"**
```bash
export NODEMAVEN_APIKEY="your-key-here"
# or edit .env file
```

**"Proxy connection failed"**
- Check your API key is valid
- Verify account has proxy access
- Test network connectivity
- Try different target countries

**"Missing PHP extensions"**
```bash
# Install required extensions (Ubuntu/Debian)
sudo apt-get install php-curl php-json php-openssl

# Check loaded extensions
php -m | grep -E "(curl|json|openssl)"
```

For more help, check the [troubleshooting section](../README.md#troubleshooting) in the main README. 