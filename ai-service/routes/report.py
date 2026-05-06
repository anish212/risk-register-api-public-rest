from flask import Blueprint, request, jsonify
from services.groq_client import call_groq_cached, is_injection
from datetime import datetime, timezone
import json
import bleach

report_bp = Blueprint("report", __name__)

@report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.get_json()

    if not data or "input" not in data:
        return jsonify({"error": "input field is required"}), 400

    clean_input = bleach.clean(str(data["input"]), strip=True)

    if not clean_input.strip():
        return jsonify({"error": "input cannot be empty"}), 400

    if is_injection(clean_input):
        return jsonify({"error": "invalid input detected"}), 400

    with open("prompts/report_prompt.txt") as f:
        template = f.read()

    prompt = template.replace("{input_data}", clean_input)

    result = call_groq_cached(prompt, temperature=0.5)

    if result is None:
        return jsonify({
            "error": "AI service unavailable",
            "is_fallback": True,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }), 200

    try:
        return jsonify(json.loads(result))
    except:
        return jsonify({
            "raw": result,
            "generated_at": datetime.now(timezone.utc).isoformat()
        })