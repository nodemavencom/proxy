package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"time"

	"github.com/nodemavencom/proxy/go/nodemaven"
)

func main() {
	fmt.Println("NodeMaven Go SDK - Basic Usage Example")
	fmt.Println("=====================================")

	// Initialize client
	client, err := nodemaven.NewClient(&nodemaven.Config{
		// APIKey will be read from NODEMAVEN_APIKEY environment variable
	})
	if err != nil {
		log.Fatalf("Failed to initialize client: %v", err)
	}

	fmt.Println("✓ Client initialized successfully")

	ctx := context.Background()

	// Example 1: Basic proxy usage
	fmt.Println("\n1. Basic Proxy Usage")
	fmt.Println("-------------------")
	
	basicProxy, err := client.GetProxyConfig(nil)
	if err != nil {
		log.Printf("Failed to get basic proxy config: %v", err)
	} else {
		ip, err := testProxyConnection(basicProxy)
		if err != nil {
			fmt.Printf("Error: %v\n", err)
		} else {
			fmt.Printf("✓ Basic proxy working! Your IP: %s\n", ip)
		}
	}

	// Example 2: Geo-targeted proxy
	fmt.Println("\n2. Geo-targeted Proxy (US)")
	fmt.Println("-------------------------")
	
	usProxy, err := client.GetProxyConfig(&nodemaven.ProxyOptions{
		Country: "US",
	})
	if err != nil {
		log.Printf("Failed to get US proxy config: %v", err)
	} else {
		ip, err := testProxyConnection(usProxy)
		if err != nil {
			fmt.Printf("Error: %v\n", err)
		} else {
			fmt.Printf("✓ US proxy working! Your IP: %s\n", ip)
		}
	}

	// Example 3: Sticky session
	fmt.Println("\n3. Sticky Session")
	fmt.Println("----------------")
	
	sessionID := "example_session_" + nodemaven.GenerateSessionID()
	sessionProxy, err := client.GetProxyConfig(&nodemaven.ProxyOptions{
		Country: "US",
		Session: sessionID,
	})
	if err != nil {
		log.Printf("Failed to get session proxy config: %v", err)
	} else {
		// Make multiple requests with same session
		var ips []string
		for i := 1; i <= 3; i++ {
			ip, err := testProxyConnection(sessionProxy)
			if err != nil {
				fmt.Printf("Request %d failed: %v\n", i, err)
			} else {
				fmt.Printf("✓ Request %d successful! IP: %s\n", i, ip)
				ips = append(ips, ip)
			}

			// Small delay between requests
			if i < 3 {
				time.Sleep(200 * time.Millisecond)
			}
		}

		// Check if all IPs are the same (sticky session working)
		if len(ips) > 0 {
			allSame := true
			firstIP := ips[0]
			for _, ip := range ips {
				if ip != firstIP {
					allSame = false
					break
				}
			}

			if allSame {
				fmt.Printf("✓ Sticky session working! All requests used same IP: %s\n", firstIP)
			} else {
				fmt.Printf("Warning: Sticky session may not be working - got different IPs\n")
			}
		}
	}

	// Example 4: Get account information
	fmt.Println("\n4. Account Information")
	fmt.Println("---------------------")
	
	userInfo, err := client.GetUserInfo(ctx)
	if err != nil {
		log.Printf("Failed to get user info: %v", err)
	} else {
		fmt.Printf("✓ Email: %s\n", userInfo.Email)
		if userInfo.TrafficLimit > 0 {
			remaining := userInfo.TrafficLimit - userInfo.TrafficUsed
			if remaining < 0 {
				remaining = 0
			}
			fmt.Printf("✓ Data Remaining: %s\n", nodemaven.FormatBytes(remaining))
		}
	}

	fmt.Println("\nExample completed successfully!")
}

// testProxyConnection tests a proxy connection and returns the IP address
func testProxyConnection(proxyConfig *nodemaven.ProxyConfig) (string, error) {
	client := proxyConfig.HTTPClientWithTimeout(15 * time.Second)

	resp, err := client.Get("https://httpbin.org/ip")
	if err != nil {
		return "", fmt.Errorf("request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("returned status %d", resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to read response: %w", err)
	}

	var result map[string]interface{}
	if err := json.Unmarshal(body, &result); err != nil {
		return "", fmt.Errorf("failed to parse JSON: %w", err)
	}

	if origin, ok := result["origin"].(string); ok {
		return origin, nil
	}

	return "", fmt.Errorf("did not return IP in expected format")
}
