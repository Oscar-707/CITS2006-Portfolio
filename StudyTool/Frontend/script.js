async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    if (!message) return;

    // Show user's message immediately
    appendMessage('user', message);
    userInput.value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Show assistant's reply dynamically
        appendMessage('assistant', data.response);
    } catch (error) {
        console.error('Error:', error);
        appendMessage('assistant', 'An error occurred while fetching the response.');
    }
}
// Append user messages and display them in the text field
function appendMessage(sender, text) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = `${sender === 'user' ? 'You' : 'Assistant'}: ${text}`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
