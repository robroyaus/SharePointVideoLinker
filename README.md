# VideoBridge

A web application that bridges SharePoint and Dropbox, allowing you to browse SharePoint video files, copy them to Dropbox, and generate direct public download links for use with Metricool and other services.

## Features

### SharePoint Integration (Top Panel)
- 🔐 Authenticate with SharePoint using OAuth2 device flow (MFA supported)
- 📁 Browse folders and files in your SharePoint site
- 🎬 Filter and display MP4 video files
- ⬇️ Copy selected videos to Dropbox with one click

### Dropbox Integration (Bottom Panel)
- 📦 List all MP4 files in specified Dropbox folder
- 🔗 Generate direct download links for each file
- 📋 One-click copy link to clipboard
- 🗑️ Delete files directly from Dropbox
- ✅ Links work with Metricool video upload

## Architecture

### Split-Screen Interface

**Top Half: SharePoint Browser**
- OAuth2 authentication with MFA support
- Folder navigation and file selection
- One-click copy to Dropbox

**Bottom Half: Dropbox File Manager**
- List MP4 files in configured Dropbox folder
- Direct download link generation (no redirects, works with Metricool)
- Delete files with confirmation

### Why Dropbox?

SharePoint's anonymous sharing links use redirects and don't serve video files with proper `Content-Type: video/mp4` headers, which prevents services like Metricool from accepting them. Dropbox provides true direct download URLs that work universally.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# SharePoint Configuration
SHAREPOINT_SITE_URL=https://yourcompany.sharepoint.com/sites/yoursite
SHAREPOINT_START_FOLDER=Shared Documents/Videos

# Dropbox Configuration
DROPBOX_ACCESS_TOKEN=your_dropbox_access_token
DROPBOX_FOLDER=/Public/Videos

# Application Authentication
APP_USERNAME=admin
APP_PASSWORD=your_secure_password

# Optional: Public URL for ngrok/proxy
PUBLIC_URL=
```

### 3. Get Dropbox Access Token

1. Go to [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Create a new app with "Full Dropbox" access
3. Generate an access token
4. Add token to `.env` file

### 4. Development Mode

```bash
python app.py
```

Navigate to `http://localhost:5000` and log in with your configured credentials.

## Deployment to DreamHost

### Prerequisites

- DreamHost account with Python/Passenger support
- SSH access to your DreamHost server
- Domain configured in DreamHost panel

### Deployment Steps

1. **Build for production:**
   ```bash
   # No build step needed for Flask - just upload files
   ```

2. **Upload to DreamHost:**
   ```bash
   # SSH into your DreamHost server
   ssh user@yourserver.dreamhost.com
   
   # Navigate to your web directory
   cd /home/username/yourdomain.com/
   
   # Upload via SFTP or git clone
   git clone https://github.com/robroyaus/VideoBridge.git .
   
   # Install dependencies
   pip3 install -r requirements.txt
   ```

3. **Configure Passenger:**
   
   Create `passenger_wsgi.py` in your domain root:
   ```python
   import sys
   import os
   
   # Add application directory to path
   sys.path.insert(0, os.path.dirname(__file__))
   
   from app import app as application
   ```

4. **Set up .htaccess:**
   
   Create `.htaccess` in your domain root:
   ```apache
   # Basic Authentication
   AuthType Basic
   AuthName "VideoBridge"
   AuthUserFile /home/username/.htpasswd
   Require valid-user
   
   # Passenger Configuration  
   PassengerEnabled On
   PassengerAppRoot /home/username/yourdomain.com
   PassengerPython /usr/bin/python3
   ```

5. **Create .htpasswd file:**
   ```bash
   htpasswd -c ~/.htpasswd admin
   # Enter password when prompted
   ```

6. **Set environment variables:**
   
   Add to `passenger_wsgi.py` before imports:
   ```python
   os.environ['SHAREPOINT_SITE_URL'] = 'your-url'
   os.environ['DROPBOX_ACCESS_TOKEN'] = 'your-token'
   # ... other env vars
   ```

### Testing Deployment

```bash
# Restart Passenger
touch tmp/restart.txt

# Check logs
tail -f logs/error.log
```

## Usage

### Copying Videos from SharePoint to Dropbox

1. Log in with configured credentials
2. Navigate SharePoint folders in top panel
3. Click "Copy to Dropbox" next to desired video
4. Video appears in bottom panel when copy completes

### Generating Metricool Links

1. Find video in Dropbox panel (bottom half)
2. Click "Copy Link" button
3. Paste into Metricool - link works directly with no redirects

### Deleting Videos

1. Click "Delete" button next to video in Dropbox panel
2. Confirm deletion
3. File removed from Dropbox

## Security Notes

- ⚠️ Never commit `.env` file to version control
- 🔒 Basic authentication protects the web interface
- 🔑 Dropbox tokens have full account access - keep secure
- 🌐 Direct download links are public - anyone with link can download
- 🔄 Token cache file (`token_cache.json`) contains sensitive data - gitignored

## Troubleshooting

**SharePoint Authentication Fails:**
- Ensure MFA is configured (uses device code flow)
- Check token_cache.json permissions
- Delete token_cache.json to force re-authentication

**Dropbox Copy Fails:**
- Verify access token has write permissions
- Check Dropbox folder path exists
- Ensure sufficient storage space

**Links Don't Work in Metricool:**
- Verify Dropbox file is in a public folder or has sharing enabled
- Check link format starts with `https://dl.dropboxusercontent.com`

**Passenger Errors on DreamHost:**
- Check `logs/error.log` for Python errors
- Verify Python version: `python3 --version` (need 3.7+)
- Ensure all dependencies installed: `pip3 list`

## Requirements

- Python 3.7+
- SharePoint Online account
- Dropbox account with API access
- DreamHost VPS or shared hosting with Passenger support
