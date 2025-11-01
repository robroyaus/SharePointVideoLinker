# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

VideoBridge is a Flask web application that bridges SharePoint and Dropbox, allowing users to browse SharePoint video files, copy them to Dropbox, and generate direct public download links that work with Metricool and similar services. The split-screen interface shows SharePoint files in the top panel and Dropbox files in the bottom panel.

## Development Commands

### Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Create environment configuration from template
cp .env_example .env
# Then edit .env with SharePoint site URL, Dropbox token, and app credentials
```

### Running the Application
```bash
# Development mode (local Flask server on port 5000)
python app.py

# Development mode with ngrok tunnel (runs Flask in background)
./start.sh
```

### Deployment to DreamHost
```bash
# Review deployment checklist and instructions
./deploy-dreamhost.sh

# After uploading to DreamHost server, restart Passenger
ssh user@server "cd ~/yourdomain.com && touch tmp/restart.txt"

# Check DreamHost error logs
ssh user@server "tail -f ~/yourdomain.com/logs/error.log"
```

### Getting Dropbox Token
```bash
# Interactive script to obtain Dropbox access token
python get_dropbox_token.py
```

## Architecture

### Dual-Service Integration

The application integrates two cloud storage services to work around SharePoint's redirect-based sharing links, which don't provide proper `Content-Type: video/mp4` headers required by services like Metricool.

**SharePoint (Microsoft Graph API):**
- OAuth2 device flow authentication with MFA support
- Uses MSAL library with persistent token cache (`token_cache.json`)
- Browse folders and files using Graph API endpoints
- Copy files to Dropbox for link generation

**Dropbox API:**
- Long-lived access token authentication
- Direct download links via `dl.dropboxusercontent.com` domain
- File management (upload, delete, list)
- Links work universally without redirects

### Backend Structure (app.py)

Single Flask application file (~550 lines) organized into route groups:

**Authentication & Core Routes (lines 1-136):**
- Basic HTTP authentication decorator (`@requires_auth`)
- Session management with random secret key
- Home page and setup page routing

**SharePoint Routes (lines 138-371):**
- `/browse` - List folders and MP4 files using Graph API
- `/generate-link` - Create SharePoint sharing links and proxy URLs
- `/video/<site_id>/<drive_id>/<item_id>` - Direct video streaming proxy
- `/test-connection` - Validate SharePoint authentication

**Dropbox Routes (lines 373-549):**
- `/dropbox/list` - List MP4 files in configured folder
- `/dropbox/copy` - Copy file from SharePoint to Dropbox (chunked upload for large files)
- `/dropbox/delete` - Delete file from Dropbox
- `/dropbox/link` - Generate direct download link (converts to `dl.dropboxusercontent.com`)

### Key Helper Functions

- `parse_site_url()` - Extract tenant and site path from SharePoint URL
- `get_access_token()` - MSAL device flow authentication with cache
- `get_graph_headers()` - Build Authorization headers for Graph API
- `get_dropbox_client()` - Initialize authenticated Dropbox client

### Token Management

**SharePoint (MSAL):**
- Device code flow initiated when cache expires
- Token cache persisted to `token_cache.json`
- Silent token refresh attempted on each request
- Public client app ID: `14d82eec-204b-4c2f-b7e8-296a70dab67e` (Microsoft Graph PowerShell)

**Dropbox:**
- Long-lived access token from environment variable
- No automatic refresh mechanism (tokens don't expire unless revoked)

### Frontend Structure

**templates/index.html** - Split-screen interface:
- Top panel: SharePoint folder browser with breadcrumb navigation
- Bottom panel: Dropbox file list with link generation
- Embedded JavaScript for AJAX requests and clipboard operations
- No frontend framework - vanilla HTML/CSS/JS

**templates/setup.html** - Configuration instructions when `.env` is missing

### Video Streaming Proxy

The `/video/<site_id>/<drive_id>/<item_id>` route acts as a proxy to work around SharePoint's redirect behavior:

1. Fetches `@microsoft.graph.downloadUrl` from Graph API
2. Streams video content in 8KB chunks
3. Sets proper `Content-Type: video/mp4` header
4. Adds `Accept-Ranges: bytes` for seeking support
5. Returns public URL (uses `PUBLIC_URL` env var for ngrok tunnels)

### File Transfer Flow

**SharePoint → Dropbox Copy:**
1. Client requests `/dropbox/copy` with SharePoint file metadata
2. Backend fetches `@microsoft.graph.downloadUrl` from Graph API
3. Downloads file stream from SharePoint
4. Uploads to Dropbox (chunked for files > 4MB)
5. Returns success with Dropbox path

**Link Generation:**
1. Client requests `/dropbox/link` with Dropbox file path
2. Backend creates or retrieves shared link via Dropbox API
3. Converts `www.dropbox.com` URL to `dl.dropboxusercontent.com`
4. Returns direct download link (no redirects, proper Content-Type)

## Configuration

### Environment Variables (.env)

**SharePoint:**
- `SHAREPOINT_SITE_URL` - Full site URL (e.g., `https://company.sharepoint.com/sites/sitename`)
- `SHAREPOINT_START_FOLDER` - Default folder path (e.g., `Shared Documents/Videos`)

**Dropbox:**
- `DROPBOX_ACCESS_TOKEN` - Long-lived API access token
- `DROPBOX_FOLDER` - Target folder for copied files (e.g., `/Apps/SharePointVideos`)

**Application:**
- `APP_USERNAME` - Basic auth username
- `APP_PASSWORD` - Basic auth password
- `PUBLIC_URL` - (Optional) Public URL for ngrok/proxy scenarios

**Security:** `.env` is gitignored. Never commit credentials. Token cache file also contains sensitive data.

### DreamHost Deployment

**passenger_wsgi.py** - WSGI entry point:
- Loads `.env` file using python-dotenv
- Imports Flask app as `application` (Passenger requirement)
- Debug mode disabled for production

**.htaccess** - Apache/Passenger configuration:
- Must update `PassengerAppRoot` with actual server path
- Optional: Add basic authentication layer

**Restart mechanism:**
```bash
mkdir -p tmp && touch tmp/restart.txt
```

## Dependencies

- **Flask 3.0.0** - Web framework
- **msal 1.24.0** - Microsoft Authentication Library (OAuth2 device flow)
- **requests 2.31.0** - HTTP client for Graph API calls
- **python-dotenv 1.0.0** - Environment variable management
- **dropbox 11.36.2** - Dropbox API client

## Common Issues

### SharePoint Authentication
- Delete `token_cache.json` to force re-authentication
- Device flow requires MFA code entry in browser
- Check that `SHAREPOINT_SITE_URL` format is correct (must include `/sites/sitename`)

### Dropbox Token Expiration
- Tokens are long-lived but can be revoked
- Use `get_dropbox_token.py` to generate new token
- Verify token has full Dropbox access (not app folder only)

### DreamHost Passenger Issues
- Check Python version: `python3 --version` (requires 3.7+)
- Verify dependencies installed in user space: `pip3 list --user`
- Review logs: `tail -f logs/error.log`
- Ensure `passenger_wsgi.py` has correct import paths
