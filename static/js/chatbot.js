// ============= SIMPLE GEMINI CHATBOT WITH HISTORY =============
let sessionId = localStorage.getItem('chat_session_id') || 'session_' + Date.now();

// Save session ID for anonymous users
if (!localStorage.getItem('chat_session_id')) {
    localStorage.setItem('chat_session_id', sessionId);
}

function initChatbot() {
    const fab = document.getElementById('chatbot-fab');
    const chatWindow = document.getElementById('chat-window');
    const closeBtn = document.getElementById('close-chat');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-chat');
    const chatMessages = document.getElementById('chat-messages');

    if (!fab || !chatWindow) return;

    // Toggle chat window
    fab.addEventListener('click', () => {
        chatWindow.classList.toggle('active');
        if (chatWindow.classList.contains('active')) {
            // Load history when opening chat
            loadChatHistory();
            chatInput.focus();
        }
    });

    // Close chat
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            chatWindow.classList.remove('active');
        });
    }

    // Load chat history
    async function loadChatHistory() {
        try {
            const response = await fetch(`/api/chat/history?session_id=${sessionId}`);
            const data = await response.json();

            if (data.success && data.history && data.history.length > 0) {
                // Clear current messages
                chatMessages.innerHTML = '';

                // Display history
                data.history.forEach(msg => {
                    addMessage(msg.role, msg.message);
                });
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    }

    // Send message
    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        // Add user message
        addMessage('user', message);
        chatInput.value = '';

        // Add typing indicator
        const typingId = addTypingIndicator();

        try {
            const payload = {
                message: message,
                session_id: sessionId
            };

            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            removeTypingIndicator(typingId);

            if (data.success) {
                addMessage('bot', data.response);
            } else {
                addMessage('bot', "Désolé, une erreur s'est produite.");
            }
        } catch (error) {
            removeTypingIndicator(typingId);
            addMessage('bot', "Erreur de connexion au serveur.");
        }
    }

    function addMessage(role, text) {
        const div = document.createElement('div');
        div.className = `message ${role}-message`;
        div.innerHTML = text.replace(/\n/g, '<br>');
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addTypingIndicator() {
        const id = 'typing-' + Date.now();
        const div = document.createElement('div');
        div.id = id;
        div.className = 'message bot-message typing-indicator';
        div.innerHTML = '<span></span><span></span><span></span>';
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    // Event listeners
    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }

    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChatbot);
} else {
    initChatbot();
}
