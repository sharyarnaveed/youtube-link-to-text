import whisper

def transcribe(audiopath="audio.mp3"):  
    model = whisper.load_model("base")
    result = model.transcribe(audiopath) 
    return result["text"]