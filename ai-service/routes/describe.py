from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
from datetime import datetime, timezone
import json
import bleach

describe_bp = Blueprint("describe", __name__)

@describe_bp.route("/describe", methods=["POST"])
def describe():
    data = request.get_json()

    if not data or "input" not in data:
        return jsonify({"error": "input field is required"}), 400

    clean_input = bleach.clean(str(data["input"]), strip=True)

    if not clean_input.strip():
        return jsonify({"error": "input cannot be empty"}), 400

    with open("prompts/describe_prompt.txt") as f:
        template = f.read()

    prompt = template.replace("{input_data}", clean_input)
    prompt = prompt.replace("{generated_at}", datetime.now(timezone.utc).isoformat())

    result = call_groq(prompt)

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