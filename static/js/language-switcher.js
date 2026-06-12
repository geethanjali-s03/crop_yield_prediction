/* ============================================
   CropYield AI - Language Switcher
   Multi-language support
   ============================================ */

class LanguageSwitcher {
    constructor() {
        this.currentLanguage = this.loadLanguage();
        this.translations = {};
        this.initializeLanguageSelector();
    }
    
    loadLanguage() {
        return localStorage.getItem('app_language') || 'en';
    }
    
    setLanguage(languageCode) {
        this.currentLanguage = languageCode;
        localStorage.setItem('app_language', languageCode);
        document.documentElement.lang = languageCode;
        this.updatePageLanguage();
        this.onLanguageChange?.(languageCode);
    }
    
    updatePageLanguage() {
        // Update voice input language
        if (typeof voiceInput !== 'undefined') {
            const languageMap = {
                'en': 'en-US',
                'kn': 'kn-IN',
                'hi': 'hi-IN'
            };
            voiceInput.setLanguage(languageMap[this.currentLanguage] || 'en-US');
        }
        
        // Update interface language
        this.updateUI();
        
        // Reload page to update all text
        window.location.reload();
    }
    
    initializeLanguageSelector() {
        const selector = document.getElementById('language-selector');
        if (!selector) return;
        
        const options = {
            'en': 'English',
            'kn': 'ಕನ್ನಡ',
            'hi': 'हिंदी'
        };
        
        for (const [code, name] of Object.entries(options)) {
            const button = document.createElement('button');
            button.className = `language-option ${code === this.currentLanguage ? 'active' : ''}`;
            button.textContent = name;
            button.onclick = () => this.setLanguage(code);
            selector.appendChild(button);
        }
    }
    
    updateUI() {
        // Update all elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            element.textContent = this.translate(key);
        });
        
        // Update placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            element.placeholder = this.translate(key);
        });
    }
    
    translate(key) {
        // Placeholder for server-side translation
        // This will be replaced with actual translations from server
        return key;
    }
    
    onLanguageChange = null;
}

// Keyboard shortcut for language switching
document.addEventListener('keydown', (e) => {
    // Alt + 1 = English, Alt + 2 = Kannada, Alt + 3 = Hindi
    if (e.altKey) {
        const languageMap = {
            '1': 'en',
            '2': 'kn',
            '3': 'hi'
        };
        
        if (languageMap[e.key]) {
            languageSwitcher.setLanguage(languageMap[e.key]);
        }
    }
});

// Global instance
const languageSwitcher = new LanguageSwitcher();

// Helper function to get current language
function getCurrentLanguage() {
    return languageSwitcher.currentLanguage;
}

// Helper function to set language
function setLanguage(code) {
    languageSwitcher.setLanguage(code);
}

// Get all available languages
function getAvailableLanguages() {
    return {
        'en': 'English',
        'kn': 'ಕನ್ನಡ (Kannada)',
        'hi': 'हिंदी (Hindi)'
    };
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Set page language
    document.documentElement.lang = languageSwitcher.currentLanguage;
    
    // Update interface
    languageSwitcher.updateUI();
    
    // Add keyboard help
    const helpText = document.createElement('div');
    helpText.className = 'language-help';
    helpText.style.fontSize = '0.8rem';
    helpText.style.opacity = '0.6';
    helpText.innerHTML = 'Language: Alt+1 (English) | Alt+2 (ಕನ್ನಡ) | Alt+3 (हिंदी)';
    
    const footer = document.querySelector('footer');
    if (footer) footer.appendChild(helpText);
});
