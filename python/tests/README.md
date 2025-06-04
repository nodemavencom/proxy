# Python Tests

Simple test files for NodeMaven Python functionality.

## Test Files

- **`test_client.py`** - Tests for NodeMaven API client
- **`test_utils.py`** - Tests for utility functions  
- **`test_ip_checker.py`** - Tests for IP checking functionality
- **`test_proxy_functionality.py`** - Tests for proxy operations

## Running Tests

```bash
# Run individual tests (with detailed logging)
python test_client.py
python test_utils.py
python test_ip_checker.py
python test_proxy_functionality.py

# Or run all tests
python -m pytest
```

**Note:** All tests now include detailed logging output showing:
- 🧪 Test progress and status
- 📊 API responses and data
- 🔧 Configuration details
- ✅ Success confirmations

## Requirements

- Virtual environment activated
- All dependencies installed (`pip install -r ../requirements.txt`)
- `.env` file with NODEMAVEN_APIKEY configured 