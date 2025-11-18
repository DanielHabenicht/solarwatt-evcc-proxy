#!/usr/bin/env python3
"""
Solarwatt EVCC Proxy Server

This proxy server handles authentication to the Solarwatt API and forwards
requests from EVCC to the authenticated Solarwatt API endpoints.
"""

import os
import logging
from flask import Flask, request, Response
import requests
from requests.auth import HTTPBasicAuth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration from environment variables
SOLARWATT_API_URL = os.getenv('SOLARWATT_API_URL', 'https://api.solarwatt.com')
SOLARWATT_USERNAME = os.getenv('SOLARWATT_USERNAME', '')
SOLARWATT_PASSWORD = os.getenv('SOLARWATT_PASSWORD', '')
PROXY_PORT = int(os.getenv('PROXY_PORT', '8080'))
PROXY_HOST = os.getenv('PROXY_HOST', '0.0.0.0')

# Session to reuse connections
session = requests.Session()
if SOLARWATT_USERNAME and SOLARWATT_PASSWORD:
    session.auth = HTTPBasicAuth(SOLARWATT_USERNAME, SOLARWATT_PASSWORD)


def forward_request(path):
    """
    Forward the request to the Solarwatt API with authentication.
    
    Args:
        path: The API path to forward to
        
    Returns:
        Response object with the proxied response
    """
    # Build the target URL
    target_url = f"{SOLARWATT_API_URL.rstrip('/')}/{path.lstrip('/')}"
    
    # Get query parameters
    params = request.args.to_dict()
    
    # Get headers (exclude host header)
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}
    
    # Get request body
    data = request.get_data()
    
    try:
        logger.info(f"Proxying {request.method} request to {target_url}")
        
        # Forward the request with authentication
        response = session.request(
            method=request.method,
            url=target_url,
            headers=headers,
            params=params,
            data=data,
            allow_redirects=False,
            timeout=30
        )
        
        # Create response with the same status code and headers
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = [
            (name, value) for name, value in response.headers.items()
            if name.lower() not in excluded_headers
        ]
        
        return Response(
            response.content,
            status=response.status_code,
            headers=response_headers
        )
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error proxying request: {e}")
        return Response(
            f"Proxy error: {str(e)}",
            status=502
        )


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def proxy(path):
    """
    Proxy endpoint that forwards all requests to the Solarwatt API.
    """
    return forward_request(path)


@app.route('/health')
def health():
    """
    Health check endpoint for monitoring.
    """
    return {'status': 'healthy', 'service': 'solarwatt-evcc-proxy'}, 200


if __name__ == '__main__':
    # Check if credentials are configured
    if not SOLARWATT_USERNAME or not SOLARWATT_PASSWORD:
        logger.warning("Solarwatt credentials not configured. Set SOLARWATT_USERNAME and SOLARWATT_PASSWORD environment variables.")
    
    logger.info(f"Starting proxy server on {PROXY_HOST}:{PROXY_PORT}")
    logger.info(f"Proxying to: {SOLARWATT_API_URL}")
    
    app.run(
        host=PROXY_HOST,
        port=PROXY_PORT,
        debug=False
    )
