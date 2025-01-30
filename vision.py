import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini model
def get_gemini_response(input_text, image):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model
    
    # Ensure we pass only the necessary elements
    request_data = []
    if input_text:
        request_data.append(input_text)
    if image:
        request_data.append(image)  # Pass PIL image directly

    # Generate response based on input
    if request_data:
        response = model.generate_content(request_data)
        return response.text
    else:
        return "No valid input provided."

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")

# Input prompt
input_text = st.text_input("Input Prompt:", key="input")

# File uploader for image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None  

if uploaded_file is not None:
    image = Image.open(uploaded_file)  # Keep as PIL Image
    st.image(image, caption="Uploaded Image.", use_container_width=True)  # Updated parameter

# Submit button
submit = st.button("Tell me about the image")

# Generate response when button is clicked
if submit:
    if not input_text and not image:
        st.warning("Please enter a prompt or upload an image.")
    else:
        response = get_gemini_response(input_text, image)
        st.subheader("The Response is")
        st.write(response)
