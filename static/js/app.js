document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('chat-form');
    const messageInput = document.getElementById('message');
    const messagesDiv = document.getElementById('messages');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const userMessage = messageInput.value.trim();
        if (!userMessage) return;

        // Отобразить сообщение пользователя
        appendMessage(userMessage, 'user-message');
        messageInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ message: userMessage }),
            });

            if (!response.ok) {
                appendMessage('Ошибка сервера. Попробуйте позже.', 'bot-message');
                return;
            }

            const data = await response.json();
            const botMessage = data.response || 'Нет ответа от бота.';
            appendMessage(botMessage, 'bot-message');
        } catch (error) {
            appendMessage('Произошла ошибка при подключении к серверу.', 'bot-message');
            console.error(error);
        }
    });

    function appendMessage(content, className) {
        const messageDiv = document.createElement('div');
        messageDiv.textContent = content;
        messageDiv.classList.add('message', className);
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight; // Прокрутка вниз
    }
});
