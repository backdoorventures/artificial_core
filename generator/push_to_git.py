import base64
import requests
from datetime import datetime
import streamlit as st

def push_post_to_github(filename: str, markdown_content: str):
    """
    Pushes a markdown blog post to the `content/posts/` directory
    in the artificial_site GitHub repo using GitHub API.
    """
    # Load from secrets
    token = st.secrets["GITHUB_TOKEN"]
    repo = st.secrets["GITHUB_REPO"]
    branch = st.secrets.get("GITHUB_BRANCH", "main")

    path = f"content/posts/{filename}"
    api_url = f"https://api.github.com/repos/{repo}/contents/{path}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    # Optional: fallback commit timestamp
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Check for existing file (get SHA for overwrite)
    sha = None
    try:
        check = requests.get(api_url, headers=headers)
        if check.status_code == 200:
            sha = check.json().get("sha")
    except Exception as e:
        return False, f"❌ Error checking file existence: {e}"

    # Encode content
    encoded_content = base64.b64encode(markdown_content.encode("utf-8")).decode("utf-8")

    # Build commit payload
    payload = {
        "message": f"📝 Add post: {filename} ({now})",
        "content": encoded_content,
        "branch": branch
    }
    if sha:
        payload["sha"] = sha  # Required to update existing file

    # Push file to GitHub
    try:
        response = requests.put(api_url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            return True, f"✅ Successfully pushed `{filename}` to `{repo}` on `{branch}`"
        else:
            return False, f"❌ GitHub API error: {response.status_code} — {response.text}"
    except Exception as e:
        return False, f"❌ Push failed: {e}"

