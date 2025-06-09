<?php

declare(strict_types=1);

namespace NodeMaven;

use GuzzleHttp\Client as GuzzleClient;
use GuzzleHttp\Exception\GuzzleException;
use GuzzleHttp\RequestOptions;
use NodeMaven\Exceptions\AuthenticationException;
use NodeMaven\Exceptions\NodeMavenException;
use NodeMaven\Exceptions\RateLimitException;
use NodeMaven\Exceptions\ValidationException;

/**
 * NodeMaven API Client
 * 
 * Main client for interacting with NodeMaven proxy API
 */
class Client
{
    private const DEFAULT_BASE_URL = 'https://dashboard.nodemaven.com';
    private const DEFAULT_PROXY_HOST = 'gate.nodemaven.com';
    private const DEFAULT_HTTP_PORT = 8080;
    private const DEFAULT_SOCKS5_PORT = 1080;
    private const DEFAULT_TIMEOUT = 30;

    private string $apiKey;
    private string $baseUrl;
    private string $proxyHost;
    private int $httpPort;
    private int $socks5Port;
    private int $timeout;
    private GuzzleClient $httpClient;

    /**
     * Initialize NodeMaven client
     * 
     * @param array $config Configuration options
     * @throws NodeMavenException
     */
    public function __construct(array $config = [])
    {
        $this->apiKey = $config['api_key'] ?? $this->getApiKeyFromEnv();
        $this->baseUrl = $config['base_url'] ?? $_ENV['NODEMAVEN_BASE_URL'] ?? self::DEFAULT_BASE_URL;
        $this->proxyHost = $config['proxy_host'] ?? $_ENV['NODEMAVEN_PROXY_HOST'] ?? self::DEFAULT_PROXY_HOST;
        $this->httpPort = (int) ($config['http_port'] ?? $_ENV['NODEMAVEN_HTTP_PORT'] ?? self::DEFAULT_HTTP_PORT);
        $this->socks5Port = (int) ($config['socks5_port'] ?? $_ENV['NODEMAVEN_SOCKS5_PORT'] ?? self::DEFAULT_SOCKS5_PORT);
        $this->timeout = (int) ($config['timeout'] ?? $_ENV['REQUEST_TIMEOUT'] ?? self::DEFAULT_TIMEOUT);

        if (empty($this->apiKey)) {
            throw new NodeMavenException('API key is required. Set NODEMAVEN_APIKEY environment variable or pass api_key in config.');
        }

        $this->initializeHttpClient();
    }

    /**
     * Get user information and account details
     * 
     * @return array User information including proxy credentials
     * @throws NodeMavenException
     */
    public function getUserInfo(): array
    {
        return $this->makeRequest('GET', '/api/v1/user-info');
    }

    /**
     * Get available countries
     * 
     * @param array $options Query options (limit, offset, etc.)
     * @return array Countries data
     * @throws NodeMavenException
     */
    public function getCountries(array $options = []): array
    {
        $query = http_build_query($options);
        $endpoint = '/api/v1/countries' . ($query ? '?' . $query : '');
        return $this->makeRequest('GET', $endpoint);
    }

    /**
     * Get regions for a specific country
     * 
     * @param array $options Query options (country_code, limit, etc.)
     * @return array Regions data
     * @throws NodeMavenException
     */
    public function getRegions(array $options = []): array
    {
        $query = http_build_query($options);
        $endpoint = '/api/v1/regions' . ($query ? '?' . $query : '');
        return $this->makeRequest('GET', $endpoint);
    }

    /**
     * Get cities for a specific country/region
     * 
     * @param array $options Query options (country_code, region_code, limit, etc.)
     * @return array Cities data
     * @throws NodeMavenException
     */
    public function getCities(array $options = []): array
    {
        $query = http_build_query($options);
        $endpoint = '/api/v1/cities' . ($query ? '?' . $query : '');
        return $this->makeRequest('GET', $endpoint);
    }

    /**
     * Get proxy configuration
     * 
     * @param array $options Proxy options (country, region, city, session, etc.)
     * @return ProxyConfig Proxy configuration object
     * @throws NodeMavenException
     */
    public function getProxyConfig(array $options = []): ProxyConfig
    {
        $userInfo = $this->getUserInfo();
        
        $username = $userInfo['proxy_username'] ?? '';
        $password = $userInfo['proxy_password'] ?? '';

        if (empty($username) || empty($password)) {
            throw new NodeMavenException('Unable to retrieve proxy credentials. Check if your account has proxy access enabled.');
        }

        return new ProxyConfig([
            'host' => $this->proxyHost,
            'http_port' => $this->httpPort,
            'socks5_port' => $this->socks5Port,
            'username' => Utils::formatProxyUsername($username, $options),
            'password' => $password,
            'options' => $options
        ]);
    }

    /**
     * Get SOCKS5 proxy URL
     * 
     * @param array $options Proxy options
     * @return string SOCKS5 proxy URL
     * @throws NodeMavenException
     */
    public function getSocks5ProxyUrl(array $options = []): string
    {
        $proxyConfig = $this->getProxyConfig($options);
        return $proxyConfig->getSocks5Url();
    }

    /**
     * Get HTTP proxy configuration for Guzzle
     * 
     * @param array $options Proxy options
     * @return array Guzzle proxy configuration
     * @throws NodeMavenException
     */
    public function getGuzzleProxyConfig(array $options = []): array
    {
        $proxyConfig = $this->getProxyConfig($options);
        return $proxyConfig->getGuzzleConfig();
    }

    /**
     * Create HTTP client with proxy configuration
     * 
     * @param array $options Proxy options
     * @param array $clientConfig Additional Guzzle client configuration
     * @return GuzzleClient HTTP client with proxy
     * @throws NodeMavenException
     */
    public function createHttpClient(array $options = [], array $clientConfig = []): GuzzleClient
    {
        $proxyConfig = $this->getProxyConfig($options);
        return $proxyConfig->createHttpClient($clientConfig);
    }

    /**
     * Initialize HTTP client for API requests
     */
    private function initializeHttpClient(): void
    {
        $this->httpClient = new GuzzleClient([
            'base_uri' => $this->baseUrl,
            'timeout' => $this->timeout,
            'headers' => [
                'User-Agent' => 'NodeMaven-PHP-SDK/1.0.0',
                'Accept' => 'application/json',
                'Authorization' => 'Bearer ' . $this->apiKey,
            ]
        ]);
    }

    /**
     * Make API request
     * 
     * @param string $method HTTP method
     * @param string $endpoint API endpoint
     * @param array $data Request data
     * @return array Response data
     * @throws NodeMavenException
     */
    private function makeRequest(string $method, string $endpoint, array $data = []): array
    {
        try {
            $options = [];
            
            if (!empty($data)) {
                $options[RequestOptions::JSON] = $data;
            }

            $response = $this->httpClient->request($method, $endpoint, $options);
            $body = $response->getBody()->getContents();
            
            $decoded = json_decode($body, true);
            if (json_last_error() !== JSON_ERROR_NONE) {
                throw new NodeMavenException('Invalid JSON response from API');
            }

            return $decoded;

        } catch (GuzzleException $e) {
            $statusCode = $e->hasResponse() ? $e->getResponse()->getStatusCode() : 0;
            $message = $e->getMessage();

            // Extract error message from response if available
            if ($e->hasResponse()) {
                $body = $e->getResponse()->getBody()->getContents();
                $decoded = json_decode($body, true);
                if (isset($decoded['error'])) {
                    $message = $decoded['error'];
                } elseif (isset($decoded['message'])) {
                    $message = $decoded['message'];
                }
            }

            // Throw specific exceptions based on status code
            switch ($statusCode) {
                case 401:
                case 403:
                    throw new AuthenticationException($message, $statusCode);
                case 429:
                    throw new RateLimitException($message, $statusCode);
                case 400:
                case 422:
                    throw new ValidationException($message, $statusCode);
                default:
                    throw new NodeMavenException($message, $statusCode);
            }
        }
    }

    /**
     * Get API key from environment
     * 
     * @return string API key
     */
    private function getApiKeyFromEnv(): string
    {
        return $_ENV['NODEMAVEN_APIKEY'] ?? getenv('NODEMAVEN_APIKEY') ?: '';
    }
} 