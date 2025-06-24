# NodeMaven Python SDK 🐍

**Status: Testing** - Basic functionality implemented, not production-ready.

## Quick Setup

```bash
cd python
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

pip install -r requirements.txt
export NODEMAVEN_APIKEY="your_api_key_here"
python quick_test.py
```

## Basic Usage

```python
from nodemaven import Client

# Initialize client
client = Client()

# Get proxy config
proxy = client.getProxyConfig({'country': 'US'})
print(f"Proxy: {proxy}")
```

## Structure

- `nodemaven/` - Core SDK package
- `examples/` - Basic usage examples
- `quick_test.py` - Setup test script

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
