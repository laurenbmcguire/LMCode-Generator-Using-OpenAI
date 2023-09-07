import os
import openai
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@st.cache_resource(ttl=3600)  # Cache results for an hour to avoid duplicate API calls
def generate_code(question: str) -> (str, str):
    """
    Return the solution to the question/users request by providing python code that is error free, detailed, 
    commented out step by step, and ready to run, at the end of the file provide a commented out brief summary of what you did.
    """
    # Improve prompt engineering for better results
    instructions = (f"Write a Python code solution for the following problem description:\n\n"
                    f"{question}\n\n"
                    f"Provide the code in a format that is ready to run, without any unnecessary comments or text. "
                    f"After the solution, include a brief summary in comments.")
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": instructions}
            ]
        )
        generated_code = response['choices'][0]['message']['content'].strip()
        return generated_code, None
    except openai.error.OpenAIError as e:
        return None, str(e)

# Streamlit UI
st.title("Code Generator Using OpenAI")

# Input for the coding question
question = st.text_area("Enter your coding question:")

# Button to trigger the code generation
if st.button("Generate Code"):
    if question:
        with st.spinner("Generating code..."):
            generated_code, error = generate_code(question)
            
            if error:
                st.error(f"Error: {error}")
            else:
                st.subheader("Generated Code:")
                st.code(generated_code, language='python')
                
                # Get current date and time
                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"main_{current_time}.py"
                
                # Allow users to download the generated code as a .py file
                st.download_button(
                    label="Download Generated Code",
                    data=generated_code.encode(),
                    file_name=file_name,
                    mime="text/x-python"
                )
    else:
        st.warning("Please enter a coding question to generate the code.")

text = """
Built by Lauren McGuire
"""
st.write(text)
