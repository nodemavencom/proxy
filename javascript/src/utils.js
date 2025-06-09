/**
 * Utility functions for NodeMaven client
 */

/**
 * Get API key from environment or throw error
 */
function getApiKey(apiKey = null) {
  return apiKey || process.env.NODEMAVEN_APIKEY || null;
}

/**
 * Get base URL with default fallback
 */
function getBaseUrl(baseUrl = null) {
  return baseUrl || process.env.NODEMAVEN_BASE_URL || 'https://dashboard.nodemaven.com';
}

/**
 * Get proxy host with default fallback
 */
function getProxyHost(proxyHost = null) {
  return proxyHost || process.env.NODEMAVEN_PROXY_HOST || 'gate.nodemaven.com';
}

/**
 * Get HTTP port with default fallback
 */
function getHttpPort(httpPort = null) {
  return httpPort || parseInt(process.env.NODEMAVEN_HTTP_PORT || '8080', 10);
}

/**
 * Get SOCKS5 port with default fallback
 */
function getSocks5Port(socks5Port = null) {
  return socks5Port || parseInt(process.env.NODEMAVEN_SOCKS5_PORT || '1080', 10);
}

/**
 * Get timeout with default fallback
 */
function getTimeout(timeout = null) {
  return timeout || parseInt(process.env.REQUEST_TIMEOUT || '30000', 10);
}

/**
 * Clean dictionary by removing null/undefined values
 */
function cleanDict(obj) {
  if (!obj) return {};
  
  const cleaned = {};
  for (const [key, value] of Object.entries(obj)) {
    if (value !== null && value !== undefined && value !== '') {
      cleaned[key] = value;
    }
  }
  return cleaned;
}

/**
 * Parse error message from API response
 */
function parseErrorMessage(errorData, statusCode = null, status = null) {
  if (!errorData) {
    return status || `HTTP ${statusCode}` || 'Unknown error';
  }

  // Try common error message fields
  if (errorData.detail) return errorData.detail;
  if (errorData.message) return errorData.message;
  if (errorData.error) return errorData.error;
  if (errorData.non_field_errors && Array.isArray(errorData.non_field_errors)) {
    return errorData.non_field_errors.join(', ');
  }

  // If it's an object with field errors, combine them
  if (typeof errorData === 'object' && !Array.isArray(errorData)) {
    const errors = [];
    for (const [field, messages] of Object.entries(errorData)) {
      if (Array.isArray(messages)) {
        errors.push(`${field}: ${messages.join(', ')}`);
      } else if (typeof messages === 'string') {
        errors.push(`${field}: ${messages}`);
      }
    }
    if (errors.length > 0) {
      return errors.join('; ');
    }
  }

  return status || `HTTP ${statusCode}` || 'Unknown error';
}

/**
 * Validate date format (YYYY-MM-DD)
 */
function validateDateFormat(dateStr) {
  if (!dateStr) return true;
  
  const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
  if (!dateRegex.test(dateStr)) {
    return false;
  }
  
  const date = new Date(dateStr);
  return date instanceof Date && !isNaN(date) && date.toISOString().substr(0, 10) === dateStr;
}

/**
 * Build query string from parameters
 */
function buildQueryString(params) {
  const cleaned = cleanDict(params);
  const searchParams = new URLSearchParams();
  
  for (const [key, value] of Object.entries(cleaned)) {
    searchParams.append(key, value.toString());
  }
  
  return searchParams.toString();
}

/**
 * Generate proxy configuration object
 */
function generateProxyConfig(proxyHost, httpPort, socks5Port, proxyUsername, proxyPassword, options = {}) {
  const config = {
    host: proxyHost,
    http_port: httpPort,
    socks5_port: socks5Port,
    username: proxyUsername,
    password: proxyPassword
  };

  // Add location parameters to username if provided
  const locationParts = [];
  if (options.country) locationParts.push(`country-${options.country}`);
  if (options.region) locationParts.push(`region-${options.region}`);
  if (options.city) locationParts.push(`city-${options.city}`);
  if (options.isp) locationParts.push(`isp-${options.isp}`);
  if (options.zip_code) locationParts.push(`zip-${options.zip_code}`);
  if (options.connection_type) locationParts.push(`session-${options.connection_type}`);

  if (locationParts.length > 0) {
    config.username = `${proxyUsername}-${locationParts.join('-')}`;
  }

  return config;
}

/**
 * Generate SOCKS5 proxy URL
 */
function generateSocks5ProxyUrl(proxyHost, socks5Port, proxyUsername, proxyPassword, options = {}) {
  const config = generateProxyConfig(proxyHost, null, socks5Port, proxyUsername, proxyPassword, options);
  return `socks5://${config.username}:${proxyPassword}@${proxyHost}:${socks5Port}`;
}

module.exports = {
  getApiKey,
  getBaseUrl,
  getProxyHost,
  getHttpPort,
  getSocks5Port,
  getTimeout,
  cleanDict,
  parseErrorMessage,
  validateDateFormat,
  buildQueryString,
  generateProxyConfig,
  generateSocks5ProxyUrl
}; 