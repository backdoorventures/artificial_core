import base64
import requests
from datetime import datetime
import streamlit as st

def push_post_to_github(filename: str, markdown_content: str, path_prefix: str = "content/blog/"):
    token = st.secrets["GITHUB_TOKEN"]
    repo = st.secrets["GITHUB_REPO"]
    branch = st.secrets.get("GITHUB_BRANCH", "main")

    path = f"{path_prefix}{filename}"
    url = f"https://api.github.com/repos/{repo}/contents/{path}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Check for existing file
    sha = None
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        sha = r.json().get("sha")

    # Push
    payload = {
        "message": f"📝 Add post: {filename} ({now})",
        "content": base64.b64encode(markdown_content.encode()).decode(),
        "branch": branch
    }
    if sha:
        payload["sha"] = sha

    r = requests.put(url, headers=headers, json=payload)
    if r.status_code in [200, 201]:
        return True, f"Pushed: {filename}"
    return False, f"GitHub error: {r.status_code} — {r.text}"


