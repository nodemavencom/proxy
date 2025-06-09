<?php

declare(strict_types=1);

namespace NodeMaven;

// Load environment variables if .env file exists
if (file_exists(__DIR__ . '/../.env')) {
    Utils::loadEnv(__DIR__ . '/../.env');
}

/**
 * NodeMaven SDK Main Class
 * 
 * Convenience class for quick access to NodeMaven functionality
 */
class NodeMaven
{
    private static ?Client $defaultClient = null;

    /**
     * Get or create default client instance
     * 
     * @param array $config Optional configuration for new client
     * @return Client
     */
    public static function client(array $config = []): Client
    {
        if (self::$defaultClient === null) {
            self::$defaultClient = new Client($config);
        }
        
        return self::$defaultClient;
    }

    /**
     * Set default client instance
     * 
     * @param Client $client
     */
    public static function setClient(Client $client): void
    {
        self::$defaultClient = $client;
    }

    /**
     * Quick proxy configuration
     * 
     * @param array $options Proxy options
     * @return ProxyConfig
     */
    public static function proxy(array $options = []): ProxyConfig
    {
        return self::client()->getProxyConfig($options);
    }

    /**
     * Quick user info
     * 
     * @return array
     */
    public static function userInfo(): array
    {
        return self::client()->getUserInfo();
    }

    /**
     * Quick countries list
     * 
     * @param array $options Query options
     * @return array
     */
    public static function countries(array $options = []): array
    {
        return self::client()->getCountries($options);
    }

    /**
     * Create HTTP client with proxy
     * 
     * @param array $proxyOptions Proxy configuration options
     * @param array $clientConfig HTTP client configuration
     * @return \GuzzleHttp\Client
     */
    public static function httpClient(array $proxyOptions = [], array $clientConfig = []): \GuzzleHttp\Client
    {
        $proxyConfig = self::proxy($proxyOptions);
        return $proxyConfig->createHttpClient($clientConfig);
    }

    /**
     * Generate session ID
     * 
     * @param int $length Session ID length
     * @return string
     */
    public static function sessionId(int $length = 8): string
    {
        return Utils::generateSessionId($length);
    }

    /**
     * Get current IP address
     * 
     * @param array $proxyOptions Optional proxy configuration for the request
     * @return string|null
     */
    public static function currentIp(array $proxyOptions = []): ?string
    {
        return Utils::getCurrentIp($proxyOptions);
    }

    /**
     * Format bytes to human readable format
     * 
     * @param int $bytes
     * @param int $precision
     * @return string
     */
    public static function formatBytes(int $bytes, int $precision = 2): string
    {
        return Utils::formatBytes($bytes, $precision);
    }

    /**
     * Check system requirements
     * 
     * @return array Missing extensions
     */
    public static function checkRequirements(): array
    {
        return Utils::checkRequiredExtensions();
    }

    /**
     * Get system information
     * 
     * @return array
     */
    public static function systemInfo(): array
    {
        return Utils::getSystemInfo();
    }
} 