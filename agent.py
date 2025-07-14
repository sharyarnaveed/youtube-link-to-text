# agent.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.agents import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from flask import Flask, request, jsonify
import requests
load_dotenv()



@tool
def transcribe_youtube(url: str) -> str:
    """Downloads and transcribes a YouTube video from a given URL."""
    from tools.download_audio import download_audio
    from tools.transcribe import transcribe
    path = download_audio(url)
    return transcribe(path)
    
@tool
def summarize_transcript(text: str) -> str:
    """Summarizes a video transcript using Gemini."""
    from tools.summerize import summarize_text
    return summarize_text(text)



llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.3,
            google_api_key=os.getenv("GEN_AI_API")
)
        

tools = [transcribe_youtube, summarize_transcript]


agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


app = Flask(__name__)

@app.route('/youtubetotext', methods=["POST"])

def youtube_to_text():
    try:
        data = request.get_json()  
        url = data.get("url")
        if not url:
            return jsonify({"error": "URL is required"}), 400

        query = f"Here is a YouTube link: {url}. Please transcribe and summarize it and explain it."
        result = agent.run(query)
        print("🧠 Agent Output:", result)
        return jsonify({"result": result})

    except Exception as e:
       return jsonify({"error": str(e)}), 500      
if __name__ == '__main__':
    app.run(debug=True)