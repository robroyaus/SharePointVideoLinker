#!/usr/bin/python3
import os
import msal
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = "14d82eec-204b-4c2f-b7e8-296a70dab67e"
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPES = ["Files.ReadWrite.All", "Sites.ReadWrite.All", "User.Read"]
TOKEN_CACHE_FILE = "token_cache.json"

cache = msal.SerializableTokenCache()
app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

flow = app.initiate_device_flow(scopes=SCOPES)
if "user_code" not in flow:
    raise Exception("Failed to create device flow")

print(flow["message"])
input("Press Enter after authenticating...")

result = app.acquire_token_by_device_flow(flow)
if "access_token" in result:
    with open(TOKEN_CACHE_FILE, 'w') as f:
        f.write(cache.serialize())
    print("\n✓ Authentication successful! Token cached.")
else:
    print(f"\n✗ Authentication failed: {result.get('error_description')}")
