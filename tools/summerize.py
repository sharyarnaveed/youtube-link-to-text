import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def summarize_text(text):
    genai.configure(api_key=os.getenv("GEN_AI_API"))
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"Summarize the following transcript:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text
