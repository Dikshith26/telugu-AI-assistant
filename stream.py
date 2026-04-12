import streamlit as st
import fitz # PyMuPDF
from deep_translator import GoogleTranslator
import io
import os

st.set_page_config(page_title="PDF Translator", layout="centered")

st.title("📄 Professional PDF Translator")

# Check if font file exists in your GitHub repo
font_path = "font.ttf" # <--- Make sure this matches your uploaded filename

uploaded_file = st.file_uploader("Upload PDF", type="pdf")
target_lang = st.selectbox("Language", ['te', 'hi', 'en'])

if uploaded_file and st.button("Translate"):
    if not os.path.exists(font_path):
        st.error("Font file not found! Please upload 'font.ttf' to your GitHub repo.")
    else:
        with st.spinner("Translating..."):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            output_doc = fitz.open()
            translator = GoogleTranslator(source='auto', target=target_lang)

            for page in doc:
                text = page.get_text()
                new_page = output_doc.new_page(width=page.rect.width, height=page.rect.height)
                
                if text.strip():
                    translated = translator.translate(text[:4000])
                    
                    # Define the area where text will be placed
                    rect = fitz.Rect(50, 50, page.rect.width - 50, page.rect.height - 50)
                    
                    # THE CRITICAL PART: Registering and using your custom font
                    new_page.insert_textbox(
                        rect, 
                        translated, 
                        fontsize=12, 
                        fontname="fgen", # logical name
                        fontfile=font_path # physical path to your .ttf file
                    )

            pdf_bytes = io.BytesIO()
            output_doc.save(pdf_bytes)
            st.download_button("Download Translated PDF", pdf_bytes.getvalue(), "translated.pdf")

