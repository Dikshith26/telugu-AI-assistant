import streamlit as st
from google import genai

st.set_page_config(page_title="Gemini AI Assistant", layout="wide")
st.title("🤖 My AI Business Tool")

# Sidebar for the Google Key
with st.sidebar:
    st.header("Settings")
    # This is the line that was showing the 'openai' link - I fixed it here:
    raw_key = st.text_input("Paste Gemini API Key", type="password", help="Get it from aistudio.google.com")
    api_key = raw_key.strip()

# Main Interface
user_input = st.text_area("What should the AI help you with today?", height=150)
mode = st.selectbox("Select Task", ["Summarize", "Translate to Telugu", "Professional Email"])

if st.button("Generate"):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar first!")
    elif not user_input:
        st.warning("Please enter some text for the AI to process.")
    else:
        try:
            # Connect to Google Gemini
            client = genai.Client(api_key=api_key)
            
            with st.spinner("Processing..."):
                #CHANGE THIS LINE
                response = client.models.generate_content(
                    model="gemini-2.5-flash", # Updated for April 2026
                    contents=f"Perform this task: {mode}. Here is the text: {user_input}"
                )
                
                st.success("Done!")
                st.write(response.text)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

