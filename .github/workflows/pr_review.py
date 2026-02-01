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

url = f"{endpoint}/openai/deployments/{deployment}/responses?api-version=2024-02-15-preview"

headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

payload = {
    "input": [
        {
            "role": "system",
            "content": [
                { "type": "text", "text": "You are a code reviewer. Check only syntax errors." }
            ]
        },
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "def add(a, b)\n return a + b" }
            ]
        }
    ]
}

response = requests.post(url, headers=headers, json=payload)

print("🔹 Status Code:", response.status_code)
print("🔹 Raw Response:")
print(response.text)

if response.status_code != 200:
    print("❌ Azure OpenAI error")
    sys.exit(1)

try:
    data = response.json()
except Exception as e:
    print("❌ JSON parse failed:", e)
    sys.exit(1)

review = data["output"][0]["content"][0]["text"]
print("✅ AI Review:")
print(review)
