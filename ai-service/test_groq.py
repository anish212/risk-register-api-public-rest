from services.groq_client import call_groq

result = call_groq("Say hello in one sentence")
print(result)