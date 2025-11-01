import sys
import os

# Add application directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Import Flask application
from app import app as application

# For debugging
application.debug = False
