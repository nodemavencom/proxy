#!/usr/bin/env node

/**
 * NodeMaven JavaScript SDK - Quick Test
 * 
 * This script quickly validates that the NodeMaven JavaScript SDK is working correctly.
 * Similar to the Python quick_test.py functionality.
 */

const { NodeMavenClient } = require('./src');

async function testBasicFunctionality() {
  console.log('🧪 NodeMaven JavaScript SDK - Quick Test\n');

  try {
    // Test 1: Client initialization
    console.log('1️⃣  Testing client initialization...');
    const client = new NodeMavenClient();
    console.log('✅ Client initialized successfully');

    // Test 2: API connectivity
    console.log('\n2️⃣  Testing API connectivity...');
    const userInfo = await client.getUserInfo();
    console.log('✅ API connection successful');
    console.log(`   Username: ${userInfo.username}`);
    console.log(`   Proxy Username: ${userInfo.proxy_username}`);

    // Test 3: Location data retrieval
    console.log('\n3️⃣  Testing location data retrieval...');
    const countries = await client.getCountries({ limit: 5 });
    console.log(`✅ Retrieved ${countries.results.length} countries`);
    countries.results.forEach((country, index) => {
      console.log(`   ${index + 1}. ${country.name} (${country.code})`);
    });

    // Test 4: Proxy configuration generation
    console.log('\n4️⃣  Testing proxy configuration generation...');
    const proxyConfig = await client.getProxyConfig({ country: 'US' });
    console.log('✅ Proxy configuration generated successfully');
    console.log(`   Host: ${proxyConfig.host}`);
    console.log(`   HTTP Port: ${proxyConfig.http_port}`);
    console.log(`   Username: ${proxyConfig.username}`);

    // Test 5: SOCKS5 URL generation
    console.log('\n5️⃣  Testing SOCKS5 URL generation...');
    const socks5Url = await client.getSocks5ProxyUrl({ country: 'UK' });
    console.log('✅ SOCKS5 URL generated successfully');
    console.log(`   URL: ${socks5Url.substring(0, 50)}...`);

    console.log('\n🎉 All tests passed! NodeMaven JavaScript SDK is working correctly.');
    return true;

  } catch (error) {
    console.error('\n❌ Test failed:');
    console.error(`   Type: ${error.constructor.name}`);
    console.error(`   Message: ${error.message}`);
    
    if (error.statusCode) {
      console.error(`   Status Code: ${error.statusCode}`);
    }

    return false;
  }
}

async function checkEnvironment() {
  console.log('🔧 Environment Check\n');
  
  // Check Node.js version
  const nodeVersion = process.version;
  console.log(`Node.js Version: ${nodeVersion}`);
  
  if (parseInt(nodeVersion.substring(1)) < 16) {
    console.log('⚠️  Warning: Node.js 16+ is recommended');
  } else {
    console.log('✅ Node.js version is compatible');
  }

  // Check API key
  const apiKey = process.env.NODEMAVEN_APIKEY;
  if (apiKey) {
    console.log('✅ NODEMAVEN_APIKEY environment variable is set');
  } else {
    console.log('❌ NODEMAVEN_APIKEY environment variable is not set');
    console.log('   Please set your API key: export NODEMAVEN_APIKEY="your-key-here"');
    return false;
  }

  console.log('');
  return true;
}

async function main() {
  const envOk = await checkEnvironment();
  if (!envOk) {
    console.log('❌ Environment check failed. Please fix the issues above.');
    process.exit(1);
  }

  const testResult = await testBasicFunctionality();
  if (!testResult) {
    console.log('\n❌ Quick test failed. Please check your configuration.');
    process.exit(1);
  }

  console.log('\n✅ Quick test completed successfully!');
  console.log('\n📖 Next steps:');
  console.log('   - Check out examples: node examples/basic_usage.js');
  console.log('   - Read the documentation in README.md');
  console.log('   - Visit: https://dashboard.nodemaven.com');
}

// Display usage information
function showUsage() {
  console.log('NodeMaven JavaScript SDK - Quick Test');
  console.log('');
  console.log('Usage:');
  console.log('  node quick_test.js');
  console.log('');
  console.log('Environment Variables:');
  console.log('  NODEMAVEN_APIKEY    Your NodeMaven API key (required)');
  console.log('  NODEMAVEN_BASE_URL  API base URL (optional)');
  console.log('');
  console.log('Get your API key at: https://dashboard.nodemaven.com');
}

// Run the quick test if this file is executed directly
if (require.main === module) {
  // Show usage if --help is provided
  if (process.argv.includes('--help') || process.argv.includes('-h')) {
    showUsage();
    process.exit(0);
  }

  main().catch(error => {
    console.error('❌ Quick test execution failed:', error.message);
    process.exit(1);
  });
}

module.exports = {
  testBasicFunctionality,
  checkEnvironment,
  main
}; 