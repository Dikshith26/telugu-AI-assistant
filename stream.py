import streamlit as st
import fitz # PyMuPDF
from deep_translator import GoogleTranslator
import io

st.set_page_config(page_title="PDF Translator", layout="centered")

st.title("📄 Multi-Language PDF Translator")
st.write("Upload a PDF to translate it into another language.")

# 1. File Uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# 2. Language Selection
target_lang = st.selectbox("Select Target Language", 
                          options=['te', 'hi', 'en', 'es', 'fr'], 
                          format_func=lambda x: {'te':'Telugu', 'hi':'Hindi', 'en':'English', 'es':'Spanish', 'fr':'French'}[x])

if uploaded_file is not None:
    if st.button("Translate and Download"):
        with st.spinner("Processing pages..."):
            try:
                # Read the uploaded PDF
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                output_doc = fitz.open()
                translator = GoogleTranslator(source='auto', target=target_lang)

                for page in doc:
                    text = page.get_text()
                    new_page = output_doc.new_page(width=page.rect.width, height=page.rect.height)
                    
                    if text.strip():
                        # Simple translation (first 4000 chars of page)
                        translated = translator.translate(text[:4000])
                        new_page.insert_text((50, 50), translated, fontsize=11)

                # Save to memory for download
                pdf_bytes = io.BytesIO()
                output_doc.save(pdf_bytes)
                
                st.success("Done!")
                st.download_button(
                    label="📥 Download Translated PDF",
                    data=pdf_bytes.getvalue(),
                    file_name=f"translated_{target_lang}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error: {e}")

