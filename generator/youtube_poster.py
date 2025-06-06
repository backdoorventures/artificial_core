import os
import pickle
import base64
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def load_token():
    # Try Streamlit secrets first
    try:
        import streamlit as st
        encoded = st.secrets["YOUTUBE_TOKEN"]
    except:
        encoded = os.getenv("YOUTUBE_TOKEN")

    with open("token.pickle", "wb") as f:
        f.write(base64.b64decode(encoded))

def upload_to_youtube(video_path, title, description, tags=None, privacy="public"):
    load_token()

    with open("token.pickle", "rb") as token_file:
        creds = pickle.load(token_file)

    youtube = build("youtube", "v3", credentials=creds)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": "22"  # People & Blogs
            },
            "status": {
                "privacyStatus": privacy
            }
        },
        media_body=MediaFileUpload(video_path, resumable=True)
    )

    response = None
    while response is None:
        _, response = request.next_chunk()

    return f"https://youtube.com/watch?v={response['id']}"
