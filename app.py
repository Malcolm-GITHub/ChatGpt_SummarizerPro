import streamlit as st
from parser import clean_text, summarize
from utils import read_file, get_clean_filename, save_summary
import os

# ---- App Config ----
st.set_page_config(page_title="ChatGPT Summarizer Pro", layout="wide")
st.title("🤖 ChatGPT Summarizer Pro")
st.markdown("Summarize and clean technical chat conversations with smart formatting and export options.")

# ---- Ensure output directory exists ----
os.makedirs("summaries", exist_ok=True)

# ---- Upload Interface ----
st.markdown("### 📁 Upload Two Documents for Summarization")

col1, col2 = st.columns(2)
doc1_file, doc2_file = None, None

with col1:
    doc1_file = st.file_uploader("📄 Browse Doc 1", type=["txt", "docx"], key="doc1")

with col2:
    doc2_file = st.file_uploader("📄 Browse Doc 2", type=["txt", "docx"], key="doc2")

# ---- Processing Logic ----
doc1_text, doc2_text = "", ""
doc1_name, doc2_name = "", ""

if doc1_file:
    doc1_text = read_file(doc1_file)
    doc1_name = get_clean_filename(doc1_file.name)
    summary1 = summarize(doc1_text)
    summary1_path = f"summaries/summary_{doc1_name}.txt"
    save_summary(summary1, summary1_path)

    st.markdown(f"### 🧾 Summary for `{doc1_name}`")
    st.text_area("Summary Text", summary1, height=300)
    st.download_button("⬇️ Download Summary", summary1, file_name=f"summary_{doc1_name}.txt")

if doc2_file:
    doc2_text = read_file(doc2_file)
    doc2_name = get_clean_filename(doc2_file.name)
    summary2 = summarize(doc2_text)
    summary2_path = f"summaries/summary_{doc2_name}.txt"
    save_summary(summary2, summary2_path)

    st.markdown(f"### 🧾 Summary for `{doc2_name}`")
    st.text_area("Summary Text", summary2, height=300)
    st.download_button("⬇️ Download Summary", summary2, file_name=f"summary_{doc2_name}.txt")

# ---- Merged Summary ----
if doc1_text and doc2_text:
    st.markdown("## 🔀 Merged Summary")
    merged_text = doc1_text + "\n\n--- MERGED ---\n\n" + doc2_text
    merged_summary = summarize(merged_text)
    merged_path = "summaries/merged_summary.txt"
    save_summary(merged_summary, merged_path)

    st.text_area("Merged Summary Text", merged_summary, height=400)
    st.download_button("⬇️ Download Merged Summary", merged_summary, file_name="merged_summary.txt")
