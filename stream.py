import fitz # PyMuPDF
from deep_translator import GoogleTranslator

def translate_pdf(input_path, output_path, target_lang='te'):
    """
    Translates a PDF file to a target language.
    Target lang examples: 'te' (Telugu), 'hi' (Hindi), 'en' (English), 'es' (Spanish)
    """
    try:
        # Load the PDF
        doc = fitz.open(input_path)
        translator = GoogleTranslator(source='auto', target=target_lang)
        
        # Create a new PDF for the translated text
        output_doc = fitz.open()

        print(f"Starting translation to {target_lang}...")

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            
            # Create a new page in the output document
            new_page = output_doc.new_page(width=page.rect.width, height=page.rect.height)
            
            if text.strip():
                # Split text into chunks to avoid API limits (approx 4500 chars)
                chunks = [text[i:i + 4500] for i in range(0, len(text), 4500)]
                translated_text = ""
                
                for chunk in chunks:
                    translated_text += translator.translate(chunk)
                
                # Insert the translated text into the new page
                # Note: For non-Latin scripts (Telugu/Hindi), you must provide a font file (.ttf)
                new_page.insert_text((50, 50), translated_text, fontsize=11)
            
            print(f"Processed page {page_num + 1}")

        output_doc.save(output_path)
        print(f"\nSuccess! Translated PDF saved as: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
translate_pdf("input.pdf", "translated_output.pdf", target_lang="hi")

