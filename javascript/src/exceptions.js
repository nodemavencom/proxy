/**
 * NodeMaven API Exception Classes
 */

class NodeMavenAPIError extends Error {
  constructor(message, statusCode = null, response = null) {
    super(message);
    this.name = 'NodeMavenAPIError';
    this.statusCode = statusCode;
    this.response = response;
  }
}

class AuthenticationError extends NodeMavenAPIError {
  constructor(message, response = null) {
    super(message, 401, response);
    this.name = 'AuthenticationError';
  }
}

class ValidationError extends NodeMavenAPIError {
  constructor(message, response = null) {
    super(message, 400, response);
    this.name = 'ValidationError';
  }
}

class NotFoundError extends NodeMavenAPIError {
  constructor(message, response = null) {
    super(message, 404, response);
    this.name = 'NotFoundError';
  }
}

class RateLimitError extends NodeMavenAPIError {
  constructor(message, response = null) {
    super(message, 429, response);
    this.name = 'RateLimitError';
  }
}

class ServerError extends NodeMavenAPIError {
  constructor(message, statusCode = 500, response = null) {
    super(message, statusCode, response);
    this.name = 'ServerError';
  }
}

/**
 * Get appropriate exception for HTTP status code
 */
function getExceptionForStatusCode(statusCode, message, response = null) {
  switch (statusCode) {
    case 400:
      return new ValidationError(message, response);
    case 401:
      return new AuthenticationError(message, response);
    case 404:
      return new NotFoundError(message, response);
    case 429:
      return new RateLimitError(message, response);
    case 500:
    case 502:
    case 503:
    case 504:
      return new ServerError(message, statusCode, response);
    default:
      return new NodeMavenAPIError(message, statusCode, response);
  }
}

module.exports = {
  NodeMavenAPIError,
  AuthenticationError,
  ValidationError,
  NotFoundError,
  RateLimitError,
  ServerError,
  getExceptionForStatusCode
}; 