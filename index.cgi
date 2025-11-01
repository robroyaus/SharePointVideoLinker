#!/usr/bin/python3
import sys
import os

# Add directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Import app
from app import app
from wsgiref.handlers import CGIHandler

# Run the app
CGIHandler().run(app)
