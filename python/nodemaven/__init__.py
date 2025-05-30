"""
NodeMaven API Client

A Python client library for the NodeMaven proxy service API.
Provides access to residential and mobile proxies with global coverage.
"""

from .client import NodeMavenClient
from .exceptions import (
    NodeMavenAPIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    ServerError
)

__version__ = "1.0.0"
__author__ = "NodeMaven Team"
__email__ = "support@nodemaven.com"

__all__ = [
    "NodeMavenClient",
    "NodeMavenAPIError",
    "AuthenticationError", 
    "RateLimitError",
    "ValidationError",
    "NotFoundError",
    "ServerError"
] 