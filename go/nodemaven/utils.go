package nodemaven

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"math"
	"net/http"
	"net/url"
	"regexp"
	"strconv"
	"strings"
	"time"
)

// FormatBytes formats byte values into human-readable strings
func FormatBytes(bytes int64) string {
	if bytes == 0 {
		return "0 B"
	}

	sizes := []string{"B", "KB", "MB", "GB", "TB"}
	sizeIndex := 0
	value := float64(bytes)

	for value >= 1024 && sizeIndex < len(sizes)-1 {
		value /= 1024
		sizeIndex++
	}

	if sizeIndex == 0 {
		return fmt.Sprintf("%.0f %s", value, sizes[sizeIndex])
	}
	return fmt.Sprintf("%.2f %s", value, sizes[sizeIndex])
}

// ValidateProxyUsername validates proxy username format
func ValidateProxyUsername(username string) bool {
	if username == "" {
		return false
	}
	// Username must be alphanumeric and underscores only, 9-100 characters
	pattern := regexp.MustCompile(`^[a-zA-Z0-9_]{9,100}$`)
	return pattern.MatchString(username)
}

// ValidateProxyPassword validates proxy password format
func ValidateProxyPassword(password string) bool {
	if password == "" {
		return false
	}
	// Password must be alphanumeric and underscores only, 9-100 characters
	pattern := regexp.MustCompile(`^[a-zA-Z0-9_]{9,100}$`)
	return pattern.MatchString(password)
}

// ValidateDateFormat validates date string in dd-mm-yyyy format
func ValidateDateFormat(dateString string) error {
	_, err := time.Parse("02-01-2006", dateString)
	if err != nil {
		return fmt.Errorf("invalid date format for '%s'. Expected dd-mm-yyyy", dateString)
	}
	return nil
}

// GenerateSessionID generates a random session ID
func GenerateSessionID() string {
	bytes := make([]byte, 7) // 7 bytes = 14 hex chars, truncate to 13
	rand.Read(bytes)
	return hex.EncodeToString(bytes)[:13]
}

// buildProxyUsername builds NodeMaven proxy username with targeting parameters
// Format matches Python implementation exactly: base_username-country-us-region-california-city-newyork-ipv4-true-sid-sessionid-filter-medium
func buildProxyUsername(baseUsername string, options *ProxyOptions) string {
	if options == nil {
		// Even with no options, we need the required default parameters
		return baseUsername + "-ipv4-true-filter-medium"
	}

	parts := []string{baseUsername}

	// Add targeting parameters in the exact order as Python implementation
	if options.Country != "" {
		parts = append(parts, "country", strings.ToLower(options.Country))
	}
	if options.Region != "" {
		// Convert spaces to nothing and make lowercase (like Python implementation)
		region := strings.ToLower(strings.ReplaceAll(strings.ReplaceAll(options.Region, " ", ""), "_", ""))
		parts = append(parts, "region", region)
	}
	if options.City != "" {
		// Convert spaces to nothing and make lowercase (like Python implementation)
		city := strings.ToLower(strings.ReplaceAll(strings.ReplaceAll(options.City, " ", ""), "_", ""))
		parts = append(parts, "city", city)
	}
	if options.ISP != "" {
		// Convert spaces to nothing and make lowercase (like Python implementation)
		isp := strings.ToLower(strings.ReplaceAll(strings.ReplaceAll(options.ISP, " ", ""), "_", ""))
		parts = append(parts, "isp", isp)
	}
	if options.ZipCode != "" {
		parts = append(parts, "zip", options.ZipCode)
	}
	if options.ASN != "" {
		parts = append(parts, "asn", options.ASN)
	}

	// Connection type (mobile, residential) - add before ipv4 parameter
	if options.ConnectionType != "" && options.ConnectionType != "residential" {
		parts = append(parts, "type", strings.ToLower(options.ConnectionType))
	}

	// IP version (always add ipv4-true to match Python format exactly)
	parts = append(parts, "ipv4", "true")

	// Session ID for sticky sessions (use 'sid' to match Python exactly, not 'session')
	if options.Session != "" {
		parts = append(parts, "sid", options.Session)
	}

	// Additional parameters from ProxyOptions
	if options.Protocol != "" {
		parts = append(parts, "protocol", strings.ToLower(options.Protocol))
	}
	if options.OS != "" {
		parts = append(parts, "os", strings.ToLower(options.OS))
	}
	if options.Browser != "" {
		parts = append(parts, "browser", strings.ToLower(options.Browser))
	}

	// IP filter quality (always add to match Python format exactly)
	parts = append(parts, "filter", "medium")

	return strings.Join(parts, "-")
}

// buildProxyURL builds a proxy URL
func buildProxyURL(protocol, host string, port int, username, password string) string {
	return fmt.Sprintf("%s://%s:%s@%s:%d", protocol, username, password, host, port)
}

// GetCurrentIP fetches current IP address using the provided HTTP client
func GetCurrentIP(client *http.Client) (string, error) {
	if client == nil {
		client = &http.Client{Timeout: 10 * time.Second}
	}

	// Try multiple IP checking services
	services := []string{
		"https://httpbin.org/ip",
		"https://api.ipify.org?format=json",
		"https://ip-api.com/json?fields=query",
	}

	for _, service := range services {
		resp, err := client.Get(service)
		if err != nil {
			continue
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			continue
		}

		// Parse JSON response based on service
		var result map[string]interface{}
		if err := parseJSONResponse(resp, &result); err != nil {
			continue
		}

		// Extract IP from different response formats
		if ip := extractIPFromResponse(result); ip != "" {
			return ip, nil
		}
	}

	return "", fmt.Errorf("failed to get current IP from any service")
}

// CheckIPWithDetails fetches detailed IP information
func CheckIPWithDetails(client *http.Client) (map[string]interface{}, error) {
	if client == nil {
		client = &http.Client{Timeout: 10 * time.Second}
	}

	resp, err := client.Get("https://ip-api.com/json")
	if err != nil {
		return nil, fmt.Errorf("failed to get IP details: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("IP service returned status %d", resp.StatusCode)
	}

	var result map[string]interface{}
	if err := parseJSONResponse(resp, &result); err != nil {
		return nil, fmt.Errorf("failed to parse IP details response: %w", err)
	}

	return result, nil
}

// IPChecker represents an IP checking service
type IPChecker struct {
	Name string
	URL  string
}

// GetSupportedIPCheckers returns list of supported IP checking services
func GetSupportedIPCheckers() []IPChecker {
	return []IPChecker{
		{Name: "HTTPBin", URL: "https://httpbin.org/ip"},
		{Name: "IPify", URL: "https://api.ipify.org?format=json"},
		{Name: "IP-API", URL: "https://ip-api.com/json?fields=query"},
		{Name: "IPInfo", URL: "https://ipinfo.io/json"},
	}
}

// TestProxyConnection tests a proxy connection and returns the IP address
func TestProxyConnection(proxyConfig *ProxyConfig, description string) (string, error) {
	client := proxyConfig.HTTPClient()

	ip, err := GetCurrentIP(client)
	if err != nil {
		return "", fmt.Errorf("%s failed: %w", description, err)
	}

	return ip, nil
}

// Helper functions for JSON parsing

func parseJSONResponse(resp *http.Response, target interface{}) error {
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("failed to read response body: %w", err)
	}

	if len(body) == 0 {
		return fmt.Errorf("empty response body")
	}

	if err := json.Unmarshal(body, target); err != nil {
		return fmt.Errorf("failed to unmarshal JSON: %w", err)
	}

	return nil
}

func extractIPFromResponse(result map[string]interface{}) string {
	// Try different field names used by various IP services
	if ip, ok := result["origin"].(string); ok {
		return ip
	}
	if ip, ok := result["ip"].(string); ok {
		return ip
	}
	if ip, ok := result["query"].(string); ok {
		return ip
	}
	return ""
}

// BuildHTTPProxyFromURL creates a proxy function from a proxy URL
func BuildHTTPProxyFromURL(proxyURL string) func(*http.Request) (*url.URL, error) {
	return func(req *http.Request) (*url.URL, error) {
		return url.Parse(proxyURL)
	}
}

// CleanMap removes empty values from a map
func CleanMap(data map[string]string) map[string]string {
	cleaned := make(map[string]string)
	for key, value := range data {
		if value != "" {
			cleaned[key] = value
		}
	}
	return cleaned
}

// StringToInt converts string to int with default value
func StringToInt(s string, defaultValue int) int {
	if i, err := strconv.Atoi(s); err == nil {
		return i
	}
	return defaultValue
}

// StringToBool converts string to bool
func StringToBool(s string) bool {
	lower := strings.ToLower(s)
	return lower == "true" || lower == "1" || lower == "yes" || lower == "on"
}

// CalculateSuccessRate calculates success rate percentage
func CalculateSuccessRate(successful, total int) float64 {
	if total == 0 {
		return 0.0
	}
	return math.Round((float64(successful)/float64(total))*10000) / 100
}

// IsValidCountryCode validates ISO country codes
func IsValidCountryCode(code string) bool {
	if len(code) != 2 {
		return false
	}
	pattern := regexp.MustCompile(`^[A-Z]{2}$`)
	return pattern.MatchString(strings.ToUpper(code))
}

// NormalizeCountryCode normalizes country code to uppercase
func NormalizeCountryCode(code string) string {
	return strings.ToUpper(strings.TrimSpace(code))
}

// SanitizeSessionID sanitizes session ID to remove invalid characters
func SanitizeSessionID(sessionID string) string {
	// Remove any characters that aren't alphanumeric or underscore
	pattern := regexp.MustCompile(`[^a-zA-Z0-9_]`)
	sanitized := pattern.ReplaceAllString(sessionID, "")

	// Truncate to reasonable length
	if len(sanitized) > 50 {
		sanitized = sanitized[:50]
	}

	return sanitized
}
