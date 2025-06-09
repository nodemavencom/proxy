/**
 * NodeMaven API Client
 * A JavaScript client library for the NodeMaven proxy service API.
 * Provides access to residential and mobile proxies with global coverage.
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');
const { getExceptionForStatusCode } = require('./exceptions');
const {
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
} = require('./utils');

// Constants
const DEFAULT_BASE_URL = 'https://dashboard.nodemaven.com';
const DEFAULT_PROXY_HOST = 'gate.nodemaven.com';
const DEFAULT_HTTP_PORT = 8080;
const DEFAULT_SOCKS5_PORT = 1080;
const DEFAULT_TIMEOUT = 30000;
const USER_AGENT = 'NodeMaven-JavaScript-Client/1.0.0';

class NodeMavenClient {
  /**
   * NodeMaven API client for managing residential and mobile proxies.
   * 
   * @param {Object} config - Configuration options
   * @param {string} config.apiKey - API key for authentication
   * @param {string} config.baseUrl - Base URL for API requests
   * @param {string} config.proxyHost - Proxy host for connections
   * @param {number} config.httpPort - HTTP proxy port
   * @param {number} config.socks5Port - SOCKS5 proxy port
   * @param {number} config.timeout - Request timeout in milliseconds
   */
  constructor(config = {}) {
    // Get API key from config or environment
    this.apiKey = getApiKey(config.apiKey);
    if (!this.apiKey) {
      throw new Error('API key is required. Set NODEMAVEN_APIKEY environment variable or pass apiKey in config');
    }

    // Set configuration with defaults
    this.baseUrl = getBaseUrl(config.baseUrl);
    this.proxyHost = getProxyHost(config.proxyHost);
    this.httpPort = getHttpPort(config.httpPort);
    this.socks5Port = getSocks5Port(config.socks5Port);
    this.timeout = getTimeout(config.timeout);
  }

  /**
   * Make HTTP request to NodeMaven API
   * @private
   */
  async _makeRequest(method, endpoint, params = null, body = null) {
    return new Promise((resolve, reject) => {
      try {
        // Build URL
        const url = new URL(endpoint, this.baseUrl);
        
        // Add query parameters
        if (params) {
          const cleaned = cleanDict(params);
          for (const [key, value] of Object.entries(cleaned)) {
            url.searchParams.append(key, value.toString());
          }
        }

        // Prepare request body
        let requestBody = null;
        if (body) {
          requestBody = JSON.stringify(body);
        }

        // Choose http or https module
        const protocol = url.protocol === 'https:' ? https : http;

        // Request options
        const options = {
          hostname: url.hostname,
          port: url.port,
          path: url.pathname + url.search,
          method: method.toUpperCase(),
          headers: {
            'Authorization': `x-api-key ${this.apiKey}`,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': USER_AGENT
          },
          timeout: this.timeout
        };

        if (requestBody) {
          options.headers['Content-Length'] = Buffer.byteLength(requestBody);
        }

        // Make request
        const req = protocol.request(options, (res) => {
          let responseData = '';

          res.on('data', (chunk) => {
            responseData += chunk;
          });

          res.on('end', () => {
            try {
              // Handle successful responses
              if (res.statusCode < 400) {
                let result = {};
                if (responseData) {
                  result = JSON.parse(responseData);
                }
                resolve(result);
                return;
              }

              // Handle error responses
              let errorData = {};
              if (responseData) {
                try {
                  errorData = JSON.parse(responseData);
                } catch (e) {
                  errorData = { message: responseData };
                }
              }

              const errorMessage = parseErrorMessage(errorData, res.statusCode, res.statusMessage);
              const error = getExceptionForStatusCode(res.statusCode, errorMessage, errorData);
              reject(error);

            } catch (parseError) {
              reject(new Error(`Failed to parse response: ${parseError.message}`));
            }
          });
        });

        req.on('error', (error) => {
          reject(new Error(`Request failed: ${error.message}`));
        });

        req.on('timeout', () => {
          req.destroy();
          reject(new Error(`Request timeout after ${this.timeout}ms`));
        });

        // Write request body if present
        if (requestBody) {
          req.write(requestBody);
        }

        req.end();

      } catch (error) {
        reject(new Error(`Request setup failed: ${error.message}`));
      }
    });
  }

  /**
   * Get current user information including proxy credentials and usage data
   */
  async getUserInfo() {
    return await this._makeRequest('GET', '/api/v2/base/users/me');
  }

  /**
   * Get list of available countries for proxy connections
   * @param {Object} options - Query options
   * @param {number} options.limit - Number of results to return (default: 50)
   * @param {number} options.offset - Number of results to skip (default: 0)
   * @param {string} options.name - Filter by country name
   * @param {string} options.code - Filter by country code
   * @param {string} options.connectionType - Connection type (default: "residential")
   */
  async getCountries(options = {}) {
    const params = {
      limit: options.limit || 50,
      offset: options.offset || 0,
      name: options.name,
      code: options.code,
      connection_type: options.connectionType || 'residential'
    };
    return await this._makeRequest('GET', '/api/v2/base/locations/countries/', params);
  }

  /**
   * Get list of regions in specified countries
   * @param {Object} options - Query options
   * @param {number} options.limit - Number of results to return (default: 50)
   * @param {number} options.offset - Number of results to skip (default: 0)
   * @param {string} options.countryCode - Filter by country code
   * @param {string} options.name - Filter by region name
   * @param {string} options.code - Filter by region code
   * @param {string} options.connectionType - Connection type (default: "residential")
   */
  async getRegions(options = {}) {
    const params = {
      limit: options.limit || 50,
      offset: options.offset || 0,
      'country__code': options.countryCode,
      name: options.name,
      code: options.code,
      connection_type: options.connectionType || 'residential'
    };
    return await this._makeRequest('GET', '/api/v2/base/locations/regions/', params);
  }

  /**
   * Get list of cities in specified regions/countries
   * @param {Object} options - Query options
   * @param {number} options.limit - Number of results to return (default: 50)
   * @param {number} options.offset - Number of results to skip (default: 0)
   * @param {string} options.countryCode - Filter by country code
   * @param {string} options.regionCode - Filter by region code
   * @param {string} options.name - Filter by city name
   * @param {string} options.code - Filter by city code
   * @param {string} options.connectionType - Connection type (default: "residential")
   */
  async getCities(options = {}) {
    const params = {
      limit: options.limit || 50,
      offset: options.offset || 0,
      'country__code': options.countryCode,
      'region__code': options.regionCode,
      name: options.name,
      code: options.code,
      connection_type: options.connectionType || 'residential'
    };
    return await this._makeRequest('GET', '/api/v2/base/locations/cities/', params);
  }

  /**
   * Get list of ISPs in specified locations
   * @param {Object} options - Query options
   * @param {number} options.limit - Number of results to return (default: 50)
   * @param {number} options.offset - Number of results to skip (default: 0)
   * @param {string} options.countryCode - Filter by country code
   * @param {string} options.regionCode - Filter by region code
   * @param {string} options.cityCode - Filter by city code
   * @param {string} options.name - Filter by ISP name
   * @param {string} options.connectionType - Connection type (default: "residential")
   */
  async getIsps(options = {}) {
    const params = {
      limit: options.limit || 50,
      offset: options.offset || 0,
      'country__code': options.countryCode,
      'region__code': options.regionCode,
      'city__code': options.cityCode,
      name: options.name,
      connection_type: options.connectionType || 'residential'
    };
    return await this._makeRequest('GET', '/api/v2/base/locations/isps/', params);
  }

  /**
   * Get traffic statistics for the account
   * @param {Object} options - Query options
   * @param {string} options.startDate - Start date (YYYY-MM-DD format)
   * @param {string} options.endDate - End date (YYYY-MM-DD format)
   * @param {string} options.groupBy - Group by period (default: "day")
   */
  async getStatistics(options = {}) {
    if (options.startDate && !validateDateFormat(options.startDate)) {
      throw new Error('startDate must be in YYYY-MM-DD format');
    }
    if (options.endDate && !validateDateFormat(options.endDate)) {
      throw new Error('endDate must be in YYYY-MM-DD format');
    }

    const params = {
      start_date: options.startDate,
      end_date: options.endDate,
      group_by: options.groupBy || 'day'
    };
    return await this._makeRequest('GET', '/api/v2/base/statistics/', params);
  }

  /**
   * Generate proxy configuration for HTTP/HTTPS connections
   * @param {Object} options - Proxy options
   * @param {string} options.country - Country code for geo-targeting
   * @param {string} options.region - Region code for geo-targeting
   * @param {string} options.city - City code for geo-targeting
   * @param {string} options.isp - ISP for targeting
   * @param {string} options.zipCode - ZIP code for targeting
   * @param {string} options.connectionType - Connection type
   * @returns {Promise<Object>} Proxy configuration object
   */
  async getProxyConfig(options = {}) {
    const userInfo = await this.getUserInfo();
    
    if (!userInfo.proxy_username || !userInfo.proxy_password) {
      throw new Error('Proxy credentials not found in user info');
    }

    return generateProxyConfig(
      this.proxyHost,
      this.httpPort,
      this.socks5Port,
      userInfo.proxy_username,
      userInfo.proxy_password,
      options
    );
  }

  /**
   * Generate SOCKS5 proxy URL
   * @param {Object} options - Proxy options
   * @param {string} options.country - Country code for geo-targeting
   * @param {string} options.region - Region code for geo-targeting
   * @param {string} options.city - City code for geo-targeting
   * @param {string} options.isp - ISP for targeting
   * @param {string} options.zipCode - ZIP code for targeting
   * @param {string} options.connectionType - Connection type
   * @returns {Promise<string>} SOCKS5 proxy URL
   */
  async getSocks5ProxyUrl(options = {}) {
    const userInfo = await this.getUserInfo();
    
    if (!userInfo.proxy_username || !userInfo.proxy_password) {
      throw new Error('Proxy credentials not found in user info');
    }

    return generateSocks5ProxyUrl(
      this.proxyHost,
      this.socks5Port,
      userInfo.proxy_username,
      userInfo.proxy_password,
      options
    );
  }
}

module.exports = { NodeMavenClient }; 