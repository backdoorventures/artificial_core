import streamlit as st
from openai import OpenAI

# STEP 1: Get affiliate product
from generator.affiliate_inserter import get_next_affiliate

# STEP 2: Generate video (script, voiceover, render)
from generator.launchlayer_video.generate import generate_video

# STEP 2.5: Upload to YouTube
from generator.youtube_poster import upload_to_youtube

# STEP 3: Build blog post prompt
from generator.prompt_builder import build_launchlayer_prompt

# STEP 4: Export markdown
from generator.markdown_exporter import export_markdown

# STEP 5: Push to Git
from generator.push_to_git import push_post_to_github

# === Init ===
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.set_page_config(page_title="LaunchLayer: Full Automation", layout="centered")
st.title("🚀 LaunchLayer: Affiliate Video + Blog Automation")

# === Session state ===
for key in ["step1_ready", "step2_ready", "step3_ready", "step4_ready"]:
    if key not in st.session_state:
        st.session_state[key] = False

# === Step 0: Get Affiliate Product ===
if st.button("🎯 Get Next Affiliate Product"):
    product = get_next_affiliate()
    st.session_state.product = product
    st.success(f"✅ Product Loaded: {product['name']}")
    st.markdown(f"- **Name**: {product['name']}\n- **Link**: {product['link']}")
    st.session_state.step1_ready = True

# === Step 1: Manual Keyword Entry + Generate Video ===
if st.session_state.step1_ready:
    keyword = st.text_input("🔑 Enter Keyword for Video + Blog")
    if st.button("🎥 Generate Video from Keyword") and keyword.strip():
        st.session_state.keyword = keyword
        with st.spinner("Generating video..."):
            product = st.session_state.product
            video_path, keyword, title, description = generate_video(
                keyword=keyword,
                background_path="assets/bg.mp4",
                music_path="assets/music.mp3",
                logo_path="assets/logo.png",
                affiliate_link=product["link"]
            )
        if video_path:
            st.session_state.video_path = video_path
            st.session_state.video_title = title
            st.session_state.video_desc = description
            st.video(video_path)
            st.success("✅ Video generated.")
            st.session_state.step2_ready = True
        else:
            st.error("❌ Video generation failed.")

# === Step 2: Upload to YouTube ===
if st.session_state.step2_ready:
    if st.button("📤 Upload to YouTube"):
        try:
            video_id = upload_video_to_youtube(
                file_path=st.session_state.video_path,
                title=st.session_state.video_title,
                description=st.session_state.video_desc
            )
            st.session_state.video_id = video_id
            st.success(f"✅ Uploaded. Video ID: `{video_id}`")
            st.session_state.step3_ready = True
        except Exception as e:
            st.error("❌ Upload failed.")
            st.exception(e)

# === Step 3: Generate Blog Post ===
if st.session_state.step3_ready:
    if st.button("🧠 Generate Blog Post Markdown"):
        prompt = build_launchlayer_prompt(
            keyword=st.session_state.keyword,
            video_id=st.session_state.video_id,
            row={
                "product_name": st.session_state.product["name"],
                "affiliate_link": st.session_state.product["link"],
                "brain": st.session_state.product["brain"]
            }
        )
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            blog_body = response.choices[0].message.content.strip()
            filename, markdown = export_markdown(
                title=st.session_state.keyword.title(),
                body=blog_body,
                tags="launchlayer, ai, automation, affiliate",
                video_id=st.session_state.video_id
            )
            st.session_state.filename = filename
            st.session_state.markdown = markdown
            st.markdown("### 📝 Final Markdown")
            st.code(markdown, language="markdown")
            st.success("✅ Blog post ready.")
            st.session_state.step4_ready = True
        except Exception as e:
            st.error("❌ Blog generation failed.")
            st.exception(e)

# === Step 4: Push to GitHub ===
if st.session_state.step4_ready:
    st.download_button("📥 Download Markdown", st.session_state.markdown, file_name=st.session_state.filename)
    if st.button("🚀 Push to Blog"):
        success, msg = push_post_to_github(st.session_state.filename, st.session_state.markdown)
        st.success(msg if success else f"❌ Push failed: {msg}")











