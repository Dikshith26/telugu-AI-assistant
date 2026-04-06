import streamlit as st
from google import genai
import PyPDF2
from docx import Document

# 1. Page Configuration
st.set_page_config(page_title="Global AI Document Pro", page_icon="🌐", layout="wide")

# 2. Sidebar
with st.sidebar:
    st.title("🚀 Business Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.markdown("---")
    st.success("✅ Pay-as-you-go enabled (Fast Mode)")

st.title("🌐 Universal Language Assistant")

# 3. Input Section
col1, col2 = st.columns([1, 1])

with col1:
    input_method = st.radio("Input Source:", ["✍️ Text", "📂 File"], horizontal=True)
    user_content = ""
    if input_method == "✍️ Text":
        user_content = st.text_area("Paste content:", height=300)
    else:
        uploaded_file = st.file_uploader("Upload PDF/DOCX", type=["pdf", "docx", "txt"])
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                reader = PyPDF2.PdfReader(uploaded_file)
                user_content = "".join([p.extract_text() for p in reader.pages if p.extract_text()])
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = Document(uploaded_file)
                user_content = "\n".join([p.text for p in doc.paragraphs])
            else:
                user_content = uploaded_file.read().decode("utf-8")

with col2:
    # --- COMPREHENSIVE LANGUAGE LIST ---
    # This list covers major global and regional Indian languages
    languages = sorted([
        "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani", 
        "Bengali", "Bosnian", "Bulgarian", "Catalan", "Chinese (Simplified)", 
        "Chinese (Traditional)", "Croatian", "Czech", "Danish", "Dutch", "English", 
        "Estonian", "Farsi", "Finnish", "French", "Georgian", "German", "Greek", 
        "Gujarati", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian", 
        "Italian", "Japanese", "Kannada", "Kazakh", "Korean", "Latvian", 
        "Lithuanian", "Macedonian", "Malay", "Malayalam", "Marathi", "Mongolian", 
        "Nepali", "Norwegian", "Odia", "Pashto", "Polish", "Portuguese", "Punjabi", 
        "Romanian", "Russian", "Sanskrit", "Serbian", "Sinhala", "Slovak", 
        "Slovenian", "Somali", "Spanish", "Swahili", "Swedish", "Tamil", "Telugu", 
        "Thai", "Turkish", "Ukrainian", "Urdu", "Uzbek", "Vietnamese", "Welsh"
    ])
    
    target_lang = st.selectbox("Select Target Language", languages)
    task = st.selectbox("Select Task", ["Translate", "Summarize", "Simplify", "Proofread"])
    
    start_btn = st.button("🚀 Start Fast Processing", use_container_width=True)

# 4. Fast AI Engine (No forced delays for Paid Users)
if start_btn:
    if not api_key:
        st.error("Missing API Key")
    elif not user_content:
        st.warning("No content provided")
    else:
        try:
            client = genai.Client(api_key=api_key)
            # Larger chunks (15,000 chars) are fine for Paid Tier
            chunks = [user_content[i:i+15000] for i in range(0, len(user_content), 15000)]
            full_result = []
            
            bar = st.progress(0)
            status = st.empty()
            
            for i, chunk in enumerate(chunks):
                status.info(f"Processing Part {i+1} of {len(chunks)}...")
                
                # Using Gemini 2.5 Flash for the best speed/cost balance
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=f"{task} the following into {target_lang}. Keep formatting: {chunk}"
                )
                full_result.append(response.text)
                bar.progress((i + 1) / len(chunks))
                
                # NOTE: time.sleep() REMOVED for Paid Tier speed!

            status.success("✨ All Done!")
            final_output = "\n\n".join(full_result)
            st.text_area("Result:", final_output, height=400)
            st.download_button("📥 Download Final Text", final_output, file_name="ai_output.txt")

        except Exception as e:
            st.error(f"Error: {e}")
