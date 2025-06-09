<?php

/**
 * NodeMaven PHP SDK - Advanced Proxy Integration Example
 * 
 * This example demonstrates advanced proxy usage patterns including:
 * - Session management and rotation
 * - Concurrent requests
 * - Error handling and retries
 * - Different HTTP client integrations
 */

declare(strict_types=1);

require_once __DIR__ . '/../vendor/autoload.php';

use NodeMaven\Client;
use NodeMaven\Utils;
use NodeMaven\Exceptions\NodeMavenException;
use GuzzleHttp\Client as GuzzleClient;
use GuzzleHttp\Promise;
use GuzzleHttp\Exception\RequestException;

// Load environment variables
Utils::loadEnv(__DIR__ . '/../.env');

echo "🔧 NodeMaven PHP SDK - Advanced Proxy Integration\n";
echo str_repeat("=", 70) . "\n\n";

try {
    $client = new Client();
    
    // 1. Session Management
    echo "1️⃣  Session Management and Sticky IPs\n";
    echo str_repeat("-", 50) . "\n";
    
    $sessionId = 'user_session_' . Utils::generateSessionId();
    echo "Creating sticky session: {$sessionId}\n";
    
    $sessionProxy = $client->getProxyConfig([
        'country' => 'US',
        'session' => $sessionId
    ]);
    
    // Make multiple requests with the same session (same IP)
    echo "Making 3 requests with sticky session...\n";
    for ($i = 1; $i <= 3; $i++) {
        $result = $sessionProxy->testConnection('https://httpbin.org/ip');
        if ($result['success']) {
            echo "   Request {$i}: IP = {$result['ip']}\n";
        } else {
            echo "   Request {$i}: Failed\n";
        }
        sleep(1); // Small delay between requests
    }
    echo "\n";

    // 2. Proxy Rotation
    echo "2️⃣  Proxy Rotation (Different Sessions)\n";
    echo str_repeat("-", 50) . "\n";
    
    $countries = ['US', 'UK', 'CA', 'DE'];
    echo "Testing different countries with unique sessions...\n";
    
    foreach ($countries as $country) {
        $uniqueSession = "session_{$country}_" . Utils::generateSessionId();
        $proxy = $client->getProxyConfig([
            'country' => $country,
            'session' => $uniqueSession
        ]);
        
        $result = $proxy->testConnection('https://httpbin.org/ip');
        if ($result['success']) {
            echo "   {$country}: IP = {$result['ip']}\n";
        } else {
            echo "   {$country}: Connection failed\n";
        }
    }
    echo "\n";

    // 3. Concurrent Requests
    echo "3️⃣  Concurrent Requests with Different Proxies\n";
    echo str_repeat("-", 50) . "\n";
    
    $promises = [];
    $proxyConfigs = [];
    
    // Create multiple proxy configurations
    for ($i = 0; $i < 5; $i++) {
        $sessionId = "concurrent_" . $i . "_" . Utils::generateSessionId();
        $proxyConfig = $client->getProxyConfig([
            'country' => 'US',
            'session' => $sessionId
        ]);
        $proxyConfigs[$i] = $proxyConfig;
        
        // Create HTTP client for this proxy
        $httpClient = $proxyConfig->createHttpClient(['timeout' => 15]);
        
        // Create async promise
        $promises[$i] = $httpClient->getAsync('https://httpbin.org/ip');
    }
    
    echo "Executing 5 concurrent requests...\n";
    $responses = Promise\settle($promises)->wait();
    
    foreach ($responses as $index => $response) {
        if ($response['state'] === 'fulfilled') {
            $body = $response['value']->getBody()->getContents();
            $data = json_decode($body, true);
            $ip = $data['origin'] ?? 'unknown';
            echo "   Request {$index}: IP = {$ip}\n";
        } else {
            echo "   Request {$index}: Failed\n";
        }
    }
    echo "\n";

    // 4. Error Handling and Retries
    echo "4️⃣  Error Handling and Retry Logic\n";
    echo str_repeat("-", 50) . "\n";
    
    $retryProxy = $client->getProxyConfig(['country' => 'US']);
    
    echo "Testing retry mechanism with potential failures...\n";
    
    $retryResult = Utils::retry(function() use ($retryProxy) {
        // Simulate some requests that might fail
        $result = $retryProxy->testConnection('https://httpbin.org/delay/1');
        
        if (!$result['success']) {
            throw new Exception("Request failed: " . $result['error']);
        }
        
        return $result;
    }, 3, 1);
    
    echo "   Retry completed successfully: IP = {$retryResult['ip']}\n\n";

    // 5. Different Integration Methods
    echo "5️⃣  Different HTTP Client Integration Methods\n";
    echo str_repeat("-", 50) . "\n";
    
    $integrationProxy = $client->getProxyConfig(['country' => 'US']);
    
    // Method 1: Using Guzzle with proxy configuration
    echo "Method 1: Guzzle with proxy config...\n";
    $guzzleConfig = $integrationProxy->getGuzzleConfig();
    $guzzleClient = new GuzzleClient(array_merge($guzzleConfig, ['timeout' => 10]));
    
    try {
        $response = $guzzleClient->get('https://httpbin.org/ip');
        $data = json_decode($response->getBody()->getContents(), true);
        echo "   ✅ Guzzle: IP = " . ($data['origin'] ?? 'unknown') . "\n";
    } catch (Exception $e) {
        echo "   ❌ Guzzle failed: " . $e->getMessage() . "\n";
    }
    
    // Method 2: Using cURL directly
    echo "Method 2: Direct cURL usage...\n";
    $curlOptions = $integrationProxy->getCurlOptions();
    
    $ch = curl_init();
    curl_setopt_array($ch, array_merge($curlOptions, [
        CURLOPT_URL => 'https://httpbin.org/ip',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json']
    ]));
    
    $curlResponse = curl_exec($ch);
    $curlError = curl_error($ch);
    curl_close($ch);
    
    if ($curlResponse && !$curlError) {
        $data = json_decode($curlResponse, true);
        echo "   ✅ cURL: IP = " . ($data['origin'] ?? 'unknown') . "\n";
    } else {
        echo "   ❌ cURL failed: {$curlError}\n";
    }
    
    // Method 3: Using stream context (file_get_contents)
    echo "Method 3: Stream context (file_get_contents)...\n";
    $streamContext = $integrationProxy->getStreamContext();
    
    try {
        $streamResponse = file_get_contents('https://httpbin.org/ip', false, $streamContext);
        if ($streamResponse) {
            $data = json_decode($streamResponse, true);
            echo "   ✅ Stream: IP = " . ($data['origin'] ?? 'unknown') . "\n";
        } else {
            echo "   ❌ Stream failed\n";
        }
    } catch (Exception $e) {
        echo "   ❌ Stream failed: " . $e->getMessage() . "\n";
    }
    echo "\n";

    // 6. Geo-targeting Examples
    echo "6️⃣  Advanced Geo-targeting\n";
    echo str_repeat("-", 50) . "\n";
    
    // Target specific cities
    $cityTargets = [
        ['country' => 'US', 'city' => 'New York'],
        ['country' => 'US', 'city' => 'Los Angeles'],
        ['country' => 'UK', 'city' => 'London'],
        ['country' => 'CA', 'city' => 'Toronto'],
    ];
    
    echo "Testing city-level targeting...\n";
    foreach ($cityTargets as $target) {
        $cityProxy = $client->getProxyConfig($target);
        echo "   {$target['country']} - {$target['city']}: ";
        echo "Username = " . $cityProxy->getUsername() . "\n";
    }
    echo "\n";

    // 7. Performance Testing
    echo "7️⃣  Performance Testing\n";
    echo str_repeat("-", 50) . "\n";
    
    $perfProxy = $client->getProxyConfig(['country' => 'US']);
    $perfClient = $perfProxy->createHttpClient(['timeout' => 5]);
    
    echo "Testing response times for 5 requests...\n";
    $times = [];
    
    for ($i = 0; $i < 5; $i++) {
        $start = microtime(true);
        try {
            $response = $perfClient->get('https://httpbin.org/ip');
            $end = microtime(true);
            $time = round(($end - $start) * 1000, 2);
            $times[] = $time;
            echo "   Request " . ($i + 1) . ": {$time}ms\n";
        } catch (Exception $e) {
            echo "   Request " . ($i + 1) . ": Failed\n";
        }
    }
    
    if (!empty($times)) {
        $avgTime = round(array_sum($times) / count($times), 2);
        echo "   Average response time: {$avgTime}ms\n";
    }
    echo "\n";

    echo str_repeat("=", 70) . "\n";
    echo "🎉 Advanced proxy integration example completed!\n\n";
    
    echo "📋 Summary of Integration Methods:\n";
    echo "   ✅ Session management for sticky IPs\n";
    echo "   ✅ Proxy rotation across countries\n";
    echo "   ✅ Concurrent requests with different proxies\n";
    echo "   ✅ Error handling and retry mechanisms\n";
    echo "   ✅ Multiple HTTP client integrations\n";
    echo "   ✅ Advanced geo-targeting options\n";
    echo "   ✅ Performance monitoring\n\n";
    
    echo "🔗 Resources:\n";
    echo "   • API Documentation: https://dashboard.nodemaven.com/documentation\n";
    echo "   • Support: https://dashboard.nodemaven.com\n";
    echo "   • GitHub: https://github.com/nodemavencom/proxy\n";

} catch (NodeMavenException $e) {
    echo "❌ NodeMaven Error: " . $e->getMessage() . "\n";
    echo "💡 Status Code: " . $e->getStatusCode() . "\n";
    
} catch (Exception $e) {
    echo "❌ Unexpected Error: " . $e->getMessage() . "\n";
    echo "💡 Stack trace: " . $e->getTraceAsString() . "\n";
} 