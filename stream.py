import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="Reading Made Easy", page_icon="📖")

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Paste Gemini API Key", type="password")
    st.info("Tip: If you get a 'Red Error', wait 60 seconds and try again.")

st.title("📖 Reading Made Easy")
st.markdown("---")

# 1. User Input
user_input = st.text_area("Paste your text here:", height=200)

# 2. Language Selection (Option Buttons)
st.write("**Select Target Language:**")
lang_options = ["Telugu", "Hindi", "English", "Spanish", "French", "Other"]
target_lang = st.radio("Choose one:", lang_options, horizontal=True)

# If 'Other' is picked, show a text box
if target_lang == "Other":
    target_lang = st.text_input("Type other language:")

# 3. Task Selection
task = st.selectbox(
    "What should the AI do?",
    ["Summarize", "Translate", "Draft an Email", "Simplify"]
)

if st.button("Generate Result"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar!")
    elif not user_input:
        st.warning("Please enter some text.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            prompt = f"Task: {task}. Output Language: {target_lang}. Text: {user_input}"
            
            with st.spinner("Processing..."):
                # Using 1.5-flash which is often more stable for free-tier users
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=prompt
                )
                st.success("Done!")
                st.markdown("### Result:")
                st.write(response.text)
                
        except Exception as e:
            if "429" in str(e):
                st.error("Too many requests! Please wait 60 seconds before clicking again.")
            else:
                st.error(f"Error: {e}")

