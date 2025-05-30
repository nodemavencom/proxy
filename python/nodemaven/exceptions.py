"""
Custom exceptions for NodeMaven API client.
"""

from typing import Optional, Dict, Any


class NodeMavenAPIError(Exception):
    """Base exception for all NodeMaven API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 response_data: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)
    
    def __str__(self):
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(NodeMavenAPIError):
    """Raised when API authentication fails (401, 403)."""
    pass


class RateLimitError(NodeMavenAPIError):
    """Raised when API rate limit is exceeded (429)."""
    pass


class ValidationError(NodeMavenAPIError):
    """Raised when request validation fails (400)."""
    pass


class NotFoundError(NodeMavenAPIError):
    """Raised when requested resource is not found (404)."""
    pass


class ServerError(NodeMavenAPIError):
    """Raised when server encounters an error (500+)."""
    pass


def get_exception_for_status_code(status_code: int, message: str, 
                                response_data: Optional[Dict[str, Any]] = None) -> NodeMavenAPIError:
    """Return appropriate exception for HTTP status code."""
    
    if status_code == 401:
        return AuthenticationError(message, status_code, response_data)
    elif status_code == 403:
        return AuthenticationError(message, status_code, response_data)
    elif status_code == 429:
        return RateLimitError(message, status_code, response_data)
    elif status_code == 400:
        return ValidationError(message, status_code, response_data)
    elif status_code == 404:
        return NotFoundError(message, status_code, response_data)
    elif status_code >= 500:
        return ServerError(message, status_code, response_data)
    else:
        return NodeMavenAPIError(message, status_code, response_data) 