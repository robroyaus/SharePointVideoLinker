from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
import os
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Configuration - you'll need to set these
SHAREPOINT_SITE_URL = os.getenv('SHAREPOINT_SITE_URL', '')
USERNAME = os.getenv('SHAREPOINT_USERNAME', '')
PASSWORD = os.getenv('SHAREPOINT_PASSWORD', '')


def get_sharepoint_context():
    """Create and return authenticated SharePoint context"""
    if not SHAREPOINT_SITE_URL or not USERNAME or not PASSWORD:
        return None
    
    ctx_auth = AuthenticationContext(SHAREPOINT_SITE_URL)
    if ctx_auth.acquire_token_for_user(USERNAME, PASSWORD):
        ctx = ClientContext(SHAREPOINT_SITE_URL, ctx_auth)
        return ctx
    return None


@app.route('/')
def index():
    """Home page"""
    if not SHAREPOINT_SITE_URL or not USERNAME:
        return render_template('setup.html')
    return render_template('index.html')


@app.route('/browse')
def browse():
    """Browse SharePoint folders and files"""
    folder_path = request.args.get('path', 'Shared Documents')
    
    try:
        ctx = get_sharepoint_context()
        if not ctx:
            return jsonify({'error': 'Authentication failed'}), 401
        
        # Get folder
        folder = ctx.web.get_folder_by_server_relative_url(folder_path)
        
        # Get subfolders
        folders = folder.folders
        ctx.load(folders)
        
        # Get files
        files = folder.files
        ctx.load(files)
        
        ctx.execute_query()
        
        items = []
        
        # Add folders
        for subfolder in folders:
            if subfolder.properties.get('Name') not in ['Forms']:
                items.append({
                    'name': subfolder.properties.get('Name'),
                    'type': 'folder',
                    'path': subfolder.properties.get('ServerRelativeUrl')
                })
        
        # Add MP4 files
        for file in files:
            filename = file.properties.get('Name', '')
            if filename.lower().endswith('.mp4'):
                items.append({
                    'name': filename,
                    'type': 'file',
                    'path': file.properties.get('ServerRelativeUrl'),
                    'size': file.properties.get('Length', 0)
                })
        
        return jsonify({
            'current_path': folder_path,
            'items': items
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate-link', methods=['POST'])
def generate_link():
    """Generate a public direct download link for an MP4 file"""
    data = request.get_json()
    file_path = data.get('file_path')
    
    if not file_path:
        return jsonify({'error': 'No file path provided'}), 400
    
    try:
        ctx = get_sharepoint_context()
        if not ctx:
            return jsonify({'error': 'Authentication failed'}), 401
        
        # Get the file
        file = ctx.web.get_file_by_server_relative_url(file_path)
        ctx.load(file)
        ctx.execute_query()
        
        # Create anonymous sharing link with direct download
        # Using create_anonymous_link with is_edit_link=False for read-only access
        link_result = file.share_link(
            kind=4,  # Anonymous link
            expiration=datetime.now() + timedelta(days=365)
        )
        ctx.execute_query()
        
        sharing_url = link_result.value.sharingLinkInfo.Url
        
        # Convert to direct download link
        # SharePoint links need to be modified to be direct download
        if 'sharepoint.com' in sharing_url:
            # Replace the sharing URL format with direct download format
            direct_url = sharing_url.replace('/:v:/g/', '/download?')
            if '?download=1' not in direct_url:
                direct_url = direct_url.split('?')[0] + '?download=1'
        else:
            direct_url = sharing_url
        
        return jsonify({
            'success': True,
            'direct_url': direct_url,
            'sharing_url': sharing_url
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/test-connection', methods=['POST'])
def test_connection():
    """Test SharePoint connection"""
    try:
        ctx = get_sharepoint_context()
        if ctx:
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()
            return jsonify({
                'success': True,
                'site_title': web.properties.get('Title', 'Connected')
            })
        return jsonify({'error': 'Authentication failed'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
