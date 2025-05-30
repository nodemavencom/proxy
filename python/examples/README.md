# NodeMaven Examples

This directory contains working examples for using the NodeMaven API and proxies.

## Files

### `basic_usage.py`
Complete example showing all NodeMaven API functionality including:
- User information retrieval
- Location data (countries, regions, cities)
- Statistics and usage data
- Sub-user management
- IP whitelist management

### `proxy_rotation.py`
Advanced example demonstrating:
- Proxy rotation strategies
- Geo-targeting (country, region, city)
- Sticky sessions
- Error handling and retry logic

### `simple_proxy_test.py`
Simple test to verify proxy connectivity:
- HTTP proxy testing
- Geo-targeting examples
- Usage examples for different targeting options

## Running Examples

1. Make sure your `.env` file is set up in the parent directory with:
   ```
   NODEMAVEN_APIKEY = "your_api_key_here"
   ```

2. Run any example:
   ```bash
   cd examples
   python basic_usage.py
   python proxy_rotation.py
   python simple_proxy_test.py
   ```

## Proxy Usage

Your proxy credentials from the API:
- **HTTP Proxy**: `username:password@residential.nodemaven.com:8080`
- **SOCKS5 Proxy**: `username:password@residential.nodemaven.com:1080`

### Targeting Examples
- **Country**: `username-country-gb:password@residential.nodemaven.com:8080`
- **Region**: `username-country-gb-region-england:password@residential.nodemaven.com:8080`
- **City**: `username-country-gb-city-london:password@residential.nodemaven.com:8080`
- **Sticky Session**: `username-session-abc123:password@residential.nodemaven.com:8080` 