@echo off
echo ====================================
echo  NodeMaven Go SDK Setup
echo ====================================
echo.

if "%~1"=="" (
    echo Usage: setup.bat YOUR_API_KEY
    echo.
    echo Example: setup.bat eyJhbGciOiJIUzI1NiIs...
    echo.
    echo This will set the NODEMAVEN_APIKEY environment variable
    echo and test the connection.
    pause
    exit /b 1
)

echo Setting API key environment variable...
set "NODEMAVEN_APIKEY=%~1"

echo.
echo Testing connection...
go run test_basic.go

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Setup successful!
    echo.
    echo You can now run examples:
    echo   go run examples/basic_usage.go
    echo   go run examples/concurrent_usage.go
    echo.
    echo Note: This environment variable is only set for this session.
    echo To make it permanent, add it to your system environment variables.
) else (
    echo.
    echo ❌ Setup failed. Please check your API key.
)

pause 