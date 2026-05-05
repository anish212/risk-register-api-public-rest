from groq import Groq
from dotenv import load_dotenv
import os
import time
import logging

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
            logging.info(f"Groq response time: {elapsed:.2f}s")
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Groq call failed attempt {attempt+1}: {e}")
    return None