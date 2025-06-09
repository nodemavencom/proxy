#!/usr/bin/env node

/**
 * NodeMaven JavaScript SDK - Proxy Integration Example
 * 
 * This example demonstrates how to integrate NodeMaven proxies with HTTP requests:
 * - Using proxies with the built-in https/http modules
 * - Proxy rotation for multiple requests
 * - Error handling and retry logic
 * - Real-world usage patterns
 */

const { NodeMavenClient } = require('../src');
const https = require('https');
const http = require('http');
const { URL } = require('url');

async function makeRequestWithProxy(targetUrl, proxyConfig) {
  return new Promise((resolve, reject) => {
    try {
      const url = new URL(targetUrl);
      const isHttps = url.protocol === 'https:';
      const protocol = isHttps ? https : http;
      
      const options = {
        hostname: proxyConfig.host,
        port: proxyConfig.http_port,
        path: targetUrl,
        method: 'GET',
        headers: {
          'Host': url.hostname,
          'User-Agent': 'NodeMaven-JavaScript-Client/1.0.0',
          'Proxy-Authorization': `Basic ${Buffer.from(`${proxyConfig.username}:${proxyConfig.password}`).toString('base64')}`
        },
        timeout: 30000
      };

      const req = protocol.request(options, (res) => {
        let data = '';
        
        res.on('data', (chunk) => {
          data += chunk;
        });
        
        res.on('end', () => {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            body: data
          });
        });
      });

      req.on('error', (error) => {
        reject(new Error(`Request failed: ${error.message}`));
      });

      req.on('timeout', () => {
        req.destroy();
        reject(new Error('Request timeout'));
      });

      req.end();
    } catch (error) {
      reject(new Error(`Request setup failed: ${error.message}`));
    }
  });
}

async function basicProxyExample() {
  console.log('🌐 Basic Proxy Integration Example\n');

  try {
    const client = new NodeMavenClient();
    
    // Get proxy configuration for US
    console.log('🔧 Getting proxy configuration for US...');
    const proxyConfig = await client.getProxyConfig({
      country: 'US',
      city: 'new_york'
    });
    
    console.log(`Proxy: ${proxyConfig.host}:${proxyConfig.http_port}`);
    console.log(`Username: ${proxyConfig.username}`);
    
    // Make request through proxy to check IP
    console.log('\n📡 Making request through proxy...');
    const response = await makeRequestWithProxy('https://httpbin.org/ip', proxyConfig);
    
    console.log(`Status: ${response.statusCode}`);
    if (response.statusCode === 200) {
      const responseData = JSON.parse(response.body);
      console.log(`Detected IP: ${responseData.origin}`);
    }
    
    console.log('✅ Basic proxy example completed successfully!');
    
  } catch (error) {
    console.error('❌ Basic proxy example failed:', error.message);
    throw error;
  }
}

async function proxyRotationExample() {
  console.log('\n🔄 Proxy Rotation Example\n');

  try {
    const client = new NodeMavenClient();
    
    // Define different locations for rotation
    const locations = [
      { country: 'US', city: 'new_york' },
      { country: 'UK', city: 'london' },
      { country: 'DE', city: 'berlin' }
    ];
    
    console.log('🌍 Testing proxy rotation across different locations...\n');
    
    for (let i = 0; i < locations.length; i++) {
      const location = locations[i];
      console.log(`${i + 1}. Testing ${location.country} - ${location.city}...`);
      
      try {
        // Get proxy config for this location
        const proxyConfig = await client.getProxyConfig(location);
        
        // Make request through this proxy
        const response = await makeRequestWithProxy('https://httpbin.org/ip', proxyConfig);
        
        if (response.statusCode === 200) {
          const responseData = JSON.parse(response.body);
          console.log(`   ✅ Success - IP: ${responseData.origin}`);
        } else {
          console.log(`   ⚠️  Unexpected status: ${response.statusCode}`);
        }
        
      } catch (error) {
        console.log(`   ❌ Failed: ${error.message}`);
      }
      
      // Wait between requests
      if (i < locations.length - 1) {
        console.log('   ⏱️  Waiting 2 seconds...\n');
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
    }
    
    console.log('\n✅ Proxy rotation example completed!');
    
  } catch (error) {
    console.error('❌ Proxy rotation example failed:', error.message);
    throw error;
  }
}

async function retryWithProxyExample() {
  console.log('\n🔁 Retry Logic Example\n');

  try {
    const client = new NodeMavenClient();
    
    async function makeRequestWithRetry(targetUrl, location, maxRetries = 3) {
      for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
          console.log(`   Attempt ${attempt}/${maxRetries}...`);
          
          // Get fresh proxy config for each attempt
          const proxyConfig = await client.getProxyConfig(location);
          
          // Make request
          const response = await makeRequestWithProxy(targetUrl, proxyConfig);
          
          if (response.statusCode === 200) {
            return response;
          } else {
            throw new Error(`HTTP ${response.statusCode}`);
          }
          
        } catch (error) {
          console.log(`   ❌ Attempt ${attempt} failed: ${error.message}`);
          
          if (attempt === maxRetries) {
            throw new Error(`All ${maxRetries} attempts failed. Last error: ${error.message}`);
          }
          
          // Wait before retry
          const waitTime = attempt * 1000; // Exponential backoff
          console.log(`   ⏱️  Waiting ${waitTime}ms before retry...`);
          await new Promise(resolve => setTimeout(resolve, waitTime));
        }
      }
    }
    
    console.log('🔄 Testing retry logic with US proxy...');
    const response = await makeRequestWithRetry('https://httpbin.org/ip', { country: 'US' });
    
    if (response.statusCode === 200) {
      const responseData = JSON.parse(response.body);
      console.log(`✅ Success after retries - IP: ${responseData.origin}`);
    }
    
    console.log('\n✅ Retry logic example completed!');
    
  } catch (error) {
    console.error('❌ Retry logic example failed:', error.message);
    throw error;
  }
}

async function geoTargetingExample() {
  console.log('\n🎯 Geo-targeting Example\n');

  try {
    const client = new NodeMavenClient();
    
    // Test different geo-targeting options
    const targetingOptions = [
      { 
        name: 'Country only',
        config: { country: 'US' }
      },
      {
        name: 'Country + City',
        config: { country: 'US', city: 'los_angeles' }
      },
      {
        name: 'Country + Region',
        config: { country: 'US', region: 'california' }
      }
    ];
    
    for (const option of targetingOptions) {
      console.log(`🎯 Testing: ${option.name}`);
      console.log(`   Config: ${JSON.stringify(option.config)}`);
      
      try {
        const proxyConfig = await client.getProxyConfig(option.config);
        console.log(`   ✅ Generated proxy: ${proxyConfig.username}`);
        
        // Test the proxy
        const response = await makeRequestWithProxy('https://httpbin.org/ip', proxyConfig);
        if (response.statusCode === 200) {
          const responseData = JSON.parse(response.body);
          console.log(`   🌐 Detected IP: ${responseData.origin}`);
        }
        
      } catch (error) {
        console.log(`   ❌ Failed: ${error.message}`);
      }
      
      console.log('');
    }
    
    console.log('✅ Geo-targeting example completed!');
    
  } catch (error) {
    console.error('❌ Geo-targeting example failed:', error.message);
    throw error;
  }
}

async function main() {
  try {
    console.log('🚀 NodeMaven JavaScript SDK - Proxy Integration Examples\n');
    
    await basicProxyExample();
    await proxyRotationExample();
    await retryWithProxyExample();
    await geoTargetingExample();
    
    console.log('\n🎉 All proxy integration examples completed successfully!');
    
  } catch (error) {
    console.error('\n💥 Examples failed:', error.message);
    process.exit(1);
  }
}

// Run the example if this file is executed directly
if (require.main === module) {
  main().catch(error => {
    console.error('❌ Example execution failed:', error.message);
    process.exit(1);
  });
}

module.exports = {
  makeRequestWithProxy,
  basicProxyExample,
  proxyRotationExample,
  retryWithProxyExample,
  geoTargetingExample
}; 