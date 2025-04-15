from gtts import gTTS
import speech_recognition as sr
import tempfile
import os
import requests

def speech_to_text(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="it-IT")
            return text
    except Exception as e:
        print(f"Errore STT: {str(e)}")
        return ""

def text_to_speech(text, language='it'):
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        print(f"Errore TTS: {str(e)}")
        return ""

def process_message(user_input):
    try:
        # Usa un modello HuggingFace senza API key
        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
        response = requests.post(API_URL, json={"inputs": user_input}, timeout=30)
        return response.json()[0]['generated_text']
    except Exception as e:
        return f"Errore: {str(e)}"
