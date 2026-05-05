from flask import Flask
from dotenv import load_dotenv
from routes.describe import describe_bp
from routes.recommend import recommend_bp
import time
import os

load_dotenv()

app = Flask(__name__)

START_TIME = time.time()

app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)

@app.route("/health")
def health():
    return {
        "status": "ok",
        "model": "llama-3.3-70b-versatile",
        "uptime_seconds": int(time.time() - START_TIME)
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)