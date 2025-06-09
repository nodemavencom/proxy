# NodeMaven JavaScript SDK Examples

This directory contains practical examples demonstrating how to use the NodeMaven JavaScript SDK for residential and mobile proxy integration.

## Prerequisites

1. **NodeMaven API Key**: Get your API key from [NodeMaven Dashboard](https://dashboard.nodemaven.com)
2. **Node.js**: Version 16 or higher
3. **Environment Setup**: Set your API key as an environment variable

```bash
# Set your API key
export NODEMAVEN_APIKEY="your-api-key-here"

# Or create a .env file
echo "NODEMAVEN_APIKEY=your-api-key-here" > .env
```

## Available Examples

### 1. Basic Usage (`basic_usage.js`)

Demonstrates core SDK functionality:
- Client initialization and configuration
- Getting user information and account details
- Retrieving location data (countries, regions, cities)
- Generating proxy configurations
- Basic error handling

```bash
node examples/basic_usage.js
```

**Features Demonstrated:**
- ✅ Client setup with environment variables
- ✅ User account information retrieval
- ✅ Location hierarchy browsing
- ✅ Proxy configuration generation
- ✅ SOCKS5 URL generation
- ✅ Traffic statistics

### 2. Proxy Integration (`proxy_integration.js`)

Shows real-world proxy usage patterns:
- Making HTTP requests through proxies
- Proxy rotation across different locations
- Retry logic with exponential backoff
- Geo-targeting configurations

```bash
node examples/proxy_integration.js
```

**Features Demonstrated:**
- ✅ HTTP proxy integration with native modules
- ✅ Multi-location proxy rotation
- ✅ Automatic retry with failure handling
- ✅ Geo-targeting (country, region, city)
- ✅ IP verification and testing

## Example Output

### Basic Usage Example
```
🚀 NodeMaven JavaScript SDK - Basic Usage Example

✅ NodeMaven client initialized successfully

📊 Getting user information...
Username: your_username
Proxy Username: your_proxy_username
Traffic Used: 1250 MB
Traffic Limit: 10000 MB

🌍 Getting available countries...
Found 195 total countries. Showing first 10:
  - United States (US)
  - United Kingdom (GB)
  - Germany (DE)
  - Canada (CA)
  - Australia (AU)
  ...

🔧 Generating proxy configuration...
Proxy Configuration:
  Host: gate.nodemaven.com
  HTTP Port: 8080
  SOCKS5 Port: 1080
  Username: your_username-country-US-city-new_york
  Password: your_password...

✅ Basic usage example completed successfully!
```

### Proxy Integration Example
```
🚀 NodeMaven JavaScript SDK - Proxy Integration Examples

🌐 Basic Proxy Integration Example

🔧 Getting proxy configuration for US...
Proxy: gate.nodemaven.com:8080
Username: your_username-country-US-city-new_york

📡 Making request through proxy...
Status: 200
Detected IP: 192.168.1.100
✅ Basic proxy example completed successfully!

🔄 Proxy Rotation Example

🌍 Testing proxy rotation across different locations...

1. Testing US - new_york...
   ✅ Success - IP: 192.168.1.100
   ⏱️  Waiting 2 seconds...

2. Testing UK - london...
   ✅ Success - IP: 192.168.2.200
   ⏱️  Waiting 2 seconds...

3. Testing DE - berlin...
   ✅ Success - IP: 192.168.3.300

✅ Proxy rotation example completed!
```

## Configuration Examples

### Environment Variables
```bash
# Required
export NODEMAVEN_APIKEY="your-api-key"

# Optional (with defaults)
export NODEMAVEN_BASE_URL="https://dashboard.nodemaven.com"
export NODEMAVEN_PROXY_HOST="gate.nodemaven.com"
export NODEMAVEN_HTTP_PORT="8080"
export NODEMAVEN_SOCKS5_PORT="1080"
export REQUEST_TIMEOUT="30000"
```

### Programmatic Configuration
```javascript
const { NodeMavenClient } = require('@nodemaven/sdk');

const client = new NodeMavenClient({
  apiKey: 'your-api-key',
  baseUrl: 'https://dashboard.nodemaven.com',
  proxyHost: 'gate.nodemaven.com',
  httpPort: 8080,
  socks5Port: 1080,
  timeout: 30000
});
```

## Common Use Cases

### 1. Simple IP Rotation
```javascript
const client = new NodeMavenClient();

// Get different proxy for each request
const usProxy = await client.getProxyConfig({ country: 'US' });
const ukProxy = await client.getProxyConfig({ country: 'UK' });
const deProxy = await client.getProxyConfig({ country: 'DE' });
```

### 2. City-Level Targeting
```javascript
const client = new NodeMavenClient();

// Target specific cities
const nyProxy = await client.getProxyConfig({ 
  country: 'US', 
  city: 'new_york' 
});

const laProxy = await client.getProxyConfig({ 
  country: 'US', 
  city: 'los_angeles' 
});
```

### 3. ISP-Specific Targeting
```javascript
const client = new NodeMavenClient();

// Target specific ISP
const comcastProxy = await client.getProxyConfig({
  country: 'US',
  isp: 'comcast'
});
```

### 4. Session Management
```javascript
const client = new NodeMavenClient();

// Sticky session for related requests
const sessionProxy = await client.getProxyConfig({
  country: 'US',
  connectionType: 'sticky'
});

// Use the same proxy for multiple requests
// ... make multiple requests with sessionProxy
```

## Error Handling

The SDK provides specific error types for different scenarios:

```javascript
const { 
  NodeMavenClient, 
  AuthenticationError, 
  RateLimitError, 
  ValidationError 
} = require('@nodemaven/sdk');

try {
  const client = new NodeMavenClient();
  const userInfo = await client.getUserInfo();
} catch (error) {
  if (error instanceof AuthenticationError) {
    console.error('Invalid API key');
  } else if (error instanceof RateLimitError) {
    console.error('Rate limit exceeded');
  } else if (error instanceof ValidationError) {
    console.error('Invalid parameters');
  } else {
    console.error('Unexpected error:', error.message);
  }
}
```

## Integration with Popular HTTP Libraries

### Using with Axios
```javascript
const axios = require('axios');
const { NodeMavenClient } = require('@nodemaven/sdk');

const client = new NodeMavenClient();
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

### Using with node-fetch
```javascript
const fetch = require('node-fetch');
const { HttpsProxyAgent } = require('https-proxy-agent');

const proxyUrl = await client.getSocks5ProxyUrl({ country: 'US' });
const agent = new HttpsProxyAgent(proxyUrl);

const response = await fetch('https://httpbin.org/ip', { agent });
```

## Best Practices

1. **Reuse Client Instances**: Create one client instance and reuse it
2. **Handle Errors Gracefully**: Implement proper error handling and retries
3. **Respect Rate Limits**: Don't make too many concurrent requests
4. **Monitor Usage**: Check your traffic statistics regularly
5. **Use Appropriate Timeouts**: Set reasonable timeouts for your use case

## Support

- 📧 **Email**: [support@nodemaven.com](mailto:support@nodemaven.com)
- 💬 **Live Chat**: [NodeMaven Dashboard](https://dashboard.nodemaven.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/nodemavencom/proxy/issues)
- 📖 **Documentation**: [API Documentation](https://dashboard.nodemaven.com/documentation)

## License

These examples are provided under the MIT License. See the main repository LICENSE file for details. 