<?php

/**
 * NodeMaven PHP SDK - Basic Usage Example
 * 
 * This example demonstrates the core functionality of the NodeMaven PHP SDK
 */

declare(strict_types=1);

require_once __DIR__ . '/../vendor/autoload.php';

use NodeMaven\Client;
use NodeMaven\Utils;
use NodeMaven\Exceptions\NodeMavenException;

// Load environment variables
Utils::loadEnv(__DIR__ . '/../.env');

echo "🚀 NodeMaven PHP SDK - Basic Usage Example\n";
echo str_repeat("=", 60) . "\n\n";

try {
    // Initialize the client
    echo "1️⃣  Initializing NodeMaven client...\n";
    $client = new Client();
    echo "✅ Client initialized successfully!\n\n";

    // Get user information
    echo "2️⃣  Getting user information...\n";
    $userInfo = $client->getUserInfo();
    
    echo "✅ User Information:\n";
    echo "   Username: " . ($userInfo['username'] ?? $userInfo['email'] ?? 'N/A') . "\n";
    echo "   Proxy Username: " . ($userInfo['proxy_username'] ?? 'N/A') . "\n";
    
    if (isset($userInfo['traffic_used'], $userInfo['traffic_limit'])) {
        echo "   Traffic Used: " . Utils::formatBytes($userInfo['traffic_used']) . "\n";
        echo "   Traffic Limit: " . Utils::formatBytes($userInfo['traffic_limit']) . "\n";
        $remaining = max(0, $userInfo['traffic_limit'] - $userInfo['traffic_used']);
        echo "   Remaining: " . Utils::formatBytes($remaining) . "\n";
    }
    echo "\n";

    // Get available countries
    echo "3️⃣  Getting available countries...\n";
    $countries = $client->getCountries(['limit' => 10]);
    
    echo "✅ Available Countries (first 10):\n";
    foreach ($countries['results'] ?? [] as $index => $country) {
        echo "   " . ($index + 1) . ". {$country['name']} ({$country['code']})\n";
    }
    echo "\n";

    // Basic proxy configuration
    echo "4️⃣  Creating basic proxy configuration...\n";
    $proxyConfig = $client->getProxyConfig();
    
    echo "✅ Basic Proxy Configuration:\n";
    echo "   Host: " . $proxyConfig->getHost() . "\n";
    echo "   HTTP Port: " . $proxyConfig->getHttpPort() . "\n";
    echo "   SOCKS5 Port: " . $proxyConfig->getSocks5Port() . "\n";
    echo "   Username: " . $proxyConfig->getUsername() . "\n";
    echo "   HTTP URL: " . $proxyConfig->getHttpUrl() . "\n";
    echo "\n";

    // Geo-targeted proxy configuration
    echo "5️⃣  Creating geo-targeted proxy (US)...\n";
    $usProxyConfig = $client->getProxyConfig(['country' => 'US']);
    
    echo "✅ US Proxy Configuration:\n";
    echo "   Username: " . $usProxyConfig->getUsername() . "\n";
    echo "   SOCKS5 URL: " . $usProxyConfig->getSocks5Url() . "\n";
    echo "\n";

    // Sticky session example
    echo "6️⃣  Creating sticky session proxy...\n";
    $sessionId = 'my_session_' . Utils::generateSessionId();
    $stickyProxyConfig = $client->getProxyConfig([
        'country' => 'US',
        'session' => $sessionId
    ]);
    
    echo "✅ Sticky Session Proxy:\n";
    echo "   Session ID: {$sessionId}\n";
    echo "   Username: " . $stickyProxyConfig->getUsername() . "\n";
    echo "\n";

    // Test proxy connection
    echo "7️⃣  Testing proxy connection...\n";
    $testResult = $usProxyConfig->testConnection('https://httpbin.org/ip');
    
    if ($testResult['success']) {
        echo "✅ Proxy Connection Test:\n";
        echo "   Status: Success\n";
        echo "   IP Address: " . $testResult['ip'] . "\n";
        echo "   Status Code: " . $testResult['status_code'] . "\n";
    } else {
        echo "❌ Proxy Connection Test Failed:\n";
        echo "   Error: " . $testResult['error'] . "\n";
    }
    echo "\n";

    // Using proxy with Guzzle
    echo "8️⃣  Making HTTP request through proxy...\n";
    $httpClient = $usProxyConfig->createHttpClient();
    
    try {
        $response = $httpClient->get('https://httpbin.org/json');
        $data = json_decode($response->getBody()->getContents(), true);
        
        echo "✅ HTTP Request through Proxy:\n";
        echo "   Status Code: " . $response->getStatusCode() . "\n";
        echo "   Response contains slideshow: " . (isset($data['slideshow']) ? 'Yes' : 'No') . "\n";
    } catch (Exception $e) {
        echo "❌ HTTP Request Failed: " . $e->getMessage() . "\n";
    }
    echo "\n";

    // Multiple proxy configurations
    echo "9️⃣  Creating multiple proxy configurations...\n";
    $countries = ['US', 'UK', 'CA', 'AU', 'DE'];
    
    foreach ($countries as $country) {
        $proxy = $client->getProxyConfig(['country' => $country]);
        echo "   {$country}: " . $proxy->getHost() . ":" . $proxy->getHttpPort() . "\n";
    }
    echo "\n";

    echo str_repeat("=", 60) . "\n";
    echo "🎉 Basic usage example completed successfully!\n\n";
    
    echo "📖 Key Takeaways:\n";
    echo "   • Use Client() to initialize the NodeMaven client\n";
    echo "   • Call getProxyConfig() with targeting options\n";
    echo "   • Use session IDs for sticky sessions\n";
    echo "   • ProxyConfig provides multiple integration methods\n";
    echo "   • Always test your proxy configurations\n\n";
    
    echo "🔗 Next Steps:\n";
    echo "   • Check proxy_integration.php for advanced usage\n";
    echo "   • Visit https://dashboard.nodemaven.com for account management\n";
    echo "   • Read the API documentation for more options\n";

} catch (NodeMavenException $e) {
    echo "❌ NodeMaven Error: " . $e->getMessage() . "\n";
    echo "💡 Status Code: " . $e->getStatusCode() . "\n";
    
    if ($e->getStatusCode() === 401 || $e->getStatusCode() === 403) {
        echo "💡 Check your API key in .env file or environment variables\n";
    }
    
} catch (Exception $e) {
    echo "❌ Unexpected Error: " . $e->getMessage() . "\n";
    echo "💡 Please check your configuration and try again\n";
} 