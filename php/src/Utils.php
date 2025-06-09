<?php

declare(strict_types=1);

namespace NodeMaven;

/**
 * Utility functions for NodeMaven SDK
 */
class Utils
{
    /**
     * Format proxy username with targeting options
     * 
     * @param string $baseUsername Base proxy username
     * @param array $options Targeting options
     * @return string Formatted username
     */
    public static function formatProxyUsername(string $baseUsername, array $options = []): string
    {
        $parts = [$baseUsername];

        // Add country targeting
        if (!empty($options['country'])) {
            $parts[] = 'country-' . strtolower($options['country']);
        }

        // Add region targeting
        if (!empty($options['region'])) {
            $parts[] = 'region-' . strtolower(str_replace(' ', '_', $options['region']));
        }

        // Add city targeting
        if (!empty($options['city'])) {
            $parts[] = 'city-' . strtolower(str_replace(' ', '_', $options['city']));
        }

        // Add ISP targeting
        if (!empty($options['isp'])) {
            $parts[] = 'isp-' . strtolower(str_replace(' ', '_', $options['isp']));
        }

        // Add session for sticky IP
        if (!empty($options['session'])) {
            $parts[] = 'session-' . $options['session'];
        }

        return implode('-', $parts);
    }

    /**
     * Generate random session ID
     * 
     * @param int $length Session ID length
     * @return string Random session ID
     */
    public static function generateSessionId(int $length = 8): string
    {
        $characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
        $sessionId = '';
        
        for ($i = 0; $i < $length; $i++) {
            $sessionId .= $characters[random_int(0, strlen($characters) - 1)];
        }
        
        return $sessionId;
    }

    /**
     * Format bytes to human readable format
     * 
     * @param int $bytes Number of bytes
     * @param int $precision Decimal precision
     * @return string Formatted bytes string
     */
    public static function formatBytes(int $bytes, int $precision = 2): string
    {
        $units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB'];
        
        for ($i = 0; $bytes > 1024 && $i < count($units) - 1; $i++) {
            $bytes /= 1024;
        }
        
        return round($bytes, $precision) . ' ' . $units[$i];
    }

    /**
     * Get current IP address using an external service
     * 
     * @param array $proxyOptions Proxy configuration for the request
     * @param int $timeout Request timeout
     * @return string|null Current IP address or null on error
     */
    public static function getCurrentIp(array $proxyOptions = [], int $timeout = 10): ?string
    {
        $services = [
            'https://httpbin.org/ip',
            'https://ipinfo.io/ip',
            'https://api.ipify.org',
            'https://checkip.amazonaws.com'
        ];

        foreach ($services as $service) {
            try {
                $context = null;
                
                // Create stream context with proxy if provided
                if (!empty($proxyOptions)) {
                    $context = stream_context_create([
                        'http' => array_merge([
                            'timeout' => $timeout,
                            'method' => 'GET',
                        ], $proxyOptions)
                    ]);
                } else {
                    $context = stream_context_create([
                        'http' => [
                            'timeout' => $timeout,
                            'method' => 'GET',
                        ]
                    ]);
                }

                $response = file_get_contents($service, false, $context);
                
                if ($response === false) {
                    continue;
                }

                // Parse response based on service
                if (strpos($service, 'httpbin.org') !== false) {
                    $data = json_decode($response, true);
                    return $data['origin'] ?? null;
                } elseif (strpos($service, 'ipinfo.io') !== false || 
                         strpos($service, 'ipify.org') !== false ||
                         strpos($service, 'amazonaws.com') !== false) {
                    return trim($response);
                }

            } catch (\Exception $e) {
                // Continue to next service
                continue;
            }
        }

        return null;
    }

    /**
     * Validate proxy options
     * 
     * @param array $options Proxy options to validate
     * @return array Validation result
     */
    public static function validateProxyOptions(array $options): array
    {
        $errors = [];
        $warnings = [];

        // Validate country code
        if (isset($options['country'])) {
            if (!is_string($options['country']) || strlen($options['country']) !== 2) {
                $errors[] = 'Country must be a 2-character ISO country code (e.g., "US", "UK")';
            }
        }

        // Validate session ID
        if (isset($options['session'])) {
            if (!is_string($options['session']) || empty($options['session'])) {
                $errors[] = 'Session must be a non-empty string';
            } elseif (strlen($options['session']) > 50) {
                $warnings[] = 'Session ID is quite long, consider using shorter IDs for better performance';
            }
        }

        // Validate string fields
        $stringFields = ['region', 'city', 'isp'];
        foreach ($stringFields as $field) {
            if (isset($options[$field]) && !is_string($options[$field])) {
                $errors[] = ucfirst($field) . ' must be a string';
            }
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors,
            'warnings' => $warnings
        ];
    }

    /**
     * Load environment variables from .env file
     * 
     * @param string $path Path to .env file
     * @return bool Success status
     */
    public static function loadEnv(string $path = '.env'): bool
    {
        if (!file_exists($path)) {
            return false;
        }

        try {
            $dotenv = \Dotenv\Dotenv::createImmutable(dirname($path), basename($path));
            $dotenv->load();
            return true;
        } catch (\Exception $e) {
            return false;
        }
    }

    /**
     * Check if required extensions are loaded
     * 
     * @return array Missing extensions
     */
    public static function checkRequiredExtensions(): array
    {
        $required = ['curl', 'json', 'openssl'];
        $missing = [];

        foreach ($required as $extension) {
            if (!extension_loaded($extension)) {
                $missing[] = $extension;
            }
        }

        return $missing;
    }

    /**
     * Get system information for debugging
     * 
     * @return array System information
     */
    public static function getSystemInfo(): array
    {
        return [
            'php_version' => PHP_VERSION,
            'os' => PHP_OS,
            'sapi' => PHP_SAPI,
            'extensions' => [
                'curl' => extension_loaded('curl'),
                'json' => extension_loaded('json'),
                'openssl' => extension_loaded('openssl'),
            ],
            'memory_limit' => ini_get('memory_limit'),
            'max_execution_time' => ini_get('max_execution_time'),
        ];
    }

    /**
     * Sanitize string for use in proxy username
     * 
     * @param string $input Input string
     * @return string Sanitized string
     */
    public static function sanitizeForProxyUsername(string $input): string
    {
        // Convert to lowercase
        $sanitized = strtolower($input);
        
        // Replace spaces and special characters with underscores
        $sanitized = preg_replace('/[^a-z0-9_-]/', '_', $sanitized);
        
        // Remove multiple consecutive underscores
        $sanitized = preg_replace('/_+/', '_', $sanitized);
        
        // Trim underscores from start and end
        $sanitized = trim($sanitized, '_');
        
        return $sanitized;
    }

    /**
     * Create retry mechanism for API calls
     * 
     * @param callable $callback Function to retry
     * @param int $maxRetries Maximum number of retries
     * @param int $delay Delay between retries in seconds
     * @return mixed Result of the callback
     * @throws \Exception Last exception if all retries fail
     */
    public static function retry(callable $callback, int $maxRetries = 3, int $delay = 1)
    {
        $lastException = null;
        
        for ($attempt = 0; $attempt <= $maxRetries; $attempt++) {
            try {
                return $callback();
            } catch (\Exception $e) {
                $lastException = $e;
                
                if ($attempt < $maxRetries) {
                    sleep($delay);
                    $delay *= 2; // Exponential backoff
                }
            }
        }
        
        throw $lastException;
    }
} 