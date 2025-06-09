#!/usr/bin/env node

/**
 * NodeMaven JavaScript SDK - Basic Usage Example
 * 
 * This example demonstrates basic functionality of the NodeMaven JavaScript SDK:
 * - Client initialization
 * - Getting user information
 * - Retrieving location data (countries, regions, cities)
 * - Getting proxy configurations
 * - Error handling
 */

const { NodeMavenClient } = require('../src');

async function basicUsageExample() {
  try {
    console.log('🚀 NodeMaven JavaScript SDK - Basic Usage Example\n');

    // Initialize client (API key from environment variable NODEMAVEN_APIKEY)
    const client = new NodeMavenClient();
    console.log('✅ NodeMaven client initialized successfully');

    // Get user information
    console.log('\n📊 Getting user information...');
    const userInfo = await client.getUserInfo();
    console.log(`Username: ${userInfo.username}`);
    console.log(`Proxy Username: ${userInfo.proxy_username}`);
    console.log(`Traffic Used: ${userInfo.traffic_used} MB`);
    console.log(`Traffic Limit: ${userInfo.traffic_limit} MB`);

    // Get available countries (first 10)
    console.log('\n🌍 Getting available countries...');
    const countries = await client.getCountries({ limit: 10 });
    console.log(`Found ${countries.count} total countries. Showing first ${countries.results.length}:`);
    countries.results.forEach(country => {
      console.log(`  - ${country.name} (${country.code})`);
    });

    // Get regions for the first country
    if (countries.results.length > 0) {
      const firstCountry = countries.results[0];
      console.log(`\n🏘️  Getting regions for ${firstCountry.name}...`);
      const regions = await client.getRegions({ 
        countryCode: firstCountry.code, 
        limit: 5 
      });
      console.log(`Found ${regions.count} regions. Showing first ${regions.results.length}:`);
      regions.results.forEach(region => {
        console.log(`  - ${region.name} (${region.code})`);
      });

      // Get cities for the first region
      if (regions.results.length > 0) {
        const firstRegion = regions.results[0];
        console.log(`\n🏙️  Getting cities for ${firstRegion.name}...`);
        const cities = await client.getCities({
          countryCode: firstCountry.code,
          regionCode: firstRegion.code,
          limit: 5
        });
        console.log(`Found ${cities.count} cities. Showing first ${cities.results.length}:`);
        cities.results.forEach(city => {
          console.log(`  - ${city.name} (${city.code})`);
        });
      }
    }

    // Get proxy configuration
    console.log('\n🔧 Generating proxy configuration...');
    const proxyConfig = await client.getProxyConfig({
      country: 'US',
      city: 'new_york'
    });
    console.log('Proxy Configuration:');
    console.log(`  Host: ${proxyConfig.host}`);
    console.log(`  HTTP Port: ${proxyConfig.http_port}`);
    console.log(`  SOCKS5 Port: ${proxyConfig.socks5_port}`);
    console.log(`  Username: ${proxyConfig.username}`);
    console.log(`  Password: ${proxyConfig.password.substring(0, 8)}...`);

    // Get SOCKS5 proxy URL
    console.log('\n🔗 Generating SOCKS5 proxy URL...');
    const socks5Url = await client.getSocks5ProxyUrl({
      country: 'UK',
      city: 'london'
    });
    console.log(`SOCKS5 URL: ${socks5Url.substring(0, 50)}...`);

    // Get traffic statistics
    console.log('\n📈 Getting traffic statistics...');
    const statistics = await client.getStatistics({
      groupBy: 'day'
    });
    if (statistics.results && statistics.results.length > 0) {
      console.log(`Found ${statistics.results.length} statistics entries:`);
      statistics.results.slice(0, 3).forEach(stat => {
        console.log(`  - ${stat.date}: ${stat.traffic_used} MB`);
      });
    } else {
      console.log('No statistics data available');
    }

    console.log('\n✅ Basic usage example completed successfully!');

  } catch (error) {
    console.error('\n❌ Error occurred:');
    console.error(`Type: ${error.constructor.name}`);
    console.error(`Message: ${error.message}`);
    
    if (error.statusCode) {
      console.error(`Status Code: ${error.statusCode}`);
    }
    
    if (error.response) {
      console.error('Response Data:', JSON.stringify(error.response, null, 2));
    }
    
    process.exit(1);
  }
}

// Usage examples with different configurations
async function configurationExamples() {
  console.log('\n🔧 Configuration Examples:');
  
  // Example 1: Manual API key
  try {
    const client1 = new NodeMavenClient({
      apiKey: 'your-api-key-here'
    });
    console.log('✅ Client with manual API key');
  } catch (error) {
    console.log('⚠️  Manual API key example (expected to fail)');
  }
  
  // Example 2: Custom configuration
  const client2 = new NodeMavenClient({
    // apiKey: 'your-api-key',  // Can be set here or via environment
    baseUrl: 'https://dashboard.nodemaven.com',
    proxyHost: 'gate.nodemaven.com',
    httpPort: 8080,
    socks5Port: 1080,
    timeout: 30000
  });
  console.log('✅ Client with custom configuration');
}

async function main() {
  await basicUsageExample();
  await configurationExamples();
}

// Run the example if this file is executed directly
if (require.main === module) {
  main().catch(error => {
    console.error('❌ Example failed:', error.message);
    process.exit(1);
  });
}

module.exports = {
  basicUsageExample,
  configurationExamples
}; 