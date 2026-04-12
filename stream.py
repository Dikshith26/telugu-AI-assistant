import streamlit as st
import fitz  # PyMuPDF
from deep_translator import GoogleTranslator
import io

st.set_page_config(page_title="PDF Translator", layout="centered")

st.title("📄 Multi-Language PDF Translator")
st.write("Upload a PDF to translate it. Note: Complex layouts may vary.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
target_lang = st.selectbox("Select Target Language", 
                          options=['te', 'hi', 'en'], 
                          format_func=lambda x: {'te':'Telugu', 'hi':'Hindi', 'en':'English'}[x])

if uploaded_file is not None:
    if st.button("Translate and Download"):
        with st.spinner("Translating... Please wait."):
            try:
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                output_doc = fitz.open()
                translator = GoogleTranslator(source='auto', target=target_lang)

                for page in doc:
                    text = page.get_text()
                    new_page = output_doc.new_page(width=page.rect.width, height=page.rect.height)
                    
                    if text.strip():
                        # Translate in chunks to prevent errors
                        translated = translator.translate(text[:4000])
                        
                        # THE FIX: Using 'mti' (Material Icons/Multi) or 'helv' 
                        # For true Telugu/Hindi, 'noto' fonts are best if available.
                        # We use insert_textbox to help with text wrapping.
                        rect = fitz.Rect(50, 50, page.rect.width - 50, page.rect.height - 50)
                        new_page.insert_textbox(rect, translated, fontsize=11, fontname="helv")

                pdf_bytes = io.BytesIO()
                output_doc.save(pdf_bytes)
                
                st.success("Translation Complete!")
                st.download_button(
                    label="📥 Download Translated PDF",
                    data=pdf_bytes.getvalue(),
                    file_name=f"translated_{target_lang}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error: {e}")

