"""
NodeMaven Python SDK

Official Python client library for NodeMaven proxy services.
Provides comprehensive proxy management, IP geolocation, and testing utilities.

Example usage:
    from nodemaven import NodeMavenClient
    
    client = NodeMavenClient()
    user_info = client.get_user_info()
    print(f"Connected as: {user_info['email']}")
"""

__version__ = "1.0.0"
__author__ = "NodeMaven Team"
__email__ = "support@nodemaven.com"
__license__ = "MIT"
__url__ = "https://github.com/nodemavencom/proxy"

from .client import NodeMavenClient
from .exceptions import (
    NodeMavenAPIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    ServerError
)

__all__ = [
    "NodeMavenClient",
    "__version__",
    "NodeMavenAPIError",
    "AuthenticationError", 
    "RateLimitError",
    "ValidationError",
    "NotFoundError",
    "ServerError"
] 