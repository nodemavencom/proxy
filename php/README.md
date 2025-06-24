# NodeMaven PHP SDK 🟣

**Status: Testing** - Basic functionality implemented, not production-ready.

## Quick Setup

```bash
cd php
composer install
export NODEMAVEN_APIKEY="your_api_key_here"
php quick_test.php
```

## Basic Usage

```php
<?php
use NodeMaven\Client;

// Initialize client
$client = new Client();

// Get proxy config
$proxy = $client->getProxyConfig(['country' => 'US']);
echo "Proxy: " . print_r($proxy, true);
?>
```

## Structure

- `src/` - Core SDK classes
- `examples/` - Basic usage examples
- `quick_test.php` - Setup test script

## Expected Test Output

```
✅ API Key found
✅ Connected! User: your@email.com  
✅ Proxy credentials obtained
✅ Test complete - SDK working!
```

## Development Status

⚠️ **This SDK is in testing phase**
- Basic functionality implemented
- APIs may change
- Not ready for production use

For production-ready SDKs, check dedicated repositories. 