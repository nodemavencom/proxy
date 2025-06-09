// Package nodemaven provides a Go client for the NodeMaven proxy service API.
// It offers access to residential and mobile proxies with global coverage.
package nodemaven

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
	"time"
)

const (
	// DefaultBaseURL is the default API base URL
	DefaultBaseURL = "https://dashboard.nodemaven.com"
	// DefaultProxyHost is the default proxy host
	DefaultProxyHost = "gate.nodemaven.com"
	// DefaultHTTPPort is the default HTTP proxy port
	DefaultHTTPPort = 8080
	// DefaultSOCKS5Port is the default SOCKS5 proxy port
	DefaultSOCKS5Port = 1080
	// DefaultTimeout is the default request timeout
	DefaultTimeout = 30 * time.Second
	// UserAgent is the client user agent string
	UserAgent = "NodeMaven-Go-Client/1.0.0"
)

// Client represents a NodeMaven API client
type Client struct {
	APIKey     string
	BaseURL    string
	ProxyHost  string
	HTTPPort   int
	SOCKS5Port int
	Timeout    time.Duration
	HTTPClient *http.Client
}

// Config holds configuration options for the NodeMaven client
type Config struct {
	APIKey     string
	BaseURL    string
	ProxyHost  string
	HTTPPort   int
	SOCKS5Port int
	Timeout    time.Duration
}

// NewClient creates a new NodeMaven client with the given configuration
func NewClient(config *Config) (*Client, error) {
	if config == nil {
		config = &Config{}
	}

	// Get API key from config or environment
	apiKey := config.APIKey
	if apiKey == "" {
		apiKey = os.Getenv("NODEMAVEN_APIKEY")
	}
	if apiKey == "" {
		return nil, fmt.Errorf("API key is required. Set NODEMAVEN_APIKEY environment variable or pass APIKey in config")
	}

	// Set defaults
	baseURL := config.BaseURL
	if baseURL == "" {
		baseURL = getEnvWithDefault("NODEMAVEN_BASE_URL", DefaultBaseURL)
	}

	proxyHost := config.ProxyHost
	if proxyHost == "" {
		proxyHost = getEnvWithDefault("NODEMAVEN_PROXY_HOST", DefaultProxyHost)
	}

	httpPort := config.HTTPPort
	if httpPort == 0 {
		httpPort = getEnvIntWithDefault("NODEMAVEN_HTTP_PORT", DefaultHTTPPort)
	}

	socks5Port := config.SOCKS5Port
	if socks5Port == 0 {
		socks5Port = getEnvIntWithDefault("NODEMAVEN_SOCKS5_PORT", DefaultSOCKS5Port)
	}

	timeout := config.Timeout
	if timeout == 0 {
		timeoutSecs := getEnvIntWithDefault("REQUEST_TIMEOUT", 30)
		timeout = time.Duration(timeoutSecs) * time.Second
	}

	return &Client{
		APIKey:     apiKey,
		BaseURL:    baseURL,
		ProxyHost:  proxyHost,
		HTTPPort:   httpPort,
		SOCKS5Port: socks5Port,
		Timeout:    timeout,
		HTTPClient: &http.Client{Timeout: timeout},
	}, nil
}

// makeRequest makes an HTTP request to the NodeMaven API
func (c *Client) makeRequest(ctx context.Context, method, endpoint string, params map[string]string, body interface{}) (map[string]interface{}, error) {
	// Build URL
	u, err := url.Parse(c.BaseURL + endpoint)
	if err != nil {
		return nil, fmt.Errorf("invalid URL: %w", err)
	}

	// Add query parameters
	if params != nil {
		q := u.Query()
		for key, value := range params {
			if value != "" {
				q.Set(key, value)
			}
		}
		u.RawQuery = q.Encode()
	}

	// Prepare request body
	var reqBody io.Reader
	if body != nil {
		jsonBody, err := json.Marshal(body)
		if err != nil {
			return nil, fmt.Errorf("failed to marshal request body: %w", err)
		}
		reqBody = bytes.NewBuffer(jsonBody)
	}

	// Create request
	req, err := http.NewRequestWithContext(ctx, method, u.String(), reqBody)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	// Set headers
	req.Header.Set("Authorization", "x-api-key "+c.APIKey)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Accept", "application/json")
	req.Header.Set("User-Agent", UserAgent)

	// Make request
	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("request failed: %w", err)
	}
	defer resp.Body.Close()

	// Read response body
	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response body: %w", err)
	}

	// Handle successful responses
	if resp.StatusCode < 400 {
		var result map[string]interface{}
		if len(respBody) > 0 {
			if err := json.Unmarshal(respBody, &result); err != nil {
				return nil, fmt.Errorf("failed to unmarshal response: %w", err)
			}
		} else {
			result = make(map[string]interface{})
		}
		return result, nil
	}

	// Handle error responses
	var errorData map[string]interface{}
	if len(respBody) > 0 {
		json.Unmarshal(respBody, &errorData)
	}

	errorMsg := parseErrorMessage(errorData, resp.StatusCode, resp.Status)
	return nil, getExceptionForStatusCode(resp.StatusCode, errorMsg, errorData)
}

// GetUserInfo retrieves current user information including proxy credentials and usage data
func (c *Client) GetUserInfo(ctx context.Context) (*UserInfo, error) {
	result, err := c.makeRequest(ctx, "GET", "/api/v2/base/users/me", nil, nil)
	if err != nil {
		return nil, err
	}

	userInfo := &UserInfo{}
	if err := mapToStruct(result, userInfo); err != nil {
		return nil, fmt.Errorf("failed to parse user info: %w", err)
	}

	return userInfo, nil
}

// GetCountries retrieves list of available countries for proxy connections
func (c *Client) GetCountries(ctx context.Context, req *CountriesRequest) (*CountriesResponse, error) {
	if req == nil {
		req = &CountriesRequest{Limit: 50, Offset: 0, ConnectionType: "residential"}
	}

	params := map[string]string{
		"limit":           strconv.Itoa(req.Limit),
		"offset":          strconv.Itoa(req.Offset),
		"connection_type": req.ConnectionType,
	}
	if req.Name != "" {
		params["name"] = req.Name
	}
	if req.Code != "" {
		params["code"] = req.Code
	}

	result, err := c.makeRequest(ctx, "GET", "/api/v2/base/locations/countries/", params, nil)
	if err != nil {
		return nil, err
	}

	response := &CountriesResponse{}
	if err := mapToStruct(result, response); err != nil {
		return nil, fmt.Errorf("failed to parse countries response: %w", err)
	}

	return response, nil
}

// GetRegions retrieves list of regions in specified countries
func (c *Client) GetRegions(ctx context.Context, req *RegionsRequest) (*RegionsResponse, error) {
	if req == nil {
		req = &RegionsRequest{Limit: 50, Offset: 0, ConnectionType: "residential"}
	}

	params := map[string]string{
		"limit":           strconv.Itoa(req.Limit),
		"offset":          strconv.Itoa(req.Offset),
		"connection_type": req.ConnectionType,
	}
	if req.CountryCode != "" {
		params["country__code"] = req.CountryCode
	}
	if req.Name != "" {
		params["name"] = req.Name
	}
	if req.Code != "" {
		params["code"] = req.Code
	}

	result, err := c.makeRequest(ctx, "GET", "/api/v2/base/locations/regions/", params, nil)
	if err != nil {
		return nil, err
	}

	response := &RegionsResponse{}
	if err := mapToStruct(result, response); err != nil {
		return nil, fmt.Errorf("failed to parse regions response: %w", err)
	}

	return response, nil
}

// GetCities retrieves list of cities in specified regions/countries
func (c *Client) GetCities(ctx context.Context, req *CitiesRequest) (*CitiesResponse, error) {
	if req == nil {
		req = &CitiesRequest{Limit: 50, Offset: 0, ConnectionType: "residential"}
	}

	params := map[string]string{
		"limit":           strconv.Itoa(req.Limit),
		"offset":          strconv.Itoa(req.Offset),
		"connection_type": req.ConnectionType,
	}
	if req.CountryCode != "" {
		params["country__code"] = req.CountryCode
	}
	if req.RegionCode != "" {
		params["region__code"] = req.RegionCode
	}
	if req.Name != "" {
		params["name"] = req.Name
	}
	if req.Code != "" {
		params["code"] = req.Code
	}

	result, err := c.makeRequest(ctx, "GET", "/api/v2/base/locations/cities/", params, nil)
	if err != nil {
		return nil, err
	}

	response := &CitiesResponse{}
	if err := mapToStruct(result, response); err != nil {
		return nil, fmt.Errorf("failed to parse cities response: %w", err)
	}

	return response, nil
}

// GetStatistics retrieves usage statistics for the current user
func (c *Client) GetStatistics(ctx context.Context, req *StatisticsRequest) (*StatisticsResponse, error) {
	if req == nil {
		req = &StatisticsRequest{GroupBy: "day"}
	}

	params := map[string]string{
		"group_by": req.GroupBy,
	}
	if req.StartDate != "" {
		params["start_date"] = req.StartDate
	}
	if req.EndDate != "" {
		params["end_date"] = req.EndDate
	}

	result, err := c.makeRequest(ctx, "GET", "/api/v2/base/traffic/statistics/", params, nil)
	if err != nil {
		return nil, err
	}

	response := &StatisticsResponse{}
	if err := mapToStruct(result, response); err != nil {
		return nil, fmt.Errorf("failed to parse statistics response: %w", err)
	}

	return response, nil
}

// GetProxyConfig returns proxy configuration for HTTP/HTTPS usage
func (c *Client) GetProxyConfig(options *ProxyOptions) (*ProxyConfig, error) {
	// Get proxy credentials from API
	ctx := context.Background()
	userInfo, err := c.GetUserInfo(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get proxy credentials: %w", err)
	}

	if userInfo.ProxyUsername == "" || userInfo.ProxyPassword == "" {
		return nil, fmt.Errorf("proxy credentials not available")
	}

	// Build proxy username with targeting
	username := buildProxyUsername(userInfo.ProxyUsername, options)

	return &ProxyConfig{
		Host:     c.ProxyHost,
		HTTPPort: c.HTTPPort,
		Username: username,
		Password: userInfo.ProxyPassword,
		client:   c,
		options:  options,
	}, nil
}

// GetSOCKS5ProxyURL returns SOCKS5 proxy URL with targeting parameters
func (c *Client) GetSOCKS5ProxyURL(options *ProxyOptions) (string, error) {
	// Get proxy credentials from API
	ctx := context.Background()
	userInfo, err := c.GetUserInfo(ctx)
	if err != nil {
		return "", fmt.Errorf("failed to get proxy credentials: %w", err)
	}

	if userInfo.ProxyUsername == "" || userInfo.ProxyPassword == "" {
		return "", fmt.Errorf("proxy credentials not available")
	}

	// Build proxy username with targeting
	username := buildProxyUsername(userInfo.ProxyUsername, options)

	return fmt.Sprintf("socks5://%s:%s@%s:%d",
		username, userInfo.ProxyPassword, c.ProxyHost, c.SOCKS5Port), nil
}

// Helper functions

func getEnvWithDefault(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvIntWithDefault(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intValue, err := strconv.Atoi(value); err == nil {
			return intValue
		}
	}
	return defaultValue
}

func parseErrorMessage(errorData map[string]interface{}, statusCode int, status string) string {
	if errorData == nil {
		return fmt.Sprintf("HTTP %d: %s", statusCode, status)
	}

	// Try to extract error message from various possible fields
	if msg, ok := errorData["message"].(string); ok && msg != "" {
		return msg
	}
	if msg, ok := errorData["error"].(string); ok && msg != "" {
		return msg
	}
	if msg, ok := errorData["detail"].(string); ok && msg != "" {
		return msg
	}

	// If we have errors array, format it
	if errors, ok := errorData["errors"].([]interface{}); ok && len(errors) > 0 {
		var messages []string
		for _, err := range errors {
			if errStr, ok := err.(string); ok {
				messages = append(messages, errStr)
			}
		}
		if len(messages) > 0 {
			return strings.Join(messages, "; ")
		}
	}

	return fmt.Sprintf("HTTP %d: %s", statusCode, status)
}

func mapToStruct(data map[string]interface{}, target interface{}) error {
	jsonData, err := json.Marshal(data)
	if err != nil {
		return err
	}
	return json.Unmarshal(jsonData, target)
}
