class AgriculturalChatbot {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.messages = [];
        this.isLoading = false;
        this.options = {
            apiEndpoint: '/api/chat',
            autoScroll: true,
            enableSound: false,
            ...options
        };
        this.initializeUI();
    }

    initializeUI() {
        const container = document.getElementById(this.containerId);
        if (!container) return;

        const language = this.getCurrentLanguage();
        const uiText = this.getUIText(language);
        const assistantAvailable = this.options.assistantAvailable !== false;

        container.innerHTML = `
            <div class="chat-container">
                ${assistantAvailable ? '' : `<div class="alert alert-warning m-2 mb-0 py-2 small">Cerebras is not configured. Add CEREBRAS_API_KEY in <code>.env</code> to enable live answers.</div>`}
                <div class="chat-messages" id="chat-messages"></div>
                <div class="chat-input">
                    <input type="text" id="chat-input" placeholder="${uiText.placeholder}" />
                    <button id="chat-send" class="btn btn-primary btn-sm" type="button">${uiText.send}</button>
                </div>
                <div class="chatbot-suggestions" id="chatbot-suggestions"></div>
            </div>
        `;

        document.getElementById('chat-send').addEventListener('click', () => this.sendMessage());
        document.getElementById('chat-input').addEventListener('keypress', event => {
            if (event.key === 'Enter') this.sendMessage();
        });
        this.renderSuggestions();
    }

    async sendMessage() {
        const inputElement = document.getElementById('chat-input');
        const message = inputElement.value.trim();
        if (!message || this.isLoading) return;

        this.addMessage(message, 'user');
        inputElement.value = '';

        try {
            this.isLoading = true;
            this.showTypingIndicator();
            const response = await fetch(this.options.apiEndpoint, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    question: message,
                    language: this.getCurrentLanguage(),
                    education_level: document.body.dataset.educationLevel || 'literate'
                })
            });
            const data = await response.json();
            this.removeTypingIndicator();
            this.addMessage(
                data.answer || data.message || this.getFallbackMessage(this.getCurrentLanguage()),
                'bot'
            );
        } catch (error) {
            this.removeTypingIndicator();
            this.addMessage(this.getFallbackMessage(this.getCurrentLanguage()), 'bot');
        } finally {
            this.isLoading = false;
        }
    }

    addMessage(text, sender = 'user') {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.innerHTML = `
            <div class="content">
                <p>${this.escapeHtml(text)}</p>
                <small>${new Date().toLocaleTimeString()}</small>
            </div>
        `;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        this.messages.push({text, sender, timestamp: new Date()});
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing-indicator';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = '<div class="content"><p>Thinking...</p></div>';
        messagesContainer.appendChild(typingDiv);
    }

    removeTypingIndicator() {
        document.getElementById('typing-indicator')?.remove();
    }

    getCurrentLanguage() {
        const selector = document.getElementById('languageSelect');
        return selector?.value || document.documentElement.lang || 'en';
    }

    renderSuggestions() {
        const wrapper = document.getElementById('chatbot-suggestions');
        if (!wrapper) return;
        const suggestions = CHATBOT_QUESTIONS[this.getCurrentLanguage()] || CHATBOT_QUESTIONS.en;
        wrapper.innerHTML = '';
        suggestions.slice(0, 3).forEach(question => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'btn btn-sm btn-outline-primary m-1';
            button.textContent = question;
            button.onclick = () => {
                document.getElementById('chat-input').value = question;
                this.sendMessage();
            };
            wrapper.appendChild(button);
        });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text || '';
        return div.innerHTML;
    }

    getUIText(language) {
        const textMap = {
            en: { placeholder: 'Ask about crop, rain, fertilizer...', send: 'Send' },
            kn: { placeholder: 'ಬೆಳೆ, ಮಳೆ, ಗೊಬ್ಬರ ಕುರಿತು ಕೇಳಿ...', send: 'ಕಳುಹಿಸಿ' },
            hi: { placeholder: 'फसल, बारिश, उर्वरक के बारे में पूछें...', send: 'भेजें' }
        };
        return textMap[language] || textMap.en;
    }

    getFallbackMessage(language) {
        const messages = {
            en: 'The agriculture assistant is offline right now. Please try again later.',
            kn: 'ಕೃಷಿ ಸಹಾಯಕ ಈಗ ಆಫ್‌ಲೈನ್ ಆಗಿದ್ದಾನೆ. ದಯವಿಟ್ಟು ಸ್ವಲ್ಪ ಸಮಯದ ನಂತರ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',
            hi: 'कृषि सहायक अभी ऑफलाइन है। कृपया थोड़ी देर बाद फिर से प्रयास करें।'
        };
        return messages[language] || messages.en;
    }
}

const CHATBOT_QUESTIONS = {
    en: [
        'How do I improve crop yield?',
        'Will rain affect my crop this week?',
        'Which fertilizer should I use?',
        'How often should I irrigate?'
    ],
    kn: [
        'ಬೆಳೆ ಇಳುವರಿ ಹೆಚ್ಚಿಸಲು ಏನು ಮಾಡಬೇಕು?',
        'ಈ ವಾರ ಮಳೆ ಬರುತ್ತದೆನಾ?',
        'ಯಾವ ಗೊಬ್ಬರ ಬಳಸುವುದು ಉತ್ತಮ?',
        'ನೀರಾವರಿ ಎಷ್ಟು ದಿನಕ್ಕೊಮ್ಮೆ ಮಾಡಬೇಕು?'
    ],
    hi: [
        'फसल की उपज कैसे बढ़ाऊं?',
        'क्या इस हफ्ते बारिश होगी?',
        'कौन सा उर्वरक उपयोग करूं?',
        'सिंचाई कितनी बार करनी चाहिए?'
    ]
};

let globalChatbot = null;

function initializeChatbot(containerId, options = {}) {
    globalChatbot = new AgriculturalChatbot(containerId, options);
    return globalChatbot;
}
