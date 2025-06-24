# NodeMaven JavaScript SDK 🟢

**Status: Testing** - Basic functionality implemented, not production-ready.

## Quick Setup

```bash
cd javascript
npm install
export NODEMAVEN_APIKEY="your_api_key_here"
node quick_test.js
```

## Basic Usage

```javascript
const { NodeMavenClient } = require('@nodemaven/sdk');

// Initialize client
const client = new NodeMavenClient();

// Get proxy config
const proxy = await client.getProxyConfig({ country: 'US' });
console.log('Proxy:', proxy);
```

## Structure

- `src/` - Core SDK files
- `examples/` - Basic usage examples
- `quick_test.js` - Setup test script

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