import streamlit as st
from google import genai
import PyPDF2
from docx import Document
import io

# 1. Setup
st.set_page_config(page_title="Pro Reader AI", page_icon="📚")

# 2. Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Upload a PDF or Word doc to begin.")

st.title("📚 Pro Reading Assistant")

# 3. Input
input_method = st.radio("Choose Input Method:", ["Paste Text", "Upload File"], horizontal=True)

user_content = ""
if input_method == "Paste Text":
    user_content = st.text_area("Paste text here:", height=200)
else:
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            user_content = "".join([page.extract_text() for page in reader.pages])
        else:
            user_content = uploaded_file.read().decode("utf-8")

# 4. Action
target_lang = st.selectbox("Target Language", ["Telugu", "Hindi", "English", "Spanish"])
task = st.selectbox("Task", ["Summarize", "Translate", "Simplify"])

if st.button("Generate Result"):
    if not api_key:
        st.error("Missing API Key")
    else:
        try:
            client = genai.Client(api_key=api_key)
            # Break 300 pages into chunks of 15,000 characters
            chunks = [user_content[i:i+15000] for i in range(0, len(user_content), 15000)]
            full_result = []
            
            bar = st.progress(0)
            for i, chunk in enumerate(chunks):
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=f"{task} to {target_lang}: {chunk}"
                )
                full_result.append(response.text)
                bar.progress((i + 1) / len(chunks))
            
            st.write("\n".join(full_result))
        except Exception as e:
            st.error(f"Error: {e}")
