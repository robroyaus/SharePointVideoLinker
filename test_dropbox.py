#!/usr/bin/python3
import dropbox
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('DROPBOX_ACCESS_TOKEN')
folder = os.getenv('DROPBOX_FOLDER')

print(f"Token: {token[:20]}...")
print(f"Folder: {folder}")

try:
    dbx = dropbox.Dropbox(token)
    account = dbx.users_get_current_account()
    print(f"\n✓ Connected as: {account.name.display_name}")
    
    # Test upload
    test_content = b"Test file content"
    test_path = f"{folder}/test.txt"
    dbx.files_upload(test_content, test_path, mode=dropbox.files.WriteMode.overwrite)
    print(f"✓ Test file uploaded to {test_path}")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
