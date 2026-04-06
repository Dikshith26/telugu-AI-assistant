import streamlit as st
from google import genai
import PyPDF2
from docx import Document
import io

# --- 1. Helper Function to Read Files ---
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return uploaded_file.read().decode("utf-8")

# --- 2. Page Config & Sidebar ---
st.set_page_config(page_title="Pro Reader AI", page_icon="📚")

with st.sidebar:
    st.title("⚙️ Settings")
    # Using secrets is better for monetization, but keeping this for your testing:
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Upload a PDF or Word doc to begin.")

st.title("📚 Pro Reading Assistant")
st.markdown("---")

# --- 3. Input Selection (Text or File) ---
input_method = st.radio("Choose Input Method:", ["Paste Text", "Upload File"], horizontal=True)

user_content = ""
if input_method == "Paste Text":
    user_content = st.text_area("Paste your text here:", height=200)
else:
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
    if uploaded_file:
        with st.spinner("Reading file..."):
            user_content = extract_text_from_file(uploaded_file)
            st.success("File loaded successfully!")

# --- 4. Options ---
st.write("**Select Target Language:**")
lang_options = ["Telugu", "Hindi", "English", "Spanish", "French", "Other"]
target_lang = st.radio("Choose one:", lang_options, horizontal=True)

task = st.selectbox("What should the AI do?", ["Summarize", "Translate", "Simplify", "Extract Key Points"])

# --- 5. Execution ---
if st.button("Generate Result"):
    if not api_key:
        st.error("Please enter your API Key!")
    elif not user_content:
        st.warning("Please provide some content (text or file).")
    else:
        try:
            client = genai.Client(api_key=api_key)
            # Improved Prompt for better results
            prompt = f"Task: {task}. Target Language: {target_lang}. Input Text: {user_content}"
            
            with st.spinner("🚀 AI is processing your document..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                st.success("Done!")
                st.markdown("### Result:")
                st.write(response.text)
                
                # Monetization Tip: Add a "Download Result" button here
                st.download_button("Download Result as Text", response.text, file_name="result.txt")

        except Exception as e:
            st.error(f"Error: {e}")

