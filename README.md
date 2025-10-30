# SharePoint Video Linker

A local web application that authenticates with SharePoint, allows you to browse folders and MP4 files, and generates public direct download links suitable for use with Metricool and other services.

## Features

- 🔐 Authenticate with SharePoint/OneDrive
- 📁 Browse folders and files in your SharePoint site
- 🎬 Filter and display MP4 video files
- 🔗 Generate anonymous public direct download links
- 📋 One-click copy to clipboard
- ✅ Links work with Metricool video upload

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure credentials:**
   
   Create a `.env` file in the project root:
   ```
   SHAREPOINT_SITE_URL=https://yourcompany.sharepoint.com/sites/yoursite
   SHAREPOINT_USERNAME=your.email@company.com
   SHAREPOINT_PASSWORD=your-password
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   Navigate to `http://localhost:5000`

## Usage

1. The app will automatically connect to your SharePoint site
2. Browse through folders by clicking on them
3. Find your MP4 video file
4. Click "Generate Link" next to the video
5. Copy the generated direct download link
6. Paste into Metricool or any other service

## How It Works

The application:
1. Authenticates using your SharePoint credentials
2. Creates anonymous sharing links for selected files
3. Converts SharePoint sharing URLs to direct download format
4. Provides links that work without authentication

## Security Notes

- Never commit your `.env` file to version control
- Add `.env` to your `.gitignore`
- The generated links are public - anyone with the link can download the video
- Links expire after 365 days by default (can be modified in `app.py`)

## Troubleshooting

**Authentication fails:**
- Verify your SharePoint site URL is correct
- Check username and password
- Ensure your account has access to the SharePoint site

**Can't browse folders:**
- Verify the folder path exists
- Check you have read permissions on the SharePoint site

**Generated link doesn't work:**
- Some SharePoint configurations may block anonymous sharing
- Contact your SharePoint administrator to enable anonymous sharing links

## Requirements

- Python 3.7+
- SharePoint Online account with appropriate permissions
- SharePoint site with anonymous sharing enabled
