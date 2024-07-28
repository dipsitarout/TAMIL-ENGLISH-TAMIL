from flask import Flask, request, jsonify, send_from_directory
from translate import Translator
from gtts import gTTS
import os

app = Flask(__name__)

AUDIO_FILE = "static/voice.mp3"

# Ensure the static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    translator = Translator(to_lang="ta")
    translation = translator.translate(text)

    # Generate and save the translated speech
    voice = gTTS(translation, lang='ta')
    voice.save(AUDIO_FILE)

    return jsonify({"translation": translation, "audio_url": f"/static/voice.mp3"})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
