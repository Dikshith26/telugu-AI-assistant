import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="Reading Made Easy", page_icon="📖")

# Sidebar for Security
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Paste Gemini API Key", type="password")
    st.info("A universal tool to summarize and translate any language.")

# App Header
st.title("📖 Reading Made Easy")
st.markdown("Summarize or translate text between any two languages instantly.")
st.markdown("---")

# Main Input
user_input = st.text_area("Paste your text here:", height=200, placeholder="Type or paste content in any language...")

# Universal Settings
col1, col2 = st.columns(2)

with col1:
    target_lang = st.text_input("Target Language:", value="Telugu", help="Which language should the AI write in?")

with col2:
    task = st.selectbox(
        "Select Task:",
        ["Summarize", "Translate", "Draft an Email", "Simplify (Explain like I'm 5)"]
    )

if st.button("Generate Result"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar!")
    elif not user_input:
        st.warning("Please enter some text first.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            # Universal Prompt Logic
            prompt = f"""
            Identify the language of the provided text and perform the following task: {task}.
            The final output MUST be written in {target_lang}.
            
            Text to process:
            {user_input}
            """
            
            with st.spinner(f"Processing your {task}..."):
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=prompt
                )
                st.success("Done!")
                st.markdown("### Result:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"An error occurred. Please check your API key.")
            st.info(f"Technical details: {e}")

