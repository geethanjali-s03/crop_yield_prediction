/* ============================================
   CropYield AI - Chatbot Handler
   Integrates with Cerebras AI API
   ============================================ */

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
        
        container.innerHTML = `
            <div class="chat-container">
                <div class="chat-messages" id="chat-messages"></div>
                <div class="chat-input">
                    <input type="text" id="chat-input" placeholder="Ask a question..." />
                    <button id="chat-send" class="btn btn-primary btn-sm">Send</button>
                </div>
            </div>
        `;
        
        const inputElement = document.getElementById('chat-input');
        const sendButton = document.getElementById('chat-send');
        
        sendButton.addEventListener('click', () => this.sendMessage());
        inputElement.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }
    
    async sendMessage() {
        const inputElement = document.getElementById('chat-input');
        const message = inputElement.value.trim();
        
        if (!message) return;
        
        // Add user message to display
        this.addMessage(message, 'user');
        inputElement.value = '';
        
        // Send to server
        try {
            this.isLoading = true;
            this.showTypingIndicator();
            
            const response = await fetch(this.options.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    question: message,
                    language: this.getCurrentLanguage()
                })
            });
            
            if (!response.ok) throw new Error('Chat request failed');
            
            const data = await response.json();
            this.removeTypingIndicator();
            
            if (data.status === 'success') {
                this.addMessage(data.answer, 'bot');
                if (this.options.enableSound) {
                    this.playResponseSound();
                }
            } else {
                this.addMessage('Sorry, I could not process your question. Please try again.', 'bot');
            }
        } catch (error) {
            console.error('Chat error:', error);
            this.removeTypingIndicator();
            this.addMessage('Error connecting to chat service. Please try again later.', 'bot');
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
        
        // Auto-scroll to bottom
        if (this.options.autoScroll) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        this.messages.push({text, sender, timestamp: new Date()});
    }
    
    showTypingIndicator() {
        const messagesContainer = document.getElementById('chat-messages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing-indicator';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="content">
                <div class="loader"></div>
                <div class="loader"></div>
                <div class="loader"></div>
            </div>
        `;
        messagesContainer.appendChild(typingDiv);
        
        if (this.options.autoScroll) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }
    
    removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    }
    
    getCurrentLanguage() {
        return document.documentElement.lang || 'en';
    }
    
    clearChat() {
        const messagesContainer = document.getElementById('chat-messages');
        if (messagesContainer) messagesContainer.innerHTML = '';
        this.messages = [];
    }
    
    getHistory() {
        return this.messages;
    }
    
    exportHistory() {
        return JSON.stringify(this.messages, null, 2);
    }
    
    playResponseSound() {
        // Play a subtle notification sound
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.1);
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Question Templates for Easy Access
const CHATBOT_QUESTIONS = {
    'en': [
        'How do I improve crop yield?',
        'What are the best fertilizers for my region?',
        'How should I irrigate my field?',
        'What pests should I watch for?',
        'When should I harvest my crop?',
        'How do I prevent crop diseases?'
    ],
    'kn': [
        'ನನ್ನ ಫಸಲಿನ ಇಳುವರಿ ಹೇಗೆ ಹೆಚ್ಚಿಸುವುದು?',
        'ನನ್ನ ಪ್ರದೇಶಕ್ಕೆ ಉತ್ತಮ ರಸಾಯನಿಕಗಳು ಯಾವುವು?',
        'ನಾನು ನನ್ನ ಹೊಲವನ್ನು ಹೇಗೆ ನೀರಾವರಿ ಮಾಡಬೇಕು?',
        'ನಾನು ಯಾವ ಕೀಟಗಳನ್ನು ಧ್ಯಾನಿಸಿ ನೋಡಬೇಕು?',
        'ನಾನು ನನ್ನ ಫಸಲನ್ನು ಹೇಗೆ ಕೊಯ್ಯುವುದು?',
        'ನಾನು ಫಸಲಿನ ರೋಗಗಳನ್ನು ಹೇಗೆ ತಡೆಯುವುದು?'
    ],
    'hi': [
        'मैं अपनी फसल की पैदावार कैसे बढ़ा सकता हूं?',
        'मेरे क्षेत्र के लिए सर्वोत्तम उर्वरक कौन से हैं?',
        'मुझे अपनी खेत को कैसे सिंचित करना चाहिए?',
        'मुझे किन कीटों पर ध्यान देना चाहिए?',
        'मुझे अपनी फसल कब काटनी चाहिए?',
        'मैं फसल की बीमारियों को कैसे रोक सकता हूं?'
    ]
};

// Global chatbot instance
let globalChatbot = null;

// Initialize chatbot on page load
function initializeChatbot(containerId, options = {}) {
    globalChatbot = new AgriculturalChatbot(containerId, options);
    return globalChatbot;
}

// Add quick question button
function addQuickQuestion(question) {
    if (globalChatbot) {
        const inputElement = document.getElementById('chat-input');
        if (inputElement) {
            inputElement.value = question;
            globalChatbot.sendMessage();
        }
    }
}

// Display suggestion buttons
function showChatbotSuggestions(language = 'en') {
    const suggestions = CHATBOT_QUESTIONS[language] || CHATBOT_QUESTIONS['en'];
    const container = document.createElement('div');
    container.className = 'chatbot-suggestions';
    container.innerHTML = '<p>Quick Questions:</p>';
    
    suggestions.forEach(q => {
        const btn = document.createElement('button');
        btn.className = 'btn btn-sm btn-outline-primary';
        btn.textContent = q;
        btn.onclick = () => addQuickQuestion(q);
        container.appendChild(btn);
    });
    
    return container;
}

// Chat history management
const ChatHistory = {
    save: function(key = 'chatbot_history') {
        if (globalChatbot) {
            localStorage.setItem(key, globalChatbot.exportHistory());
        }
    },
    
    load: function(key = 'chatbot_history') {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : [];
    },
    
    clear: function(key = 'chatbot_history') {
        localStorage.removeItem(key);
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Look for chat container
    const chatContainer = document.getElementById('chatbot-container');
    if (chatContainer) {
        initializeChatbot('chatbot-container', {
            enableSound: localStorage.getItem('chatbot_sound') === 'true'
        });
    }
});
