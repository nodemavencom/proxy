# Changelog

All notable changes to the NodeMaven Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-16

### 🎉 Initial Release

This is the first stable release of the NodeMaven Python SDK, providing comprehensive proxy management and IP geolocation capabilities.

### Added

#### Core Features
- **NodeMavenClient**: Complete API client for NodeMaven services
- **Proxy Management**: HTTP and SOCKS5 proxy support with global targeting
- **IP Geolocation**: Dual-service IP checking with ipapi.com and ipinfo.io
- **Session Management**: Sticky sessions with configurable TTL (Time-To-Live)
- **Error Handling**: Comprehensive exception handling with detailed error messages

#### Targeting Options
- **Geographic Targeting**: Country, region, city-level proxy selection
- **Connection Types**: Residential and mobile proxy support
- **ISP Targeting**: Internet Service Provider specific routing
- **Quality Filtering**: Low, medium, high quality proxy filters
- **Protocol Support**: IPv4 support with automatic configuration

#### Professional Tools
- **CLI Tools**: Command-line interface with 3 utilities:
  - `nodemaven-test`: Test API connectivity and proxy functionality
  - `nodemaven-ip`: Check IP geolocation information
  - `nodemaven-countries`: List available countries and locations
- **Type Hints**: Full type annotation support for better IDE experience
- **Documentation**: Comprehensive examples and usage guides

#### Testing & Quality Assurance
- **48 Comprehensive Tests**: Complete test coverage
  - 31 Unit Tests: No API key required, test all functionality
  - 17 Integration Tests: Real API and proxy connection validation
- **GitHub Actions**: Automated testing on every commit and PR
- **Community Testing**: Users can test with their own API keys
- **Quality Tools**: Black formatting, MyPy type checking, pytest coverage

#### Examples & Demos
- **Basic Usage**: Simple client initialization and API calls
- **Proxy Examples**: Advanced proxy configurations and targeting
- **Proxy Rotation**: IP rotation and session management techniques
- **Mobile Proxies**: Mobile-specific proxy configurations
- **Web Scraping Demo**: Professional web scraping with error handling
- **IP Checker Tools**: Standalone geolocation utilities

#### Professional Features
- **PyPI Package**: Modern pyproject.toml configuration
- **Automated Publishing**: GitHub Actions workflow for PyPI releases
- **Version Management**: Semantic versioning with automated updates
- **Package Validation**: Comprehensive build and distribution checks
- **Type Safety**: py.typed marker for type checking support

### Technical Specifications
- **Python Support**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Dependencies**: Minimal dependencies (requests, urllib3, certifi, python-dotenv)
- **License**: MIT License for maximum compatibility
- **Package Size**: Optimized for fast installation
- **Documentation**: Complete API reference and examples

### Installation
```bash
# Install from PyPI
pip install nodemaven

# Install with development tools
pip install nodemaven[dev]

# Install with documentation tools  
pip install nodemaven[docs]

# Install with example dependencies
pip install nodemaven[examples]
```

### Quick Start
```python
from nodemaven import NodeMavenClient

# Initialize client
client = NodeMavenClient()

# Get user information
user_info = client.get_user_info()
print(f"Connected as: {user_info['email']}")

# Use proxies
from nodemaven.utils import get_proxy_config
import requests

proxies = get_proxy_config(country="us", city="new_york")
response = requests.get("http://httpbin.org/ip", proxies=proxies)
print(f"Your IP: {response.json()['origin']}")
```

### Community & Support
- **GitHub Repository**: https://github.com/nodemavencom/proxy
- **Documentation**: https://dashboard.nodemaven.com/documentation
- **Support**: https://t.me/node_maven
- **Issues**: https://github.com/nodemavencom/proxy/issues

### Breaking Changes
None - this is the initial release.

### Migration Guide
Not applicable - initial release.

---

## [Unreleased]

### Planned Features
- Async/await support for high-performance applications
- WebSocket proxy support for real-time applications
- Enhanced mobile proxy features
- Advanced analytics and monitoring tools
- Integration with popular web scraping frameworks
- Docker containerization examples
- Kubernetes deployment guides

---

**Note**: This changelog follows the [Keep a Changelog](https://keepachangelog.com/) format. For more details about any release, check the corresponding GitHub release page. 