# NodeMaven Go SDK

A comprehensive Go client library for [NodeMaven](https://nodemaven.com) - high-performance residential and mobile proxy service.

[![Go Reference](https://pkg.go.dev/badge/github.com/nodemavencom/proxy/go/nodemaven.svg)](https://pkg.go.dev/github.com/nodemavencom/proxy/go/nodemaven)
[![Go Report Card](https://goreportcard.com/badge/github.com/nodemavencom/proxy/go)](https://goreportcard.com/report/github.com/nodemavencom/proxy/go)

## Features

- 🌍 **Global Proxy Network** - Access residential and mobile proxies from 100+ countries
- 🎯 **Geo-targeting** - Target specific countries, regions, cities, and ISPs
- 📌 **Sticky Sessions** - Maintain the same IP across multiple requests
- ⚡ **High Performance** - Concurrent request support with connection pooling
- 🔒 **Secure** - Built-in authentication and error handling
- 📖 **Well Documented** - Comprehensive documentation and examples

## Installation

```bash
go get github.com/nodemavencom/proxy/go/nodemaven
```

## Quick Start

### 1. Get Your API Key

Sign up at [NodeMaven Dashboard](https://dashboard.nodemaven.com) and get your API key.

### 2. Set Environment Variable

```bash
# Windows
set NODEMAVEN_APIKEY=your_api_key_here

# Linux/macOS
export NODEMAVEN_APIKEY=your_api_key_here
```

### 3. Basic Usage

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/nodemavencom/proxy/go/nodemaven"
)

func main() {
    // Initialize client
    client, err := nodemaven.NewClient(&nodemaven.Config{})
    if err != nil {
        log.Fatal(err)
    }

    // Get basic proxy
    proxy, err := client.GetProxyConfig(nil)
    if err != nil {
        log.Fatal(err)
    }

    // Use proxy with HTTP client
    httpClient := proxy.HTTPClient()
    
    // Make request through proxy
    resp, err := httpClient.Get("https://httpbin.org/ip")
    if err != nil {
        log.Fatal(err)
    }
    defer resp.Body.Close()

    fmt.Println("Request successful through proxy!")
}
```

## Advanced Usage

### Geo-targeting

```go
// Target specific country
proxy, err := client.GetProxyConfig(&nodemaven.ProxyOptions{
    Country: "US",
})

// Target specific region and city
proxy, err := client.GetProxyConfig(&nodemaven.ProxyOptions{
    Country: "US",
    Region:  "California",
    City:    "San Francisco",
})
```

### Sticky Sessions

```go
// Create sticky session
sessionID := "my_session_" + nodemaven.GenerateSessionID()

proxy, err := client.GetProxyConfig(&nodemaven.ProxyOptions{
    Country: "US",
    Session: sessionID,
})

// All requests with this proxy will use the same IP
httpClient := proxy.HTTPClient()
```

### Concurrent Requests

```go
// Multiple concurrent requests with different sessions
var wg sync.WaitGroup
for i := 0; i < 10; i++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        
        sessionID := fmt.Sprintf("worker_%d", id)
        proxy, err := client.GetProxyConfig(&nodemaven.ProxyOptions{
            Country: "US",
            Session: sessionID,
        })
        if err != nil {
            return
        }
        
        httpClient := proxy.HTTPClient()
        resp, err := httpClient.Get("https://httpbin.org/ip")
        if err != nil {
            return
        }
        resp.Body.Close()
        
        fmt.Printf("Worker %d completed\n", id)
    }(i)
}
wg.Wait()
```

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NODEMAVEN_APIKEY` | Your API key (required) | - |
| `NODEMAVEN_BASE_URL` | API base URL | `https://dashboard.nodemaven.com` |
| `NODEMAVEN_PROXY_HOST` | Proxy host | `gate.nodemaven.com` |
| `NODEMAVEN_HTTP_PORT` | HTTP proxy port | `8080` |
| `NODEMAVEN_SOCKS5_PORT` | SOCKS5 proxy port | `1080` |
| `REQUEST_TIMEOUT` | Request timeout (seconds) | `30` |

### Programmatic Configuration

```go
client, err := nodemaven.NewClient(&nodemaven.Config{
    APIKey:     "your_api_key",
    BaseURL:    "https://dashboard.nodemaven.com",
    ProxyHost:  "gate.nodemaven.com",
    HTTPPort:   8080,
    SOCKS5Port: 1080,
    Timeout:    30 * time.Second,
})
```

## API Reference

### Core Types

- **`Client`** - Main client for API interactions
- **`ProxyConfig`** - Proxy configuration with HTTP client
- **`ProxyOptions`** - Targeting and session options
- **`UserInfo`** - Account information and usage stats

### Key Methods

- **`NewClient(config)`** - Create new client
- **`GetUserInfo()`** - Get account information
- **`GetProxyConfig(options)`** - Get HTTP proxy configuration
- **`GetSOCKS5ProxyURL(options)`** - Get SOCKS5 proxy URL
- **`GetCountries()`** - List available countries
- **`GetRegions()`** - List available regions

## Examples

See the [examples](./examples/) directory for complete working examples:

- **[basic_usage.go](./examples/basic_usage.go)** - Basic proxy usage and geo-targeting
- **[concurrent_usage.go](./examples/concurrent_usage.go)** - Concurrent requests and sticky sessions

## Error Handling

The SDK provides specific error types for different scenarios:

```go
proxy, err := client.GetProxyConfig(options)
if err != nil {
    switch e := err.(type) {
    case *nodemaven.AuthenticationError:
        log.Fatal("Invalid API key")
    case *nodemaven.RateLimitError:
        log.Fatal("Rate limit exceeded")
    case *nodemaven.ValidationError:
        log.Fatal("Invalid parameters:", e.Message)
    default:
        log.Fatal("Unexpected error:", err)
    }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 **Documentation**: [NodeMaven Docs](https://dashboard.nodemaven.com/documentation)
- 💬 **Telegram**: [@node_maven](https://t.me/node_maven)
- 📧 **Email**: Support via [NodeMaven Dashboard](https://dashboard.nodemaven.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/nodemavencom/proxy/issues)

## Links

- [NodeMaven Website](https://nodemaven.com)
- [Dashboard](https://dashboard.nodemaven.com)
- [API Documentation](https://dashboard.nodemaven.com/documentation)
- [Python SDK](https://github.com/nodemavencom/proxy/tree/main/python)
- [JavaScript SDK](https://github.com/nodemavencom/proxy/tree/main/javascript) 