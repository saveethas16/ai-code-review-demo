import os
import requests
import json
import sys

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_KEY")
deployment = os.getenv("DEPLOYMENT_NAME")

if not endpoint or not api_key or not deployment:
    print("❌ Missing environment variables")
    sys.exit(1)

url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2024-02-15-preview"

headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

payload = {
    "messages": [
        {
            "role": "system",
            "content": "You are a code reviewer. Check only syntax errors."
        },
        {
            "role": "user",
            "content": "def add(a, b)\n return a + b"
        }
    ],
    "temperature": 0
}

response = requests.post(url, headers=headers, json=payload)

print("🔹 Status Code:", response.status_code)
print("🔹 Raw Response:")
print(response.text)

# SAFETY CHECK
if response.status_code != 200:
    print("❌ Azure OpenAI error")
    sys.exit(1)

try:
    data = response.json()
except Exception as e:
    print("❌ Failed to parse JSON:", e)
    sys.exit(1)

review = data["choices"][0]["message"]["content"]
print("✅ AI Review:")
print(review)
