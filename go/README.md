# NodeMaven Go SDK 🔵

[![Go](https://img.shields.io/badge/Go-Coming%20Soon-cyan?style=for-the-badge&logo=go)](https://github.com/nodemaven/nodemaven/issues)
[![Go Modules](https://img.shields.io/badge/Go%20Modules-Ready-green?style=for-the-badge)](https://golang.org/ref/mod)
[![pkg.go.dev](https://img.shields.io/badge/pkg.go.dev-Coming%20Soon-blue?style=for-the-badge)](https://pkg.go.dev/)

> **Go SDK for NodeMaven Proxy API** - Coming Soon!

## 🚧 Under Development

We're crafting a high-performance Go SDK for NodeMaven with idiomatic Go patterns:

### 🎯 Planned Features
- **Go 1.19+** - Modern Go with generics support
- **Zero Dependencies** - Pure standard library implementation
- **Context Support** - Proper context handling for cancellation
- **Concurrent Safe** - Thread-safe client implementation
- **HTTP/2 Support** - Modern HTTP protocol support

### 📦 Expected API
```go
package main

import (
    "context"
    "fmt"
    "log"
    
    "github.com/nodemaven/go-sdk"
)

func main() {
    client := nodemaven.NewClient(&nodemaven.Config{
        APIKey: "your_api_key_here",
    })
    
    ctx := context.Background()
    
    // Get user information
    userInfo, err := client.GetUserInfo(ctx)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("Username: %s\n", userInfo.ProxyUsername)
    
    // Get countries
    countries, err := client.GetCountries(ctx, &nodemaven.CountriesRequest{
        Limit: 10,
    })
    if err != nil {
        log.Fatal(err)
    }
    
    for _, country := range countries.Results {
        fmt.Printf("%s (%s)\n", country.Name, country.Code)
    }
    
    // Use with HTTP client
    proxyConfig := client.GetProxyConfig(&nodemaven.ProxyOptions{
        Country: "US",
        City:    "new_york",
    })
    
    httpClient := proxyConfig.HTTPClient()
    resp, err := httpClient.Get("https://httpbin.org/ip")
    if err != nil {
        log.Fatal(err)
    }
    defer resp.Body.Close()
}
```

### 🔧 Advanced Usage
```go
// With context and timeout
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

// Concurrent requests
var wg sync.WaitGroup
for i := 0; i < 10; i++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        
        proxy := client.GetProxyConfig(&nodemaven.ProxyOptions{
            Country: "US",
            Session: fmt.Sprintf("session_%d", id),
        })
        
        // Make request with unique session
        resp, err := proxy.HTTPClient().Get("https://httpbin.org/ip")
        if err != nil {
            log.Printf("Request %d failed: %v", id, err)
            return
        }
        defer resp.Body.Close()
        
        fmt.Printf("Request %d completed\n", id)
    }(i)
}
wg.Wait()
```

## 🤝 Want to Help?

We'd love your contribution! Here's how you can help:

1. **⭐ Star this repo** to show interest
2. **💬 Join the discussion** in [GitHub Issues](https://github.com/nodemaven/nodemaven/issues)
3. **🔧 Contribute code** - we welcome pull requests!
4. **📝 Share feedback** on Go-specific features you need

## 📞 Stay Updated

- 📧 **Email**: [support@nodemaven.com](mailto:support@nodemaven.com)
- 💬 **Live Chat**: [Dashboard Support](https://dashboard.nodemaven.com/support/?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=go_support)
- 🐛 **Issues**: [GitHub Issues](https://github.com/nodemaven/nodemaven/issues)

## 🐍 Available Now: Python SDK

While you wait for the Go SDK, check out our fully-featured [Python SDK](../python/) that's ready to use today!

---

<div align="center">

**[🚀 Get Started with Python](../python/)** • **[📖 API Docs](https://dashboard.nodemaven.com/documentation/?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=go_docs)** • **[💬 Request Features](https://github.com/nodemaven/nodemaven/issues)**

</div> 