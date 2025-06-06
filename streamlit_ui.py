import streamlit as st
from openai import OpenAI
from generator.affiliate_inserter import get_next_affiliate
from generator.prompt_builder import build_launchlayer_prompt
from generator.launchlayer_video.generate.description_builder import generate_description
from generator.markdown_exporter import export_markdown
from generator.push_to_git import push_post_to_github

# === Init ===
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.set_page_config(page_title="LaunchLayer Blog Builder", layout="centered")
st.title("🚀 LaunchLayer: SEO Blog & Video Builder")

# === Session state for approvals ===
for key in ["step1_ready", "step2_ready", "step3_ready"]:
    if key not in st.session_state:
        st.session_state[key] = False

# === STEP 0: Manual Keyword Entry + Bot Fetch ===
keyword = st.text_input("🎯 Enter Video Title / Keyword")

if st.button("🧠 Fetch Product + Start Generation") and keyword.strip():
    product = get_next_affiliate()
    st.session_state.product = product

    prompt = build_launchlayer_prompt(
        keyword=keyword,
        video_id="TO_BE_INSERTED",
        row={
            "product_name": product["product_name"],
            "affiliate_link": product["affiliate_link"],
            "brain": product["brain"]
        }
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        st.session_state.script = response.choices[0].message.content.strip()
        st.session_state.keyword = keyword
        st.success("✅ Script generated. Review & approve below.")
        st.session_state.step1_ready = True
    except Exception as e:
        st.error("❌ Failed to generate script.")
        st.exception(e)

# === STEP 1: Script Approval ===
if st.session_state.step1_ready:
    st.markdown("### 🎬 Generated Video Script")
    st.code(st.session_state.script, language="markdown")
    if st.button("✅ Approve Script & Build Video Description"):
        desc = generate_description(
            keyword=st.session_state.keyword,
            script_text=st.session_state.script,
            affiliate_link=st.session_state.product["affiliate_link"]
        )
        st.session_state.description = desc
        st.session_state.step2_ready = True
        st.success("✅ Description ready.")

# === STEP 2: Manual Video ID + Markdown Approval ===
if st.session_state.step2_ready:
    st.markdown("### 🧾 Final Description")
    st.text_area("📝 SEO-Optimized Description", st.session_state.description, height=250)

    video_id = st.text_input("📺 YouTube Video ID (no full link)")

    if st.button("✅ Approve & Generate Markdown") and video_id.strip():
        filename, markdown = export_markdown(
            title=st.session_state.keyword.title(),
            body=st.session_state.description,
            tags="launchlayer, ai, automation, affiliate",
            video_id=video_id
        )
        st.session_state.filename = filename
        st.session_state.markdown = markdown
        st.session_state.step3_ready = True
        st.success("✅ Markdown ready. Final step below.")

# === STEP 3: Push to Git ===
if st.session_state.step3_ready:
    st.download_button("📥 Download Markdown", st.session_state.markdown, file_name=st.session_state.filename)
    if st.button("🚀 Push to LaunchLayer Blog"):
        success, msg = push_post_to_github(st.session_state.filename, st.session_state.markdown)
        st.success(msg if success else f"❌ Push failed: {msg}")











