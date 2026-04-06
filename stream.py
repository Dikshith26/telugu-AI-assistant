import streamlit as st
from google import genai
import PyPDF2
from docx import Document
import time # Needed to fix the 429 error

# 1. Setup
st.set_page_config(page_title="Pro Reader AI", page_icon="📚")

# 2. Sidebar Settings
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Large files take time. We will process them in chunks to avoid errors.")

st.title("📚 Pro Reading Assistant")

# 3. Input Method
input_method = st.radio("Choose Input Method:", ["Paste Text", "Upload File"], horizontal=True)

user_content = ""
if input_method == "Paste Text":
    user_content = st.text_area("Paste text here:", height=200)
else:
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            user_content = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
        else:
            user_content = uploaded_file.read().decode("utf-8")

# 4. ALL LANGUAGES RESTORED
target_lang = st.selectbox("Target Language", [
    "Telugu", "Hindi", "English", "Spanish", "French", 
    "German", "Tamil", "Kannada", "Malayalam", "Marathi", "Bengali"
])
task = st.selectbox("Task", ["Summarize", "Translate", "Simplify", "Extract Key Points"])

# 5. Execution with 429 Fix
if st.button("Generate Result"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar.")
    elif not user_content:
        st.warning("Please provide some text or a file.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            # Smaller chunks for large PDFs (10,000 characters)
            chunks = [user_content[i:i+10000] for i in range(0, len(user_content), 10000)]
            full_result = []
            
            bar = st.progress(0)
            status_text = st.empty()
            
            for i, chunk in enumerate(chunks):
                status_text.text(f"Processing chunk {i+1} of {len(chunks)}...")
                
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=f"{task} into {target_lang}: {chunk}"
                )
                full_result.append(response.text)
                bar.progress((i + 1) / len(chunks))
                
                # --- THE 429 FIX ---
                # We wait 10 seconds between chunks so the free tier doesn't block us
                if len(chunks) > 1:
                    time.sleep(10) 
            
            status_text.text("✅ All pages processed!")
            final_text = "\n\n".join(full_result)
            st.markdown("### Result:")
            st.write(final_text)
            st.download_button("Download Result", final_text, file_name="ai_result.txt")

        except Exception as e:
            if "429" in str(e):
                st.error("API Limit Reached. Please wait 60 seconds and try again. For 300-page files, the free tier is very slow.")
            else:
                st.error(f"Error: {e}")
