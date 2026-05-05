# AI Service — Tool-101

A Flask-based AI microservice that provides risk analysis capabilities
using the Groq API (LLaMA-3.3-70b model).

---

## Prerequisites

- Python 3.11 or higher
- A Groq API key (free at https://console.groq.com)
- Redis (optional — service works without it, caching is skipped)

---

## Setup Steps

### 1. Clone the repository
git clone https://github.com/anish212/risk-register-api-public-rest.git
cd risk-register-api-public-rest/ai-service

### 2. Install dependencies
pip install -r requirements.txt

### 3. Create your .env file
Create a file called .env inside the ai-service folder:
GROQ_API_KEY=your_groq_api_key_here
REDIS_HOST=localhost

### 4. Run the service
python app.py

The service will start on http://localhost:5000

---

## Environment Variables

| Variable      | Required | Description                        |
|---------------|----------|------------------------------------|
| GROQ_API_KEY  | Yes      | Your Groq API key from console.groq.com |
| REDIS_HOST    | No       | Redis host (default: localhost)    |

---

## API Reference

### GET /health
Returns the health status of the AI service.

**Response:**
```json
{
  "status": "ok",
  "model": "llama-3.3-70b-versatile",
  "uptime_seconds": 120,
  "avg_response_time_seconds": 0.9
}
```

---

### POST /describe
Generates a structured description of a risk.

**Request:**
```json
{
  "input": "Server downtime risk in production environment"
}
```

**Response:**
```json
{
  "description": "The server downtime risk refers to...",
  "key_points": ["point 1", "point 2", "point 3"],
  "severity": "high",
  "generated_at": "2026-05-05T12:00:00+00:00"
}
```

---

### POST /recommend
Returns 3 actionable recommendations for a given risk.

**Request:**
```json
{
  "input": "Database failure risk in payment system"
}
```

**Response:**
```json
[
  {"action_type": "Mitigation", "description": "...", "priority": "high"},
  {"action_type": "Monitoring", "description": "...", "priority": "medium"},
  {"action_type": "Review", "description": "...", "priority": "low"}
]
```

---

### POST /generate-report
Generates a full structured risk report.

**Request:**
```json
{
  "input": "Cybersecurity breach risk in banking application"
}
```

**Response:**
```json
{
  "title": "Cybersecurity Breach Risk Report",
  "summary": "Executive summary...",
  "overview": "Detailed overview...",
  "key_items": ["item 1", "item 2", "item 3"],
  "recommendations": ["rec 1", "rec 2", "rec 3"]
}
```

---

## Running Tests

pytest tests/test_endpoints.py -v

All 8 tests should pass without needing a live Groq API connection.

---

## Tech Stack

| Technology     | Purpose                        |
|----------------|-------------------------------|
| Python 3.11+   | Language                      |
| Flask 3.x      | Web framework                 |
| Groq API       | LLaMA-3.3-70b AI model        |
| Redis          | Response caching (15 min TTL) |
| flask-limiter  | Rate limiting (30 req/min)    |
| pytest         | Unit testing                  |