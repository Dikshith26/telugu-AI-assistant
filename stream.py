if st.button("Generate Result"):
    if not api_key:
        st.error("Please enter your API Key!")
    elif not user_content:
        st.warning("Please provide some content (text or file).")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            # --- CHUNKING LOGIC ---
            # If it's a very long document, we split it into 5-page chunks
            # This prevents the app from crashing on large files
            chunks = [user_content[i:i+15000] for i in range(0, len(user_content), 15000)]
            full_result = []
            
            progress_bar = st.progress(0)
            
            for i, chunk in enumerate(chunks):
                prompt = f"Task: {task}. Target Language: {target_lang}. Text: {chunk}"
                response = client.models.generate_content(
                    model="gemini-2.0-flash", # Note: Changed to 2.0-flash if 2.5 is not available
                    contents=prompt
                )
                full_result.append(response.text)
                progress_bar.progress((i + 1) / len(chunks))
            
            final_output = "\n".join(full_result)
            
            st.success("Done!")
            st.markdown("### Result:")
            st.write(final_output)
            
            # Allow the user to download the long translation
            st.download_button("Download Full Result", final_output, file_name="translated_result.txt")

        except Exception as e:
            st.error(f"Error: {e}")
