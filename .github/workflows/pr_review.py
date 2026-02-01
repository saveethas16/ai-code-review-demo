import os
import requests

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_KEY"]
deployment = os.environ["DEPLOYMENT_NAME"]

repo = os.environ["REPO"]
pr_number = os.environ["PR_NUMBER"]
github_token = os.environ["GITHUB_TOKEN"]

headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

prompt = """
You are a senior code reviewer.
Review this pull request and give:
- Code quality feedback
- Possible bugs
- Improvement suggestions
"""

body = {
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.2
}

url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2024-02-15-preview"
response = requests.post(url, headers=headers, json=body)
review = response.json()["choices"][0]["message"]["content"]

comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
gh_headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github+json"
}

requests.post(comment_url, headers=gh_headers, json={"body": review})
