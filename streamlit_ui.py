import streamlit as st

st.set_page_config(page_title="Backdoor Blog Builder", layout="centered")

st.title("🛠️ Backdoor Blog Builder")
st.markdown("This is a placeholder app shell. Full functionality coming soon.")

topic = st.text_input("Enter a blog topic:")
tone = st.selectbox("Select tone:", ["professional", "conversational", "casual"])
tags_input = st.text_input("Tags (comma separated):", value="seo, automation, affiliate")
use_affiliate = st.checkbox("Insert affiliate links automatically")

if st.button("Generate Blog Post") and topic.strip():
    st.success("✅ Placeholder activated")
    st.code(f"# {topic.title()}\n\nThis is a placeholder post in a {tone} tone.\n\nTags: {tags_input}", language="markdown")
else:
    st.markdown("⚠️ Enter a topic to simulate post generation.")
