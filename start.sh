#!/bin/bash

# Start Flask in the background
python app.py &
FLASK_PID=$!

# Wait for Flask to start
echo "Waiting for Flask to start..."
sleep 3

# Start ngrok
echo "Starting ngrok tunnel..."
ngrok http 5000

# Clean up Flask when ngrok exits
kill $FLASK_PID
