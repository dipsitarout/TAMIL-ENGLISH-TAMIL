from flask import Flask, request, jsonify, send_from_directory
from translate import Translator
from gtts import gTTS
import os
import speech_recognition as sr
import pyaudio

app = Flask(__name__)

AUDIO_FILE = "static/voice.mp3"

# Ensure the static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return send_from_directory('', 'index3.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text')
    lang_direction = data.get('lang_direction', 'ta_to_en')  # Default to Tamil-to-English

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Set up the translator based on language direction
    if lang_direction == 'ta_to_en':
        translator = Translator(to_lang="en", from_lang='ta')
        target_lang = 'en'
    else:
        return jsonify({"error": "Unsupported language direction"}), 400

    # Translate the text
    translation = translator.translate(text)

    # Generate and save the translated speech
    voice = gTTS(translation, lang=target_lang)
    voice.save(AUDIO_FILE)

    return jsonify({"translation": translation, "audio_url": f"/static/voice.mp3"})

if __name__ == '__main__':
    app.run(debug=True)
