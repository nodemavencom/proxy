# GitHub Workflows for NodeMaven

This directory contains GitHub Actions workflows that automatically test the NodeMaven Python SDK and allow community members to test with their own API keys.

## 🚀 Available Workflows

### 1. `python-tests.yml` - Main Testing Workflow

**Triggers:**
- ✅ **Automatic**: Runs on every push to `main`/`develop` branches
- ✅ **Pull Requests**: Runs on all PRs to `main` branch
- ✅ **Manual**: Can be triggered manually with custom settings

**What it does:**
- 🧪 **Always runs**: 31 unit tests (no API key needed)
- 🌐 **Conditionally runs**: 17 integration tests (API key required)
- 📊 **Generates**: Detailed test reports and summaries
- 🔍 **Tests**: Real proxy connections across multiple countries

## 🔧 How to Use

### For Developers (Automatic Testing)

Every time you push code or create a PR, the workflow automatically:
1. Runs all unit tests
2. Verifies code quality
3. Shows results directly in GitHub

### For Community Members (Test Your API Key)

**Option 1: Manual Workflow Run**
1. Go to [Actions tab](../actions)
2. Click "NodeMaven Python SDK Tests"
3. Click "Run workflow"
4. Fill in your settings:
   - Test Mode: `unit-only`, `integration-basic`, or `integration-full`
   - API Key: Your NodeMaven API key
   - Countries: `us,gb,ca` (or any combination)
5. Click "Run workflow"

**Option 2: Issue Template**
1. Go to [Issues tab](../issues)
2. Click "New issue"
3. Choose "🧪 Test with My API Key"
4. Fill out the form with your requirements
5. Follow the instructions to run tests

## 📊 What Gets Tested

### Unit Tests (Always Run - No API Key)
```
✅ Proxy username building (12 tests)
✅ TTL validation (2 tests) 
✅ Credential validation (4 tests)
✅ Utility functions (5 tests)
✅ Client initialization (3 tests)
✅ Configuration methods (5 tests)
```

### Integration Tests (API Key Required)
```
✅ Real API connectivity
✅ User authentication 
✅ Proxy connections (HTTP/SOCKS5)
✅ Multi-country verification
✅ Session persistence
✅ Error handling
```

## 🌍 Example Test Results

When you run integration tests, you'll see results like:
```
✅ API Key Valid - User: your@email.com
✅ US proxy working: 65.189.94.222
✅ GB proxy working: 86.22.70.218
✅ CA proxy working: 50.67.58.150
✅ Session persistence: Verified
```

## 🔐 Security Features

**API Key Protection:**
- ✅ **Not logged**: API keys never appear in logs
- ✅ **Not stored**: Keys are used only during test execution
- ✅ **Temporary**: Environment variables cleaned after tests
- ✅ **Masked**: GitHub automatically masks sensitive data

**Access Control:**
- ✅ **Public results**: Test results are public (no sensitive data)
- ✅ **Private inputs**: API keys remain private
- ✅ **Rate limiting**: Prevents abuse with reasonable limits

## 📈 Benefits for You

### As a Repository Owner:
1. **🚀 Confidence**: Every change is automatically tested
2. **🛡️ Quality**: Catch issues before they reach users
3. **📊 Visibility**: Clear status on all PRs and commits
4. **🤝 Community**: Let users test with their own accounts
5. **📚 Documentation**: Live examples of how things work

### As a Community Member:
1. **✅ Verification**: Test that SDK works with your account
2. **🔍 Debugging**: Identify issues specific to your setup
3. **🌍 Coverage**: Test proxies in your required countries
4. **📋 Reports**: Get detailed results and troubleshooting info
5. **💡 Examples**: See real working configurations

## 🎯 Real-World Benefits

### For Development:
- **Faster releases**: Automated testing catches issues early
- **Better quality**: Comprehensive testing across scenarios
- **User confidence**: Community can verify functionality
- **Issue resolution**: Clear data when problems occur

### For Business:
- **Trust building**: Transparent testing builds user confidence
- **Support reduction**: Users can self-verify before issues
- **Market reach**: Easy for prospects to test functionality
- **Quality assurance**: Continuous validation of service quality

## 🚀 Next Steps

1. **Try it out**: Run the workflow with your API key
2. **Provide feedback**: Let us know how it works for you
3. **Suggest improvements**: What other tests would be helpful?
4. **Share results**: Help others by sharing your experience

## 🆘 Getting Help

- **Documentation**: Check the [Python SDK README](../python/README.md)
- **Issues**: Create an issue if you find problems
- **Community**: Join discussions in existing issues
- **Support**: Contact support@nodemaven.com for account issues

---

**This automated testing ensures NodeMaven Python SDK works reliably for everyone!** 🎉 