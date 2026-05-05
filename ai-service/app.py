from flask import Flask, request, jsonify
from dotenv import load_dotenv
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
import os

load_dotenv()

app = Flask(__name__)

START_TIME = time.time()

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    storage_uri="memory://"
)

app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)

@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

@app.route("/health")
def health():
    return {
        "status": "ok",
        "model": "llama-3.3-70b-versatile",
        "uptime_seconds": int(time.time() - START_TIME)
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)