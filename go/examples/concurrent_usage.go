package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"sync"
	"time"

	"github.com/nodemavencom/proxy/go/nodemaven"
)

func main() {
	fmt.Println("NodeMaven Go SDK - Concurrent Usage Example")
	fmt.Println("==========================================")

	// Initialize client
	client, err := nodemaven.NewClient(&nodemaven.Config{
		// APIKey will be read from NODEMAVEN_APIKEY environment variable
	})
	if err != nil {
		log.Fatalf("Failed to initialize client: %v", err)
	}

	fmt.Println("✓ Client initialized successfully")

	// Example 1: Concurrent requests with unique sessions
	fmt.Println("\n1. Concurrent Requests with Unique Sessions")
	fmt.Println("-------------------------------------------")
	
	concurrentRequests(client, 5)

	// Example 2: Concurrent requests to different countries
	fmt.Println("\n2. Concurrent Requests to Different Countries")
	fmt.Println("---------------------------------------------")
	
	geoTargetedRequests(client)

	fmt.Println("\nExample completed successfully!")
}

// concurrentRequests demonstrates concurrent usage with unique sessions
func concurrentRequests(client *nodemaven.Client, numWorkers int) {
	var wg sync.WaitGroup
	results := make(chan string, numWorkers)

	fmt.Printf("Starting %d concurrent workers...\n", numWorkers)

	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()

			// Create unique session for this worker
			sessionID := fmt.Sprintf("worker_%d_%d", workerID, time.Now().Unix())
			
			proxy, err := client.GetProxyConfig(&nodemaven.ProxyOptions{
				Country: "US",
				Session: sessionID,
			})
			if err != nil {
				results <- fmt.Sprintf("Worker %d: Failed to get proxy config: %v", workerID, err)
				return
			}

			// Make request through proxy
			ip, err := testProxyConnection(proxy)
			if err != nil {
				results <- fmt.Sprintf("Worker %d: Request failed: %v", workerID, err)
				return
			}

			results <- fmt.Sprintf("Worker %d: Success! IP: %s (Session: %s)", workerID, ip, sessionID)
		}(i)
	}

	// Close results channel when all workers are done
	go func() {
		wg.Wait()
		close(results)
	}()

	// Collect and display results
	for result := range results {
		fmt.Printf("✓ %s\n", result)
	}
}

// geoTargetedRequests demonstrates concurrent requests to different countries
func geoTargetedRequests(client *nodemaven.Client) {
	countries := []string{"US", "UK", "DE", "CA", "AU"}
	var wg sync.WaitGroup
	results := make(chan string, len(countries))

	fmt.Printf("Making concurrent requests to %d countries...\n", len(countries))

	for _, country := range countries {
		wg.Add(1)
		go func(countryCode string) {
			defer wg.Done()

			proxy, err := client.GetProxyConfig(&nodemaven.ProxyOptions{
				Country: countryCode,
				Session: fmt.Sprintf("geo_%s_%d", countryCode, time.Now().Unix()),
			})
			if err != nil {
				results <- fmt.Sprintf("%s: Failed to get proxy config: %v", countryCode, err)
				return
			}

			ip, err := testProxyConnection(proxy)
			if err != nil {
				results <- fmt.Sprintf("%s: Request failed: %v", countryCode, err)
				return
			}

			results <- fmt.Sprintf("%s: Success! IP: %s", countryCode, ip)
		}(country)
	}

	// Close results channel when all workers are done
	go func() {
		wg.Wait()
		close(results)
	}()

	// Collect and display results
	for result := range results {
		fmt.Printf("✓ %s\n", result)
	}
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
