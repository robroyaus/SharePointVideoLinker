# Using ngrok for Public Access

To make your video links accessible to Metricool (or other external services), you need to expose your local Flask server to the internet using ngrok.

## Steps

### 1. Start Flask (in Terminal Tab 1)
```bash
python app.py
```

Wait for Flask to start and complete authentication if needed.

### 2. Start ngrok (in Terminal Tab 2)
```bash
ngrok http 5000
```

This will output something like:
```
Forwarding   https://xxxx-xx-xx-xxx-xxx.ngrok-free.app -> http://localhost:5000
```

### 3. Set the Public URL (in Terminal Tab 3)
Copy the ngrok HTTPS URL (the one ending in `.ngrok-free.app`) and set it as an environment variable:

```bash
export PUBLIC_URL=https://xxxx-xx-xx-xxx-xxx.ngrok-free.app
```

Then restart Flask in Tab 1 (Ctrl+C and run `python app.py` again).

### 4. Generate Video Links

Now when you generate video links in the web interface, the "Proxy URL" will use your ngrok URL, making it accessible to Metricool.

## Important Notes

- **Keep both Flask and ngrok running** while using the service
- The ngrok URL changes each time you restart ngrok (unless you have a paid account)
- The PUBLIC_URL environment variable needs to be set before starting Flask
- Free ngrok accounts have rate limits and session timeouts

## Alternative: One-Command Start

You can set the PUBLIC_URL and start Flask in one command:

```bash
PUBLIC_URL=https://your-ngrok-url.ngrok-free.app python app.py
```

Just replace `your-ngrok-url` with your actual ngrok URL after starting ngrok.
