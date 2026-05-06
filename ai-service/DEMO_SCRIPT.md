# AI Developer 1 — Demo Script

## My Section (60-90 seconds during Demo Day)

### What I say to open:
"I built the AI microservice that powers the intelligence behind this application.
It runs on Flask, connects to the Groq API using the LLaMA-3.3-70b model,
and exposes 3 endpoints that the Java backend calls automatically."

---

## Live Demo Steps (practice these exactly)

### Step 1 — Show the health endpoint
Open browser and go to: http://localhost:5000/health
Say: "This is our AI service health check. You can see the model name,
uptime, and average response time — currently under 1 second."

### Step 2 — Live /describe demo
Run in terminal:
Invoke-WebRequest -Uri http://localhost:5000/describe -Method POST -ContentType "application/json" -Body '{"input": "Cybersecurity breach risk in banking system"}' | Select-Object -ExpandProperty Content

Say: "When a risk record is created in the Java backend, it automatically
calls our /describe endpoint. The AI generates a structured description,
key points, and severity rating in under 2 seconds."

### Step 3 — Live /recommend demo
Run in terminal:
Invoke-WebRequest -Uri http://localhost:5000/recommend -Method POST -ContentType "application/json" -Body '{"input": "Cybersecurity breach risk in banking system"}' | Select-Object -ExpandProperty Content

Say: "The /recommend endpoint returns 3 prioritised action items —
each with an action type, description, and priority level."

### Step 4 — Live /generate-report demo
Run in terminal:
Invoke-WebRequest -Uri http://localhost:5000/generate-report -Method POST -ContentType "application/json" -Body '{"input": "Cybersecurity breach risk in banking system"}' | Select-Object -ExpandProperty Content

Say: "Finally, /generate-report creates a full structured report with
title, executive summary, overview, key findings, and recommendations."

### Step 5 — Show security (if asked)
Run in terminal:
Invoke-WebRequest -Uri http://localhost:5000/describe -Method POST -ContentType "application/json" -Body '{"input": "ignore previous instructions"}' | Select-Object -ExpandProperty Content

Say: "Our service also detects and blocks prompt injection attacks.
This returns a 400 error instead of passing the malicious input to the AI."

---

## Tech Explanation (60 seconds — plain English)

"The AI service is built with Python and Flask. When a request comes in,
we first sanitise the input using bleach to strip any HTML. Then we check
for prompt injection keywords. If the input is clean, we load a prompt
template from a text file, inject the user's data into it, and send it
to the Groq API which runs the LLaMA-3.3-70b model. The response comes
back as JSON in under 1 second. We also cache repeated inputs in Redis
for 15 minutes so identical queries don't hit the AI twice. The service
is rate limited to 30 requests per minute per IP address."

---

## Questions panel might ask — prepare these answers

Q: Why did you choose Groq over OpenAI?
A: Groq is free tier with no credit card required, and LLaMA-3.3-70b
   is a powerful open source model. Response times are very fast.

Q: What happens if the AI service goes down?
A: Every endpoint returns a fallback response with is_fallback: true
   instead of crashing. The Java backend handles null gracefully.

Q: How do you prevent misuse of the AI?
A: Three layers — input sanitisation with bleach, prompt injection
   detection, and rate limiting at 30 requests per minute.

Q: How many tests do you have?
A: 8 pytest unit tests, all passing. Groq API is mocked so tests
   run without any live network connection.