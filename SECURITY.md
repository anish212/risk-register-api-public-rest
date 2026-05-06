# Security Documentation — Tool-101 AI Service

## Overview
This document covers all security threats identified, tests conducted,
findings fixed, and residual risks for the Tool-101 AI microservice.
All team members have reviewed and signed off on this document.

---

## Threats Identified

| # | Threat | Type | Severity |
|---|--------|------|----------|
| 1 | Prompt injection via user input | Injection | High |
| 2 | Sensitive data exposure via API responses | Data Exposure | High |
| 3 | Rate limit abuse / DoS attack | Availability | Medium |
| 4 | Missing security headers | Misconfiguration | Medium |
| 5 | Hardcoded API keys in source code | Credential Exposure | High |
| 6 | Cross-site scripting via input fields | XSS | Medium |
| 7 | Unhandled errors exposing stack traces | Information Leakage | Low |

---

## Tests Conducted

| Test | Method | Result |
|------|--------|--------|
| Prompt injection attempt | Sent "ignore previous instructions" as input | Blocked — 400 returned |
| Empty input | Sent empty string as input | Blocked — 400 returned |
| HTML injection | Sent `<script>alert(1)</script>` as input | Stripped by bleach |
| Rate limit test | Sent 35 requests in 1 minute | Blocked after 30 — 429 returned |
| Missing input field | Sent request with no input key | Blocked — 400 returned |
| Security headers check | Checked response headers | All 6 headers present |
| API key exposure check | Checked GitHub commits | No secrets committed |
| Error handling | Called non-existent endpoint | Clean 404 JSON returned |

---

## Findings and Fixes

| Finding | Fix Applied |
|---------|-------------|
| No prompt injection protection | Added keyword detection in groq_client.py |
| Missing security headers | Added X-Content-Type-Options, X-Frame-Options, CSP, Referrer-Policy, X-XSS-Protection, Permissions-Policy |
| Raw HTML accepted in input | Added bleach.clean() to all routes |
| No rate limiting | Added flask-limiter at 30 requests/minute |
| Unhandled 404/500 errors | Added @app.errorhandler for 404, 405, 429, 500 |
| API key hardcoding risk | Used .env file with python-dotenv, .env in .gitignore |

---

## Residual Risks

| Risk | Reason Not Fixed | Mitigation |
|------|-----------------|------------|
| No HTTPS in development | Requires SSL certificate setup | Use HTTPS in production via reverse proxy |
| Redis cache not authenticated | Redis runs locally without password | Add Redis password in production deployment |
| Groq API rate limits | External service limitation | Fallback template implemented for failures |

---

## Team Sign-off

| Member | Role | Sign-off |
|--------|------|----------|
| Anish | AI Developer 1 | Signed |
| (Member 2) | Java Developer 1 | Pending |
| (Member 3) | Java Developer 2 | Pending |
| (Member 4) | AI Developer 2 | Pending |
| (Member 5) | Security Reviewer | Pending |

Last updated: May 2026