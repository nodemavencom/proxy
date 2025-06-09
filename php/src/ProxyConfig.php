<?php

declare(strict_types=1);

namespace NodeMaven;

use GuzzleHttp\Client as GuzzleClient;

/**
 * Proxy Configuration
 * 
 * Represents proxy configuration with helper methods for different HTTP clients
 */
class ProxyConfig
{
    private string $host;
    private int $httpPort;
    private int $socks5Port;
    private string $username;
    private string $password;
    private array $options;

    /**
     * Initialize proxy configuration
     * 
     * @param array $config Proxy configuration
     */
    public function __construct(array $config)
    {
        $this->host = $config['host'] ?? '';
        $this->httpPort = $config['http_port'] ?? 8080;
        $this->socks5Port = $config['socks5_port'] ?? 1080;
        $this->username = $config['username'] ?? '';
        $this->password = $config['password'] ?? '';
        $this->options = $config['options'] ?? [];
    }

    /**
     * Get proxy host
     * 
     * @return string
     */
    public function getHost(): string
    {
        return $this->host;
    }

    /**
     * Get HTTP port
     * 
     * @return int
     */
    public function getHttpPort(): int
    {
        return $this->httpPort;
    }

    /**
     * Get SOCKS5 port
     * 
     * @return int
     */
    public function getSocks5Port(): int
    {
        return $this->socks5Port;
    }

    /**
     * Get proxy username
     * 
     * @return string
     */
    public function getUsername(): string
    {
        return $this->username;
    }

    /**
     * Get proxy password
     * 
     * @return string
     */
    public function getPassword(): string
    {
        return $this->password;
    }

    /**
     * Get proxy options
     * 
     * @return array
     */
    public function getOptions(): array
    {
        return $this->options;
    }

    /**
     * Get HTTP proxy URL
     * 
     * @return string
     */
    public function getHttpUrl(): string
    {
        return sprintf(
            'http://%s:%s@%s:%d',
            urlencode($this->username),
            urlencode($this->password),
            $this->host,
            $this->httpPort
        );
    }

    /**
     * Get SOCKS5 proxy URL
     * 
     * @return string
     */
    public function getSocks5Url(): string
    {
        return sprintf(
            'socks5://%s:%s@%s:%d',
            urlencode($this->username),
            urlencode($this->password),
            $this->host,
            $this->socks5Port
        );
    }

    /**
     * Get proxy configuration for Guzzle HTTP client
     * 
     * @return array
     */
    public function getGuzzleConfig(): array
    {
        return [
            'proxy' => [
                'http' => $this->getHttpUrl(),
                'https' => $this->getHttpUrl(),
            ]
        ];
    }

    /**
     * Get proxy configuration as array
     * 
     * @return array
     */
    public function toArray(): array
    {
        return [
            'host' => $this->host,
            'http_port' => $this->httpPort,
            'socks5_port' => $this->socks5Port,
            'username' => $this->username,
            'password' => $this->password,
            'http_url' => $this->getHttpUrl(),
            'socks5_url' => $this->getSocks5Url(),
            'options' => $this->options
        ];
    }

    /**
     * Create HTTP client with this proxy configuration
     * 
     * @param array $config Additional Guzzle configuration
     * @return GuzzleClient
     */
    public function createHttpClient(array $config = []): GuzzleClient
    {
        $defaultConfig = [
            'timeout' => 30,
            'connect_timeout' => 10,
            'verify' => true,
        ];

        $proxyConfig = $this->getGuzzleConfig();
        $finalConfig = array_merge($defaultConfig, $config, $proxyConfig);

        return new GuzzleClient($finalConfig);
    }

    /**
     * Get cURL options for proxy
     * 
     * @return array
     */
    public function getCurlOptions(): array
    {
        return [
            CURLOPT_PROXY => $this->host,
            CURLOPT_PROXYPORT => $this->httpPort,
            CURLOPT_PROXYUSERPWD => $this->username . ':' . $this->password,
            CURLOPT_PROXYTYPE => CURLPROXY_HTTP,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_CONNECTTIMEOUT => 10,
        ];
    }

    /**
     * Create context for file_get_contents/stream_context_create
     * 
     * @return resource
     */
    public function getStreamContext()
    {
        $proxy = $this->getHttpUrl();
        
        $context = stream_context_create([
            'http' => [
                'proxy' => $proxy,
                'request_fulluri' => true,
                'timeout' => 30,
            ],
            'https' => [
                'proxy' => $proxy,
                'request_fulluri' => true,
                'timeout' => 30,
            ]
        ]);

        return $context;
    }

    /**
     * Test proxy connection
     * 
     * @param string $testUrl URL to test against
     * @return array Test result with IP and response data
     * @throws \Exception
     */
    public function testConnection(string $testUrl = 'https://httpbin.org/ip'): array
    {
        $client = $this->createHttpClient([
            'timeout' => 15,
            'connect_timeout' => 10,
        ]);

        try {
            $response = $client->get($testUrl);
            $body = $response->getBody()->getContents();
            $data = json_decode($body, true);

            return [
                'success' => true,
                'status_code' => $response->getStatusCode(),
                'ip' => $data['origin'] ?? 'unknown',
                'response' => $data,
                'proxy_used' => $this->getHttpUrl()
            ];

        } catch (\Exception $e) {
            return [
                'success' => false,
                'error' => $e->getMessage(),
                'proxy_used' => $this->getHttpUrl()
            ];
        }
    }
} 