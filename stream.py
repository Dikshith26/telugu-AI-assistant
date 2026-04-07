import streamlit as st
from google import genai
import PyPDF2
from docx import Document
import io

# 1. Page Config
st.set_page_config(page_title="Ultimate AI Assistant", page_icon="🤖", layout="wide")

# 2. Sidebar Setup
with st.sidebar:
    st.title("⚙️ AI Control Panel")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.markdown("---")
    st.info("Using **Gemini 2.5 Pro** for large-scale document analysis.")

# 3. Main Interface
st.title("🤖 Ultimate Professional AI Assistant")

# Language List (Expanded)
languages = sorted([
    "Telugu", "Hindi", "English", "Tamil", "Kannada", "Malayalam", "Marathi", "Bengali",
    "Spanish", "French", "German", "Japanese", "Korean", "Arabic", "Russian", "Portuguese"
])

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Input")
    input_type = st.radio("Source:", ["Manual Text", "Upload File"], horizontal=True)
    
    user_data = ""
    if input_type == "Manual Text":
        user_data = st.text_area("Paste your text here:", height=300)
    else:
        files = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"], accept_multiple_files=True)
        if files:
            for f in files:
                if f.type == "application/pdf":
                    pdf = PyPDF2.PdfReader(f)
                    user_data += "\n".join([page.extract_text() for page in pdf.pages])
                elif f.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    doc = Document(f)
                    user_data += "\n".join([p.text for p in doc.paragraphs])
                else:
                    user_data += f.read().decode("utf-8")

with col2:
    st.subheader("🎯 Task Configuration")
    mode = st.selectbox("What do you want to do?", [
        "Translate", 
        "Summarize Document", 
        "Create Email Format", 
        "Simplify Language",
        "Extract Key Action Items"
    ])
    
    target_lang = st.selectbox("Target Language:", languages)
    
    # Custom Instructions for Email
    email_context = ""
    if mode == "Create Email Format":
        email_context = st.text_input("Email Tone (e.g., Professional, Friendly, Urgent):", "Professional")

    process_btn = st.button("🚀 Process with Gemini 2.5 Pro", use_container_width=True)

# 4. Execution Logic
if process_btn:
    if not api_key:
        st.error("Please enter an API Key!")
    elif not user_data:
        st.warning("Please provide input data.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            # System Prompting based on Mode
            prompts = {
                "Translate": f"Translate the following text into {target_lang}. Keep the professional tone.",
                "Summarize Document": f"Provide a detailed summary of this document in {target_lang}.",
                "Create Email Format": f"Draft a {email_context} email in {target_lang} based on this content.",
                "Simplify Language": f"Explain this content in very simple {target_lang} (5th-grade level).",
                "Extract Key Action Items": f"List the main tasks and deadlines from this text in {target_lang}."
            }

            with st.spinner("Analyzing large-scale data..."):
                # Gemini 2.5 Pro handles the 300 pages in one shot
                response = client.models.generate_content(
                    model="gemini-2.5-pro",
                    contents=f"{prompts[mode]}\n\nContent:\n{user_data}"
                )
            
            st.success("✨ Analysis Complete!")
            st.markdown("### 📝 Result")
            st.write(response.text)
            
            # Professional Download Options
            st.download_button("📥 Download Result (.txt)", response.text, file_name=f"{mode}_result.txt")

        except Exception as e:
            if "429" in str(e):
                st.error("🚨 API Quota Reached. Gemini 2.5 Pro requires a 'Pay-as-you-go' account for large files.")
            else:
                st.error(f"Error: {e}")
