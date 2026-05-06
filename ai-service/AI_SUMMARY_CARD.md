# AI Service — Summary Card
## Tool-101 | Demo Day May 9 2026

---

## 3 Endpoints

| Endpoint | Method | What It Does |
|----------|--------|--------------|
| /describe | POST | Generates structured risk description with severity |
| /recommend | POST | Returns 3 prioritised action recommendations |
| /generate-report | POST | Creates full risk report with title, summary, findings |

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.13 | Language |
| Flask 3.x | Web framework |
| Groq API | LLaMA-3.3-70b AI model |
| Redis | Response caching (15 min TTL) |
| flask-limiter | Rate limiting (30 req/min) |
| bleach | Input sanitisation |
| pytest | 8 unit tests, all passing |

---

## Security Features

- Prompt injection detection — blocks malicious inputs
- Input sanitisation — strips HTML via bleach
- Rate limiting — 30 requests per minute per IP
- Security headers — X-Content-Type-Options, X-Frame-Options, CSP, Referrer-Policy, X-XSS-Protection
- No secrets in code — all via .env file

---

## Performance

- Average response time: under 1 second
- Redis caching: repeated inputs served instantly
- Fallback template: returns is_fallback:true if Groq fails
- Rate limit: 429 returned after 30 requests/minute

---

## GitHub

https://github.com/anish212/risk-register-api-public-rest/tree/anish-ai-developer-1

## Developer

Anish | AI Developer 1