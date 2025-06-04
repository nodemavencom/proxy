# NodeMaven Tests 🧪

This directory contains tests for the NodeMaven Python SDK.

## 📋 Test Types

### ✅ **Unit Tests** (`test_unit.py`)
- **Purpose**: Test individual functions and classes **without external dependencies**
- **Requirements**: No API key needed, no network access required
- **Usage**: Perfect for CI/CD pipelines and quick development testing
- **Coverage**: Utility functions, exception handling, client initialization, proxy URL building

```bash
# Run unit tests (CI/CD safe)
python -m pytest tests/test_unit.py -v
```

### 🌐 **Integration Tests** (`test_integration_*.py`)
- **Purpose**: Test real API interactions and proxy functionality
- **Requirements**: Valid NodeMaven API key, network access
- **Usage**: Local testing and verification of actual service integration
- **Coverage**: Real API calls, proxy requests, IP checking services

```bash
# Run integration tests (requires API key)
python -m pytest tests/test_integration_*.py -v

# Or run specific integration tests
python tests/test_integration_client.py
python tests/test_integration_proxy.py
python tests/test_integration_ip_checker.py
```

### 🛠️ **Utility Tests** (`test_utils.py`)
- **Purpose**: Test utility functions that may or may not require API access
- **Mixed requirements**: Some tests need API key, others don't

## 🚀 Quick Testing

### For Development (Unit Tests Only)
```bash
# Fast, no API key needed
python -m pytest tests/test_unit.py -v
```

### For Full Verification (All Tests)
```bash
# Requires API key in .env file
python -m pytest tests/ -v
```

### For CI/CD (GitHub Actions)
```bash
# Only unit tests run in CI/CD
python -m pytest tests/test_unit.py -v
```

## 📊 Test Coverage

| Test File | Type | Tests | Requirements |
|-----------|------|-------|--------------|
| `test_unit.py` | Unit | 14 tests | ✅ None |
| `test_integration_client.py` | Integration | 3 tests | 🔑 API Key |
| `test_integration_proxy.py` | Integration | 3 tests | 🔑 API Key |
| `test_integration_ip_checker.py` | Integration | 3 tests | 🔑 API Key |
| `test_utils.py` | Mixed | 3 tests | 🔑 API Key |

## 🔧 Running Tests

### Prerequisites
```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Set up API key (for integration tests)
cp env.example .env
# Edit .env with your API key
```

### Commands
```bash
# All unit tests (CI/CD safe)
python -m pytest tests/test_unit.py -v

# All tests (requires API key)
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_integration_client.py -v

# With coverage
python -m pytest tests/test_unit.py --cov=nodemaven --cov-report=html
```

## 🎯 CI/CD Integration

The GitHub Actions workflow runs **only unit tests** to avoid requiring API keys in the CI environment:

```yaml
- name: Test with pytest (unit tests only)
  run: python -m pytest tests/test_unit.py -v --tb=short
```

This ensures reliable, fast testing in CI/CD while keeping integration tests for local verification.

## Requirements

- Virtual environment activated
- All dependencies installed (`pip install -r ../requirements.txt`)
- `.env`