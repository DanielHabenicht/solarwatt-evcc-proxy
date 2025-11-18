# solarwatt-evcc-proxy

Proxy to make authenticated solarwatt API work with evcc

## Overview

This is a lightweight Python proxy server that handles authentication to the Solarwatt API, allowing EVCC (Electric Vehicle Charge Controller) to access the API without needing to manage credentials directly.

## Features

- 🔐 Automatic authentication handling for Solarwatt API
- 🚀 Dockerized application for easy deployment
- 🛠️ DevContainer support for streamlined development
- 🏥 Health check endpoint for monitoring
- 📦 Production-ready with Gunicorn WSGI server
- 🔄 Forwards all HTTP methods (GET, POST, PUT, DELETE, etc.)

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/DanielHabenicht/solarwatt-evcc-proxy.git
cd solarwatt-evcc-proxy
```

2. Create a `.env` file with your Solarwatt credentials:
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

3. Start the proxy server:
```bash
docker-compose up -d
```

The proxy will be available at `http://localhost:8080`

### Using Docker

Build and run the container:
```bash
docker build -t solarwatt-proxy .
docker run -d -p 8080:8080 \
  -e SOLARWATT_USERNAME=your_username \
  -e SOLARWATT_PASSWORD=your_password \
  solarwatt-proxy
```

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export SOLARWATT_USERNAME=your_username
export SOLARWATT_PASSWORD=your_password
export SOLARWATT_API_URL=https://api.solarwatt.com
```

3. Run the server:
```bash
python proxy_server.py
```

## Configuration

Configure the proxy using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `SOLARWATT_API_URL` | Base URL of the Solarwatt API | `https://api.solarwatt.com` |
| `SOLARWATT_USERNAME` | Your Solarwatt username | (required) |
| `SOLARWATT_PASSWORD` | Your Solarwatt password | (required) |
| `PROXY_HOST` | Host to bind the proxy server | `0.0.0.0` |
| `PROXY_PORT` | Port to bind the proxy server | `8080` |

## DevContainer Support

This project includes full DevContainer support for VS Code:

1. Open the project in VS Code
2. Install the "Remote - Containers" extension
3. Click "Reopen in Container" when prompted
4. The development environment will be automatically set up

## Usage

Once the proxy is running, configure EVCC to use the proxy URL instead of the direct Solarwatt API URL:

```yaml
# Example EVCC configuration
meters:
  - name: solarwatt
    type: http
    uri: http://localhost:8080/api/endpoint
```

All requests to the proxy will be forwarded to the Solarwatt API with authentication headers automatically added.

## Health Check

The proxy includes a health check endpoint:

```bash
curl http://localhost:8080/health
```

Response:
```json
{
  "status": "healthy",
  "service": "solarwatt-evcc-proxy"
}
```

## Architecture

```
EVCC → Proxy Server (with auth) → Solarwatt API
```

The proxy:
1. Receives requests from EVCC
2. Adds authentication credentials (HTTP Basic Auth)
3. Forwards the request to the Solarwatt API
4. Returns the response back to EVCC

## Security Notes

- Store credentials securely in environment variables or `.env` file (never commit `.env` to git)
- The proxy runs as a non-root user in the Docker container
- Use HTTPS in production environments
- Consider using Docker secrets for credential management in production


## Alternatives

https://community.simon42.com/t/solarwatt-rest-api-verlangt-authorisierung-nach-software-update/66521/20
https://www.photovoltaikforum.com/thread/253422-solarwatt-cloud-update-zerschie%C3%9Ft-funktionierendes-monitoring/#post4515035
https://github.com/evcc-io/evcc/issues/24549

### Modbus 
- https://community.simon42.com/t/solarwatt-vision-steuern-via-modbus/67335
- https://github.com/nathanmarlor/foxess_modbus?tab=readme-ov-file
