<?php
#!/usr/bin/env php
<?php

/**
 * NodeMaven PHP SDK - Quick Test
 * 
 * This script quickly validates that the NodeMaven PHP SDK is working correctly.
 * Similar to the Python quick_test.py and JavaScript quick_test.js functionality.
 */

declare(strict_types=1);

// Autoload composer dependencies
if (file_exists(__DIR__ . '/vendor/autoload.php')) {
    require_once __DIR__ . '/vendor/autoload.php';
} else {
    echo "❌ Composer autoload not found. Run 'composer install' first.\n";
    exit(1);
}

use NodeMaven\Client;
use NodeMaven\Utils;
use NodeMaven\Exceptions\AuthenticationException;
use NodeMaven\Exceptions\NodeMavenException;

/**
 * Test proxy connection
 */
function testProxyConnection(string $description, \NodeMaven\ProxyConfig $proxyConfig): bool
{
    echo "   Testing {$description}... ";
    
    try {
        $result = $proxyConfig->testConnection();
        
        if ($result['success']) {
            echo "✅ Success! IP: " . $result['ip'] . "\n";
            return true;
        } else {
            echo "❌ Failed: " . $result['error'] . "\n";
            return false;
        }
        
    } catch (Exception $e) {
        echo "❌ Error: " . substr($e->getMessage(), 0, 50) . "...\n";
        return false;
    }
}

/**
 * Check environment and system requirements
 */
function checkEnvironment(): bool
{
    echo "🔧 Environment Check\n";
    echo str_repeat("=", 50) . "\n";
    
    // Check PHP version
    echo "PHP Version: " . PHP_VERSION;
    if (version_compare(PHP_VERSION, '8.0.0', '>=')) {
        echo " ✅\n";
    } else {
        echo " ❌ (PHP 8.0+ required)\n";
        return false;
    }
    
    // Check required extensions
    $missing = Utils::checkRequiredExtensions();
    if (empty($missing)) {
        echo "Required Extensions: ✅ All present\n";
    } else {
        echo "Required Extensions: ❌ Missing: " . implode(', ', $missing) . "\n";
        return false;
    }
    
    // Load environment variables
    if (Utils::loadEnv(__DIR__ . '/.env')) {
        echo "Environment File: ✅ Loaded .env\n";
    } else {
        echo "Environment File: ⚠️  .env not found (you can set variables manually)\n";
    }
    
    // Check API key
    if (!empty($_ENV['NODEMAVEN_APIKEY'] ?? getenv('NODEMAVEN_APIKEY'))) {
        echo "API Key: ✅ Found\n";
    } else {
        echo "API Key: ❌ NODEMAVEN_APIKEY not set\n";
        echo "💡 Set your API key: export NODEMAVEN_APIKEY=\"your-key-here\"\n";
        echo "   Or create .env file with: NODEMAVEN_APIKEY=your-key-here\n";
        return false;
    }
    
    echo "\n";
    return true;
}

/**
 * Test basic SDK functionality
 */
function testBasicFunctionality(): bool
{
    echo "🧪 NodeMaven PHP SDK - Quick Test\n";
    echo str_repeat("=", 50) . "\n";
    
    try {
        // Test 1: Client initialization
        echo "1️⃣  Testing client initialization... ";
        $client = new Client();
        echo "✅ Success\n";
        
        // Test 2: API connectivity
        echo "2️⃣  Testing API connectivity... ";
        $userInfo = $client->getUserInfo();
        echo "✅ Success\n";
        
        $username = $userInfo['username'] ?? $userInfo['email'] ?? 'Unknown';
        $proxyUsername = $userInfo['proxy_username'] ?? '';
        
        echo "   User: {$username}\n";
        echo "   Proxy Username: {$proxyUsername}\n";
        
        // Test 3: Location data retrieval
        echo "\n3️⃣  Testing location data retrieval... ";
        $countries = $client->getCountries(['limit' => 5]);
        echo "✅ Success\n";
        echo "   Retrieved " . count($countries['results'] ?? []) . " countries:\n";
        
        foreach (($countries['results'] ?? []) as $index => $country) {
            echo "     " . ($index + 1) . ". {$country['name']} ({$country['code']})\n";
        }
        
        // Test 4: Proxy configuration generation
        echo "\n4️⃣  Testing proxy configuration generation... ";
        $proxyConfig = $client->getProxyConfig(['country' => 'US']);
        echo "✅ Success\n";
        echo "   Host: " . $proxyConfig->getHost() . "\n";
        echo "   HTTP Port: " . $proxyConfig->getHttpPort() . "\n";
        echo "   Username: " . $proxyConfig->getUsername() . "\n";
        
        // Test 5: SOCKS5 URL generation
        echo "\n5️⃣  Testing SOCKS5 URL generation... ";
        $socks5Url = $client->getSocks5ProxyUrl(['country' => 'UK']);
        echo "✅ Success\n";
        echo "   URL: " . substr($socks5Url, 0, 50) . "...\n";
        
        // Test 6: Proxy connection test
        echo "\n6️⃣  Testing proxy connections...\n";
        $usProxy = $client->getProxyConfig(['country' => 'US']);
        $usSuccess = testProxyConnection("US Proxy", $usProxy);
        
        if ($usSuccess) {
            $ukProxy = $client->getProxyConfig(['country' => 'GB']);
            testProxyConnection("UK Proxy", $ukProxy);
        }
        
        // Display account information
        echo "\n📊 Account Information:\n";
        
        $trafficUsed = $userInfo['traffic_used'] ?? 0;
        $trafficLimit = $userInfo['traffic_limit'] ?? 0;
        
        if ($trafficUsed && $trafficLimit) {
            echo "   Traffic Used: " . Utils::formatBytes($trafficUsed) . "\n";
            echo "   Traffic Limit: " . Utils::formatBytes($trafficLimit) . "\n";
            $remaining = max(0, $trafficLimit - $trafficUsed);
            echo "   Remaining: " . Utils::formatBytes($remaining) . "\n";
        }
        
        echo "\n" . str_repeat("=", 50) . "\n";
        echo "🎉 All tests passed! NodeMaven PHP SDK is working correctly.\n";
        return true;
        
    } catch (AuthenticationException $e) {
        echo "\n❌ Authentication Error: " . $e->getMessage() . "\n";
        echo "💡 Your API key may be invalid or expired\n";
        return false;
        
    } catch (NodeMavenException $e) {
        echo "\n❌ NodeMaven Error: " . $e->getMessage() . "\n";
        
        if ($e->getStatusCode() >= 400 && $e->getStatusCode() < 500) {
            echo "💡 Check your API key and account status\n";
        }
        return false;
        
    } catch (Exception $e) {
        echo "\n❌ Unexpected Error: " . $e->getMessage() . "\n";
        return false;
    }
}

/**
 * Show usage information
 */
function showUsage(): void
{
    echo "NodeMaven PHP SDK - Quick Test\n\n";
    echo "Usage:\n";
    echo "  php quick_test.php\n\n";
    echo "Environment Variables:\n";
    echo "  NODEMAVEN_APIKEY    Your NodeMaven API key (required)\n";
    echo "  NODEMAVEN_BASE_URL  API base URL (optional)\n\n";
    echo "Get your API key at: https://dashboard.nodemaven.com\n";
}

/**
 * Main function
 */
function main(): void
{
    // Show usage if --help is provided
    if (in_array('--help', $argv ?? []) || in_array('-h', $argv ?? [])) {
        showUsage();
        exit(0);
    }
    
    // Check environment
    if (!checkEnvironment()) {
        echo "❌ Environment check failed. Please fix the issues above.\n";
        exit(1);
    }
    
    // Test functionality
    if (!testBasicFunctionality()) {
        echo "\n❌ Quick test failed. Please check your configuration.\n";
        exit(1);
    }
    
    echo "\n✅ Quick test completed successfully!\n";
    echo "\n📖 Next steps:\n";
    echo "   - Check out examples: php examples/basic_usage.php\n";
    echo "   - Read the documentation in README.md\n";
    echo "   - Visit: https://dashboard.nodemaven.com\n";
}

// Run the quick test if this file is executed directly
if (realpath($argv[0] ?? '') === realpath(__FILE__)) {
    main();
} 