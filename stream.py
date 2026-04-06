import streamlit as st
from google import genai
import PyPDF2
from docx import Document
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Universal AI Translator Pro", page_icon="🌐", layout="wide")

# --- 2. SIDEBAR (MONETIZATION READY) ---
with st.sidebar:
    st.title("🚀 Pro Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.markdown("---")
    st.info("💡 **Business Tip:** Large files (300+ pages) use many 'tokens'. On the free tier, we wait 15 seconds between parts to avoid errors.")
    st.link_button("💳 Get Pro API Key", "https://aistudio.google.com/")

# --- 3. MAIN INTERFACE ---
st.title("🌐 Universal Language Assistant")
st.subheader("Translate, Summarize, and Analyze any Document")

col1, col2 = st.columns([1, 1])

with col1:
    input_method = st.radio("Choose Input:", ["✍️ Paste Text", "📂 Upload Document"], horizontal=True)
    
    user_content = ""
    if input_method == "✍️ Paste Text":
        user_content = st.text_area("Paste your content here:", height=300)
    else:
        uploaded_file = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])
        if uploaded_file:
            with st.spinner("Reading document..."):
                if uploaded_file.type == "application/pdf":
                    reader = PyPDF2.PdfReader(uploaded_file)
                    user_content = "".join([p.extract_text() for p in reader.pages if p.extract_text()])
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    doc = Document(uploaded_file)
                    user_content = "\n".join([p.text for p in doc.paragraphs])
                else:
                    user_content = uploaded_file.read().decode("utf-8")
            st.success(f"Loaded {len(user_content)} characters!")

with col2:
    # --- ALL LANGUAGES ---
    all_langs = sorted(["Telugu", "Hindi", "English", "Tamil", "Kannada", "Malayalam", "Marathi", "Bengali", "Gujarati", "Punjabi", "Spanish", "French", "German", "Japanese", "Korean", "Arabic", "Russian"])
    target_lang = st.selectbox("Target Language", all_langs)
    
    task = st.selectbox("What should I do?", ["Translate", "Summarize", "Simplify", "Extract Action Items"])
    
    start_button = st.button("🚀 Start AI Processing", use_container_width=True)

# --- 4. THE AI ENGINE (With 429 Error Protection) ---
if start_button:
    if not api_key:
        st.error("❌ Please enter an API Key in the sidebar.")
    elif not user_content:
        st.warning("⚠️ Please provide some text or a file.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            # Chunks of 8,000 characters (Safe for 300-page files)
            chunks = [user_content[i:i+8000] for i in range(0, len(user_content), 8000)]
            full_result = []
            
            progress_bar = st.progress(0)
            status = st.empty()
            
            for i, chunk in enumerate(chunks):
                status.info(f"Processing Part {i+1} of {len(chunks)}... (Don't close this tab)")
                
                # RETRY LOGIC for 429 Errors
                success = False
                for attempt in range(3):
                    try:
                        response = client.models.generate_content(
                            model="gemini-2.5-flash", 
                            contents=f"Task: {task} into {target_lang}. Content: {chunk}"
                        )
                        full_result.append(response.text)
                        success = True
                        break 
                    except Exception as e:
                        if "429" in str(e):
                            wait = (attempt + 1) * 20
                            status.warning(f"Limit reached. Sleeping for {wait}s...")
                            time.sleep(wait)
                        else:
                            st.error(f"Error: {e}")
                            st.stop()
                
                if not success:
                    st.error("Too many requests. Please try a smaller file or wait 1 minute.")
                    break

                progress_bar.progress((i + 1) / len(chunks))
                # Mandatory wait between chunks for free tier
                if len(chunks) > 1:
                    time.sleep(10)

            status.success("✅ Document Processing Complete!")
            final_text = "\n\n".join(full_result)
            st.text_area("Final Result", final_text, height=400)
            st.download_button("📥 Download Result", final_text, file_name="ai_output.txt")

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
