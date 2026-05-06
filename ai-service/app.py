from flask import Flask, request, jsonify
from dotenv import load_dotenv
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp
from services.groq_client import get_avg_response_time, call_groq
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

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
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
    return response

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model": "llama-3.3-70b-versatile",
        "uptime_seconds": int(time.time() - START_TIME),
        "avg_response_time_seconds": get_avg_response_time()
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "method not allowed"}), 405

@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({"error": "rate limit exceeded, try again later"}), 429

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)