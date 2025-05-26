import base64
import requests
from datetime import datetime
import streamlit as st

def push_post_to_github(filename: str, markdown_content: str):
    """
    Pushes a markdown blog post to the `content/posts/` directory
    in the artificial_site GitHub repo using GitHub API.
    """
    # Load secrets
    token = st.secrets["GITHUB_TOKEN"]
    repo = st.secrets["GITHUB_REPO"]  # e.g., backdoorventures/artificial_site
    branch = st.secrets.get("GITHUB_BRANCH", "main")

    # Build API URL
    path = f"content/posts/{filename}"
    api_url = f"https://api.github.com/repos/{repo}/contents/{path}"

    # Check if file exists to get the SHA (needed for update)
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    sha = None
    r = requests.get(api_url, headers=headers)
    if r.status_code == 200:
        sha = r.json()["sha"]

    # Prepare payload
    encoded_content = base64.b64encode(markdown_content.encode("utf-8")).decode("utf-8")
    commit_message = f"Add new blog post: {filename}"

    payload = {
        "message": commit_message,
        "content": encoded_content,
        "branch": branch
    }

    if sha:
        payload["sha"] = sha  # Required for updating existing files

    # Push to GitHub
    response = requests.put(api_url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        return True, f"✅ Successfully pushed `{filename}` to `{repo}`"
    else:
        return False, f"❌ Failed to push. Status: {response.status_code}, Message: {response.text}"
