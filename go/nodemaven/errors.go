package nodemaven

import (
	"fmt"
	"net/http"
)

// NodeMavenError represents a base error from the NodeMaven API
type NodeMavenError struct {
	StatusCode int
	Message    string
	ErrorData  map[string]interface{}
}

func (e *NodeMavenError) Error() string {
	return fmt.Sprintf("NodeMaven API error (HTTP %d): %s", e.StatusCode, e.Message)
}

// AuthenticationError represents an authentication error (401)
type AuthenticationError struct {
	*NodeMavenError
}

func (e *AuthenticationError) Error() string {
	return fmt.Sprintf("Authentication error: %s", e.Message)
}

// ForbiddenError represents a forbidden error (403)
type ForbiddenError struct {
	*NodeMavenError
}

func (e *ForbiddenError) Error() string {
	return fmt.Sprintf("Forbidden: %s", e.Message)
}

// NotFoundError represents a not found error (404)
type NotFoundError struct {
	*NodeMavenError
}

func (e *NotFoundError) Error() string {
	return fmt.Sprintf("Not found: %s", e.Message)
}

// ValidationError represents a validation error (400, 422)
type ValidationError struct {
	*NodeMavenError
}

func (e *ValidationError) Error() string {
	return fmt.Sprintf("Validation error: %s", e.Message)
}

// RateLimitError represents a rate limit error (429)
type RateLimitError struct {
	*NodeMavenError
}

func (e *RateLimitError) Error() string {
	return fmt.Sprintf("Rate limit exceeded: %s", e.Message)
}

// ServerError represents a server error (5xx)
type ServerError struct {
	*NodeMavenError
}

func (e *ServerError) Error() string {
	return fmt.Sprintf("Server error: %s", e.Message)
}

// getExceptionForStatusCode returns the appropriate error type based on HTTP status code
func getExceptionForStatusCode(statusCode int, message string, errorData map[string]interface{}) error {
	baseError := &NodeMavenError{
		StatusCode: statusCode,
		Message:    message,
		ErrorData:  errorData,
	}

	switch statusCode {
	case http.StatusUnauthorized:
		return &AuthenticationError{NodeMavenError: baseError}
	case http.StatusForbidden:
		return &ForbiddenError{NodeMavenError: baseError}
	case http.StatusNotFound:
		return &NotFoundError{NodeMavenError: baseError}
	case http.StatusBadRequest, http.StatusUnprocessableEntity:
		return &ValidationError{NodeMavenError: baseError}
	case http.StatusTooManyRequests:
		return &RateLimitError{NodeMavenError: baseError}
	default:
		if statusCode >= 500 {
			return &ServerError{NodeMavenError: baseError}
		}
		return baseError
	}
}
