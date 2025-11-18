# solarwatt-evcc-proxy

Proxy to make the authenticated solarwatt API work with evcc (which does not support authentication) by acting as a Man-in-the-Middle.

```
EVCC → solarwatt-evcc-proxy → Solarwatt API
```

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
export SOLARWATT_PASSWORD=
export SOLARWATT_API_URL=http://192.168.100.120
```

3. Start the proxy server:
```bash
docker-compose up -d
```

The proxy will be available at `http://localhost:80`

#### Available Docker Tags

- `latest` - Latest stable release from the main branch
- `v*.*.*` - Specific version tags (e.g., `v1.0.0`)
- `main` - Latest commit on the main branch
- Multi-architecture support: `linux/amd64`, `linux/arm64`

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
python proxy_server.py
```

## Alternatives

https://community.simon42.com/t/solarwatt-rest-api-verlangt-authorisierung-nach-software-update/66521/20
https://www.photovoltaikforum.com/thread/253422-solarwatt-cloud-update-zerschie%C3%9Ft-funktionierendes-monitoring/#post4515035
https://github.com/evcc-io/evcc/issues/24549

### Modbus 
- https://community.simon42.com/t/solarwatt-vision-steuern-via-modbus/67335
- https://github.com/nathanmarlor/foxess_modbus?tab=readme-ov-file
