import streamlit as st
from utils.get_next_affiliate import get_next_affiliate
from utils.video_generator import generate_launchlayer_video
from utils.youtube_poster import upload_to_youtube
from utils.blog_prompt_builder import build_launchlayer_prompt
from utils.markdown_exporter import build_markdown_file
from utils.push_to_git import push_post_to_github

# === UI ===
st.title("🚀 LaunchLayer AI Bot: Full Content System")

# Step 1 — Get affiliate product data
if st.button("📦 STEP 1: Load Affiliate Product"):
    product = get_next_affiliate()
    st.session_state.product = product
    st.success(f"Loaded: {product['name']}")
    st.json(product)

# Step 2 — Input manual keyword/title
if "product" in st.session_state:
    title = st.text_input("✍️ Enter Video Title / Keyword", key="video_title")
    if title:
        st.session_state.title = title

# Step 3 — Generate video (requires product + title)
if "title" in st.session_state and st.button("🎥 STEP 2: Generate Video"):
    video_path, script_text = generate_launchlayer_video(
        keyword=st.session_state.title,
        brain_text=st.session_state.product["brain"]
    )
    st.session_state.video_path = video_path
    st.session_state.script_text = script_text
    st.success("Video rendered.")
    st.video(video_path)
    st.code(script_text)

# Step 4 — Upload to YouTube
if "video_path" in st.session_state and st.button("☁️ STEP 3: Upload to YouTube"):
    video_id = upload_to_youtube(
        title=st.session_state.title,
        description_script=st.session_state.script_text,
        keyword=st.session_state.title,
        product=st.session_state.product
    )
    st.session_state.video_id = video_id
    st.success(f"Uploaded: https://www.youtube.com/watch?v={video_id}")
    st.markdown(f"[View on YouTube](https://www.youtube.com/watch?v={video_id})")

# Step 5 — Generate Markdown blog post
if "video_id" in st.session_state and st.button("📝 STEP 4: Generate Markdown"):
    md_text, filename = build_markdown_file(
        title=st.session_state.title,
        video_id=st.session_state.video_id,
        script_text=st.session_state.script_text,
        product=st.session_state.product
    )
    st.session_state.markdown = md_text
    st.session_state.filename = filename
    st.success("Markdown file generated.")
    st.code(md_text, language="markdown")

# Step 6 — Push to GitHub
if "markdown" in st.session_state and st.button("🚀 FINAL STEP: Push to GitHub"):
    success, msg = push_post_to_github(
        filename=st.session_state.filename,
        markdown_content=st.session_state.markdown
    )
    if success:
        st.success(msg)
    else:
        st.error(msg)
