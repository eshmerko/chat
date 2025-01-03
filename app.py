from flask import Flask, render_template, request, jsonify
from mistralai import Mistral
import logging

app = Flask(__name__)

# Настройка API
API_KEY = "JQrFsd8FA2PusEUG6eXKce5Zo1y0mjDQ"
MODEL = "mistral-large-latest"
client = Mistral(api_key=API_KEY)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.form.get('message')
        if not user_message or not user_message.strip():
            return jsonify({"error": "Message cannot be empty"}), 400

        chat_response = client.chat.complete(
            model=MODEL,
            messages=[{"role": "user", "content": user_message.strip()}]
        )
        response_content = chat_response.choices[0].message.content
        print("Response from API:", response_content)  # Проверка ответа
        return jsonify({"response": response_content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
