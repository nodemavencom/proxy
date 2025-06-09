package nodemaven

import (
	"context"
	"net/http"
	"net/url"
	"time"
)

// UserInfo represents user account information
type UserInfo struct {
	ID               string `json:"id"`
	Email            string `json:"email"`
	ProxyUsername    string `json:"proxy_username"`
	ProxyPassword    string `json:"proxy_password"`
	TrafficUsed      int64  `json:"traffic_used"`
	TrafficLimit     int64  `json:"traffic_limit"`
	Subscription     string `json:"subscription"`
	SubscriptionType string `json:"subscription_type"`
	IsActive         bool   `json:"is_active"`
	DateJoined       string `json:"date_joined"`
}

// Country represents a country location
type Country struct {
	ID             string `json:"id"`
	Name           string `json:"name"`
	Code           string `json:"code"`
	ConnectionType string `json:"connection_type"`
	RegionsCount   int    `json:"regions_count"`
	CitiesCount    int    `json:"cities_count"`
	ProxiesCount   int    `json:"proxies_count"`
}

// Region represents a region/state location
type Region struct {
	ID             string `json:"id"`
	Name           string `json:"name"`
	Code           string `json:"code"`
	Country        string `json:"country"`
	CountryCode    string `json:"country_code"`
	ConnectionType string `json:"connection_type"`
	CitiesCount    int    `json:"cities_count"`
	ProxiesCount   int    `json:"proxies_count"`
}

// City represents a city location
type City struct {
	ID             string `json:"id"`
	Name           string `json:"name"`
	Code           string `json:"code"`
	Country        string `json:"country"`
	CountryCode    string `json:"country_code"`
	Region         string `json:"region"`
	RegionCode     string `json:"region_code"`
	ConnectionType string `json:"connection_type"`
	ProxiesCount   int    `json:"proxies_count"`
}

// StatisticEntry represents a single statistics entry
type StatisticEntry struct {
	Date        string  `json:"date"`
	TrafficUsed int64   `json:"traffic_used"`
	Requests    int     `json:"requests"`
	SuccessRate float64 `json:"success_rate"`
}

// Request and Response types

// CountriesRequest represents a request for countries
type CountriesRequest struct {
	Limit          int    `json:"limit"`
	Offset         int    `json:"offset"`
	Name           string `json:"name,omitempty"`
	Code           string `json:"code,omitempty"`
	ConnectionType string `json:"connection_type"`
}

// CountriesResponse represents the response for countries
type CountriesResponse struct {
	Count    int       `json:"count"`
	Next     *string   `json:"next"`
	Previous *string   `json:"previous"`
	Results  []Country `json:"results"`
}

// RegionsRequest represents a request for regions
type RegionsRequest struct {
	Limit          int    `json:"limit"`
	Offset         int    `json:"offset"`
	CountryCode    string `json:"country_code,omitempty"`
	Name           string `json:"name,omitempty"`
	Code           string `json:"code,omitempty"`
	ConnectionType string `json:"connection_type"`
}

// RegionsResponse represents the response for regions
type RegionsResponse struct {
	Count    int      `json:"count"`
	Next     *string  `json:"next"`
	Previous *string  `json:"previous"`
	Results  []Region `json:"results"`
}

// CitiesRequest represents a request for cities
type CitiesRequest struct {
	Limit          int    `json:"limit"`
	Offset         int    `json:"offset"`
	CountryCode    string `json:"country_code,omitempty"`
	RegionCode     string `json:"region_code,omitempty"`
	Name           string `json:"name,omitempty"`
	Code           string `json:"code,omitempty"`
	ConnectionType string `json:"connection_type"`
}

// CitiesResponse represents the response for cities
type CitiesResponse struct {
	Count    int     `json:"count"`
	Next     *string `json:"next"`
	Previous *string `json:"previous"`
	Results  []City  `json:"results"`
}

// StatisticsRequest represents a request for statistics
type StatisticsRequest struct {
	StartDate string `json:"start_date,omitempty"`
	EndDate   string `json:"end_date,omitempty"`
	GroupBy   string `json:"group_by"`
}

// StatisticsResponse represents the response for statistics
type StatisticsResponse struct {
	Count    int              `json:"count"`
	Next     *string          `json:"next"`
	Previous *string          `json:"previous"`
	Results  []StatisticEntry `json:"results"`
}

// ProxyOptions represents proxy targeting options
type ProxyOptions struct {
	Country        string `json:"country,omitempty"`
	Region         string `json:"region,omitempty"`
	City           string `json:"city,omitempty"`
	ISP            string `json:"isp,omitempty"`
	ZipCode        string `json:"zip_code,omitempty"`
	ASN            string `json:"asn,omitempty"`
	Session        string `json:"session,omitempty"`
	ConnectionType string `json:"connection_type,omitempty"`
	Protocol       string `json:"protocol,omitempty"`
	OS             string `json:"os,omitempty"`
	Browser        string `json:"browser,omitempty"`
}

// ProxyConfig represents a proxy configuration for HTTP/HTTPS usage
type ProxyConfig struct {
	Host     string
	HTTPPort int
	Username string
	Password string
	client   *Client
	options  *ProxyOptions
}

// HTTPClient returns an HTTP client configured to use the proxy
func (p *ProxyConfig) HTTPClient() *http.Client {
	proxyURL, _ := url.Parse(p.ProxyURL())

	transport := &http.Transport{
		Proxy: http.ProxyURL(proxyURL),
	}

	return &http.Client{
		Transport: transport,
		Timeout:   p.client.Timeout,
	}
}

// HTTPClientWithTimeout returns an HTTP client with custom timeout
func (p *ProxyConfig) HTTPClientWithTimeout(timeout time.Duration) *http.Client {
	proxyURL, _ := url.Parse(p.ProxyURL())

	transport := &http.Transport{
		Proxy: http.ProxyURL(proxyURL),
	}

	return &http.Client{
		Transport: transport,
		Timeout:   timeout,
	}
}

// HTTPClientWithContext returns an HTTP client that respects context cancellation
func (p *ProxyConfig) HTTPClientWithContext(ctx context.Context) *http.Client {
	proxyURL, _ := url.Parse(p.ProxyURL())

	transport := &http.Transport{
		Proxy: http.ProxyURL(proxyURL),
	}

	client := &http.Client{
		Transport: transport,
		Timeout:   p.client.Timeout,
	}

	// Wrap the transport to handle context cancellation
	client.Transport = &contextTransport{
		base: transport,
		ctx:  ctx,
	}

	return client
}

// ProxyURL returns the HTTP proxy URL
func (p *ProxyConfig) ProxyURL() string {
	return buildProxyURL("http", p.Host, p.HTTPPort, p.Username, p.Password)
}

// HTTPSProxyURL returns the HTTPS proxy URL
func (p *ProxyConfig) HTTPSProxyURL() string {
	return buildProxyURL("https", p.Host, p.HTTPPort, p.Username, p.Password)
}

// contextTransport wraps http.Transport to handle context cancellation
type contextTransport struct {
	base http.RoundTripper
	ctx  context.Context
}

func (t *contextTransport) RoundTrip(req *http.Request) (*http.Response, error) {
	select {
	case <-t.ctx.Done():
		return nil, t.ctx.Err()
	default:
		return t.base.RoundTrip(req.WithContext(t.ctx))
	}
}
