from groq import Groq
from dotenv import load_dotenv
import os
import time
import logging
import hashlib

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response_times = []

def call_groq(prompt: str, temperature=0.3) -> str:
    for attempt in range(3):
        try:
            start = time.time()
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=temperature
            )
            elapsed = time.time() - start
            response_times.append(elapsed)
            logging.info(f"Groq response time: {elapsed:.2f}s")
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Groq call failed attempt {attempt+1}: {e}")
    return None

def call_groq_cached(prompt: str, temperature=0.3) -> str:
    try:
        import redis
        r = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=6379,
            decode_responses=True,
            socket_connect_timeout=2
        )
        key = "ai:" + hashlib.sha256(prompt.encode()).hexdigest()
        cached = r.get(key)
        if cached:
            logging.info("Cache hit")
            return cached
        result = call_groq(prompt, temperature)
        if result:
            r.setex(key, 900, result)
        return result
    except Exception as e:
        logging.warning(f"Redis unavailable, calling Groq directly: {e}")
        return call_groq(prompt, temperature)

def get_avg_response_time():
    if not response_times:
        return 0
    return round(sum(response_times) / len(response_times), 2)