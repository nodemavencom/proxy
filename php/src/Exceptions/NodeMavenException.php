<?php

declare(strict_types=1);

namespace NodeMaven\Exceptions;

use Exception;

/**
 * Base NodeMaven exception
 */
class NodeMavenException extends Exception
{
    protected int $statusCode;

    /**
     * Initialize exception
     * 
     * @param string $message Error message
     * @param int $statusCode HTTP status code
     * @param Exception|null $previous Previous exception
     */
    public function __construct(string $message = '', int $statusCode = 0, Exception $previous = null)
    {
        parent::__construct($message, 0, $previous);
        $this->statusCode = $statusCode;
    }

    /**
     * Get HTTP status code
     * 
     * @return int
     */
    public function getStatusCode(): int
    {
        return $this->statusCode;
    }

    /**
     * Get error details as array
     * 
     * @return array
     */
    public function toArray(): array
    {
        return [
            'error' => static::class,
            'message' => $this->getMessage(),
            'status_code' => $this->statusCode,
            'file' => $this->getFile(),
            'line' => $this->getLine(),
        ];
    }
} 