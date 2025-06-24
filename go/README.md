# NodeMaven Go SDK 🔷

**Status: Testing** - Basic functionality implemented, not production-ready.

## Quick Setup

```bash
cd go
go mod tidy
export NODEMAVEN_APIKEY="your_api_key_here"
go run examples/basic_usage.go
```

## Basic Usage

```go
package main

import (
    "fmt"
    "github.com/nodemavencom/proxy/go/nodemaven"
)

func main() {
    client, err := nodemaven.NewClient(&nodemaven.Config{})
    if err != nil {
        panic(err)
    }
    
    proxy, err := client.GetProxyConfig(&nodemaven.ProxyOptions{
        Country: "US",
    })
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("Proxy: %+v\n", proxy)
}
```

## Structure

- `nodemaven/` - Core Go package
- `examples/` - Basic usage examples

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