# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

SharePoint Video Linker is a Flask web application that authenticates with SharePoint/OneDrive, enables browsing folders and MP4 files, and generates anonymous public direct download links for use with Metricool and similar services.

## Development Commands

### Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Create environment configuration from template
cp .env.example .env
# Then edit .env with actual SharePoint credentials
```

### Running the Application
```bash
# Start the Flask development server (runs on port 5000)
python app.py

# Access the application
# Navigate to http://localhost:5000 in browser
```

### Testing Connection
The app includes a `/test-connection` endpoint to verify SharePoint authentication before browsing files.

## Architecture

### Backend Structure
- **app.py** - Single Flask application file containing all routes and SharePoint integration logic
- **Authentication** - Uses `Office365-REST-Python-Client` with username/password authentication via `AuthenticationContext`
- **Session Management** - Flask sessions with randomly generated secret key on each startup

### Key Routes
- `GET /` - Home page, shows setup instructions if credentials missing
- `GET /browse?path=<folder_path>` - Returns JSON with folders and MP4 files at specified path
- `POST /generate-link` - Creates anonymous sharing link and converts to direct download format
- `POST /test-connection` - Validates SharePoint credentials and connectivity

### Frontend Structure
- **templates/index.html** - Main browser interface with embedded CSS and JavaScript
- **templates/setup.html** - Credentials setup page shown when `.env` is not configured
- Pure HTML/CSS/JS (no frameworks) with client-side folder navigation and link generation UI

### SharePoint Integration
- Default folder path: `Shared Documents`
- Filters display to only show `.mp4` files
- Creates anonymous sharing links with 365-day expiration (configurable in `app.py` line 115)
- Converts SharePoint sharing URLs to direct download format by modifying URL pattern

### Link Generation Process
1. File selected from browser UI
2. `share_link()` called with `kind=4` (anonymous) and expiration date
3. Sharing URL converted to direct download format:
   - Pattern: `/:v:/g/` → `/download?`
   - Ensures `?download=1` parameter present
4. Returns both sharing URL and direct download URL

## Configuration

### Environment Variables (.env)
- `SHAREPOINT_SITE_URL` - Full SharePoint site URL (e.g., `https://company.sharepoint.com/sites/sitename`)
- `SHAREPOINT_USERNAME` - SharePoint user email
- `SHAREPOINT_PASSWORD` - SharePoint password

**Security Note:** The `.env` file is gitignored and must never be committed.

### SharePoint Requirements
- SharePoint Online account with read access to target site
- Anonymous sharing must be enabled at the SharePoint tenant/site level
- Links are public and expire after 365 days by default

## Common Issues

### Authentication Failures
- Verify `SHAREPOINT_SITE_URL` format matches SharePoint site structure
- Confirm user has permissions to access the SharePoint site
- Check for MFA requirements (this app uses basic username/password only)

### Link Generation Failures
- SharePoint admin may have disabled anonymous sharing
- Some organizations block external sharing entirely
- URL conversion logic assumes standard SharePoint URL patterns

## Dependencies

- **Flask 3.0.0** - Web framework
- **Office365-REST-Python-Client 2.5.3** - SharePoint API client
- **python-dotenv 1.0.0** - Environment variable management

No database, no caching, no external services beyond SharePoint.
