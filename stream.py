import streamlit as st
from google import genai
import time
import os

# 1. Setup
st.set_page_config(page_title="Pro Document AI", page_icon="📄")

with st.sidebar:
    st.title("⚙️ Setup")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Large files (up to 300 pages) work best with a verified API key.")

st.title("📄 High-Capacity Document AI")

# 2. File Upload
uploaded_file = st.file_uploader("Upload PDF or Word Doc", type=["pdf", "docx", "txt"])

# 3. Language & Task
all_langs = sorted(["Telugu", "Hindi", "English", "Tamil", "Spanish", "French", "German"])
target_lang = st.selectbox("Target Language", all_langs)
task = st.selectbox("Task", ["Translate", "Summarize", "Explain"])

if st.button("🚀 Process Large Document"):
    if not api_key:
        st.error("Please enter your API Key!")
    elif not uploaded_file:
        st.warning("Please upload a file first.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            # SAVE FILE LOCALLY TEMPORARILY
            with open("temp_file.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("📤 Uploading to AI Studio... (This handles large files better)"):
                # UPLOAD TO FILES API
                uploaded_doc = client.files.upload(path="temp_file.pdf")
                
                # Wait for file to be processed by Google
                while uploaded_doc.state.name == "PROCESSING":
                    time.sleep(2)
                    uploaded_doc = client.files.get(name=uploaded_doc.name)
            
            st.info("🧠 AI is reading the document...")
            
            # GENERATE CONTENT (Gemini can read the whole file at once this way!)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    uploaded_doc,
                    f"Please {task} this entire document into {target_lang}. "
                    "If the document is very long, provide a detailed page-by-page translation."
                ]
            )
            
            st.success("✅ Done!")
            st.markdown("### Result:")
            st.write(response.text)
            
            # Clean up
            os.remove("temp_file.pdf")

        except Exception as e:
            if "429" in str(e):
                st.error("🚨 Daily Limit Reached. Google only allows 250 requests/day for free. Please try again tomorrow or enable Billing in AI Studio.")
            else:
                st.error(f"Error: {e}")
