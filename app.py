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

        # Системный промпт для задания контекста беседы
        system_prompt = {
            "role": "system",
            "content": "Вы являетесь помощником, который помогает с техническими вопросами по выбору сайта. Отвечайте четко и по существу."
        }

        # Создание запроса с системным промптом
        chat_response = client.chat.complete(
            model=MODEL,
            messages=[
                system_prompt,  # Добавление системного промпта
                {"role": "user", "content": user_message.strip()}
            ]
        )
        response_content = chat_response.choices[0].message.content

        # Преобразование текста в формат Markdown или HTML (если необходимо)
        formatted_response = format_response(response_content)

        return jsonify({"response": formatted_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def format_response(text):
    """
    Преобразует текст в читаемый вид, заменяя Markdown-синтаксис на переносы строк.
    """
    # Заменяем Markdown-форматирование на перенос строки
    text = text.replace("**", "\n").replace("*", "")  # Убираем неиспользуемый Markdown
    # Убираем лишние пробелы, если есть
    return text.strip()


if __name__ == '__main__':
    app.run(debug=True)