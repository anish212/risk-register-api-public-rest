import pytest
import json
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

MOCK_DESCRIBE = json.dumps({
    "description": "Test risk description",
    "key_points": ["point 1", "point 2", "point 3"],
    "severity": "high",
    "generated_at": "2026-05-05T00:00:00+00:00"
})

MOCK_RECOMMEND = json.dumps([
    {"action_type": "Mitigation", "description": "Test action 1", "priority": "high"},
    {"action_type": "Monitoring", "description": "Test action 2", "priority": "medium"},
    {"action_type": "Review", "description": "Test action 3", "priority": "low"}
])

MOCK_REPORT = json.dumps({
    "title": "Test Report",
    "summary": "Test summary",
    "overview": "Test overview",
    "key_items": ["item 1", "item 2", "item 3"],
    "recommendations": ["rec 1", "rec 2", "rec 3"]
})

# Test 1 - Health endpoint returns 200
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "ok"
    assert "uptime_seconds" in data

# Test 2 - Describe returns 400 when no input
def test_describe_missing_input(client):
    response = client.post("/describe",
        data=json.dumps({}),
        content_type="application/json")
    assert response.status_code == 400

# Test 3 - Describe returns 400 when empty body
def test_describe_empty_body(client):
    response = client.post("/describe",
        data=json.dumps({"input": ""}),
        content_type="application/json")
    assert response.status_code == 400

# Test 4 - Describe returns 200 with valid input
@patch("services.groq_client.call_groq", return_value=MOCK_DESCRIBE)
def test_describe_success(mock_groq, client):
    response = client.post("/describe",
        data=json.dumps({"input": "Server downtime risk"}),
        content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "description" in data

# Test 5 - Describe handles Groq failure gracefully
@patch("routes.describe.call_groq", return_value=None)
def test_describe_groq_failure(mock_groq, client):
    response = client.post("/describe",
        data=json.dumps({"input": "Server downtime risk"}),
        content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["is_fallback"] == True

# Test 6 - Recommend returns 200 with valid input
@patch("services.groq_client.call_groq", return_value=MOCK_RECOMMEND)
def test_recommend_success(mock_groq, client):
    response = client.post("/recommend",
        data=json.dumps({"input": "Database failure risk"}),
        content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 3

# Test 7 - Recommend returns 400 when no input
def test_recommend_missing_input(client):
    response = client.post("/recommend",
        data=json.dumps({}),
        content_type="application/json")
    assert response.status_code == 400

# Test 8 - Generate report returns 200 with valid input
@patch("services.groq_client.call_groq", return_value=MOCK_REPORT)
def test_report_success(mock_groq, client):
    response = client.post("/generate-report",
        data=json.dumps({"input": "Cybersecurity breach risk"}),
        content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "title" in data
    assert "recommendations" in data