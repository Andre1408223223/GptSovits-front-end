from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

API_URL = os.getenv("API_URL", "http://gpt-sovits-api:9880")

@app.route("/")
def index():
    try:
        r = requests.get(f"{API_URL}/status")
        status = r.json().get("status", "unknown")
    except Exception as e:
        status = f"error: {e}"

    return f"API status: {status}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
