/* ============================================
   CropYield AI - Voice Input Handler
   Uses Web Speech API for voice recognition
   ============================================ */

class VoiceInputHandler {
    constructor() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = SpeechRecognition ? new SpeechRecognition() : null;
        this.isListening = false;
        this.transcript = '';
        if (this.recognition) {
            this.setupRecognition();
        }
    }
    
    setupRecognition() {
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.language = 'en-US';
        
        this.recognition.onstart = () => {
            this.isListening = true;
            this.onStart?.();
        };
        
        this.recognition.onresult = (event) => {
            let interim = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    this.transcript += transcript + ' ';
                } else {
                    interim += transcript;
                }
            }
            this.onResult?.(this.transcript + interim);
        };
        
        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.onError?.(event.error);
        };
        
        this.recognition.onend = () => {
            this.isListening = false;
            this.onEnd?.(this.transcript);
        };
    }
    
    startListening(language = 'en-US') {
        if (!this.recognition) {
            this.onError?.('Speech recognition is not supported in this browser');
            return;
        }
        this.recognition.language = language;
        this.transcript = '';
        try {
            this.recognition.start();
        } catch (e) {
            console.error('Error starting recognition:', e);
        }
    }
    
    stopListening() {
        if (!this.recognition) return;
        this.recognition.stop();
    }
    
    setLanguage(language) {
        const languageMap = {
            'en': 'en-US',
            'kn': 'kn-IN',
            'hi': 'hi-IN'
        };
        this.recognition.language = languageMap[language] || 'en-US';
    }
    
    // Callbacks
    onStart = null;
    onResult = null;
    onError = null;
    onEnd = null;
}

// Text to Speech
class TextToSpeech {
    constructor() {
        this.synth = window.speechSynthesis;
        this.isSpeaking = false;
    }
    
    speak(text, language = 'en-US') {
        if (this.isSpeaking) {
            this.synth.cancel();
        }
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.language = language;
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        utterance.onstart = () => {
            this.isSpeaking = true;
            this.onStart?.();
        };
        
        utterance.onend = () => {
            this.isSpeaking = false;
            this.onEnd?.();
        };
        
        this.synth.speak(utterance);
    }
    
    stop() {
        this.synth.cancel();
        this.isSpeaking = false;
    }
    
    onStart = null;
    onEnd = null;
}

// Global instances
const voiceInput = new VoiceInputHandler();
const textSpeech = new TextToSpeech();

// Helper function to attach voice button
function attachVoiceButton(inputElementId, buttonElementId) {
    const inputElement = document.getElementById(inputElementId);
    const button = document.getElementById(buttonElementId);
    
    if (!button || !inputElement) return;
    
    button.addEventListener('click', () => {
        if (!voiceInput.isListening) {
            voiceInput.startListening();
            button.classList.add('recording');
            button.innerHTML = '<i class="bi bi-record-circle me-1"></i>Listening';
        } else {
            voiceInput.stopListening();
            button.classList.remove('recording');
            button.innerHTML = '<i class="bi bi-mic"></i>';
        }
    });
    
    voiceInput.onResult = (text) => {
        inputElement.value = text;
    };
    
    voiceInput.onEnd = (transcript) => {
        inputElement.value = transcript;
        button.classList.remove('recording');
        button.innerHTML = '<i class="bi bi-mic"></i>';
    };
    
    voiceInput.onError = (error) => {
        console.error('Voice input error:', error);
        button.classList.remove('recording');
        button.innerHTML = '<i class="bi bi-mic-mute"></i>';
        showAlert(`Voice input error: ${error}`, 'danger');
    };
}

// Helper function for text-to-speech
function speakText(text, language = 'en-US') {
    textSpeech.speak(text, language);
}

// Check browser support
function isVoiceInputSupported() {
    return !!(window.SpeechRecognition || window.webkitSpeechRecognition);
}

function isTextToSpeechSupported() {
    return !!window.speechSynthesis;
}

// Initialize voice features on page load
document.addEventListener('DOMContentLoaded', () => {
    if (!isVoiceInputSupported()) {
        console.warn('Speech Recognition API not supported');
    }
    if (!isTextToSpeechSupported()) {
        console.warn('Text-to-Speech API not supported');
    }
});
