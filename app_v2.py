# app_v2.py

import streamlit as st
from parser import smart_summarize, extract_code_blocks
from utils import read_file, get_clean_filename, save_summary
import os

# App Setup
st.set_page_config(page_title="AIT - ChatGPT Summarizer Pro (v2)", layout="wide")
st.title("🤖 Advanced IT -ChatGPT Summarizer Pro-    by  https://Malcolm-GitHub.github.io")
st.markdown("Enhanced restructuring of technical conversations with logical step formatting, speaker-aware context, and code block extraction.")

# Create output directory
os.makedirs("summaries", exist_ok=True)

# Style Injection for dark mode & speaker colors
st.markdown("""
    <style>
        .speaker-you { color: #56B6C2; font-weight: bold; }
        .speaker-ai { color: #C678DD; font-weight: bold; }
        .step-text { margin-left: 20px; }
        .codebox { background-color: #1e1e1e; border-radius: 6px; padding: 10px; margin: 10px 0; overflow-x: auto; color: #abb2bf; font-family: monospace; }
        .stTextArea > label { font-weight: bold; }
    </style>
""", unsafe_allow_html=True)
# Upload section
st.markdown("### 📁 Upload up to 2 chat logs")
col1, col2 = st.columns(2)
with col1:
    doc1_file = st.file_uploader("📄 Browse Doc 1", type=["txt", "docx"], key="doc1")
with col2:
    doc2_file = st.file_uploader("📄 Browse Doc 2", type=["txt", "docx"], key="doc2")

doc1_text, doc2_text = "", ""
doc1_name, doc2_name = "", ""

if doc1_file:
    doc1_text = read_file(doc1_file)
    doc1_name = get_clean_filename(doc1_file.name)
if doc2_file:
    doc2_text = read_file(doc2_file)
    doc2_name = get_clean_filename(doc2_file.name)
if doc1_text or doc2_text:
    tabs = st.tabs(["📝 Structured Summary", "💻 Code Only", "📜 Full Cleaned Text"])
    
    # Merge + summarize both
    full_combined = doc1_text + "\n\n---\n\n" + doc2_text
    structured, full_cleaned, code_blocks = smart_summarize(full_combined)

    # --- Tab 1: Structured summary with flow ---
    with tabs[0]:
        st.subheader("🧠 Reconstructed Technical Flow")
        st.markdown(structured, unsafe_allow_html=True)
        save_summary(structured, "summaries/structured_summary.html")
        st.download_button("⬇️ Download Structured Summary", structured, file_name="structured_summary.html")

    # --- Tab 2: Code Blocks Only ---
    with tabs[1]:
        st.subheader("💻 Extracted Code Blocks")
        show_code = st.checkbox("Show All Code Blocks", value=True)
        if show_code:
            for i, code in enumerate(code_blocks):
                st.code(code, language="bash")  # You can later auto-detect language

    # --- Tab 3: Full cleaned text ---
    with tabs[2]:
        st.subheader("📜 Full Cleaned Conversation")
        st.text_area("Full Cleaned Text", full_cleaned, height=400)
        save_summary(full_cleaned, "summaries/full_cleaned.txt")
        st.download_button("⬇️ Download Full Text", full_cleaned, file_name="full_cleaned.txt")
