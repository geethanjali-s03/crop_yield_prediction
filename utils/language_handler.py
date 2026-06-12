"""
Language Handler
Multi-language support for English, Kannada, and Hindi
"""

TRANSLATIONS = {
    'en': {
        'welcome': 'Welcome to CropYield AI',
        'dashboard': 'Dashboard',
        'predict_crop': 'Predict Crop',
        'predict_yield': 'Predict Yield',
        'recommendations': 'Recommendations',
        'chatbot': 'Agricultural Assistant',
        'history': 'History',
        'admin': 'Admin Panel',
        'logout': 'Logout',
        'login': 'Login',
        'register': 'Register',
        'username': 'Username',
        'password': 'Password',
        'email': 'Email',
        'education_level': 'Education Level',
        'literate': 'Literate',
        'illiterate': 'Illiterate (Simple Interface)',
        'location': 'Location',
        'enter_location': 'Enter Your Location',
        'use_current_location': 'Use Current Location',
        'select_on_map': 'Select on Map',
        'submit': 'Submit',
        'loading': 'Loading...',
        'error': 'Error',
        'success': 'Success',
        'crop': 'Crop',
        'weather': 'Weather',
        'temperature': 'Temperature',
        'humidity': 'Humidity',
        'rainfall': 'Rainfall',
        'get_recommendations': 'Get Recommendations',
        'npk_ratio': 'NPK Ratio',
        'fertilizer': 'Fertilizer',
        'pesticide': 'Pesticide',
        'irrigation': 'Irrigation',
        'yield_prediction': 'Yield Prediction',
        'predicted_yield': 'Predicted Yield',
        'ask_question': 'Ask a Question',
        'send': 'Send',
        'chat_history': 'Chat History',
        'clear_chat': 'Clear Chat',
        'user_logs': 'User Logs',
        'model_accuracy': 'Model Accuracy',
        'predictions_made': 'Predictions Made',
        'back': 'Back',
    },
    'kn': {
        'welcome': 'CropYield AI ಗೆ ಸ್ವಾಗತ',
        'dashboard': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'predict_crop': 'ಫಸಲು ಊಹಿಸಿ',
        'predict_yield': 'ಇಳುವರಿ ಊಹಿಸಿ',
        'recommendations': 'ಶಿಫಾರಸುಗಳು',
        'chatbot': 'ಕೃಷಿ ಸಹಾಯಕ',
        'history': 'ಇತಿಹಾಸ',
        'admin': 'ನಿರ್ವಾಹಕ ಫಲಕ',
        'logout': 'ಲಾಗ್‌ಔಟ್',
        'login': 'ಲಾಗಿನ್',
        'register': 'ನೋಂದಾಯಿತಗೊಳಿಸು',
        'username': 'ಬಳಕೆದಾರ ಹೆಸರು',
        'password': 'ಪಾಸ್‌ವರ್ಡ್',
        'email': 'ಇಮೇಲ್',
        'education_level': 'ಶಿಕ್ಷಾ ಮಾರ್ಗ',
        'literate': 'ಸಾಕ್ಷರ',
        'illiterate': 'ಅನೂರ್ಜಿತ (ಸರಳ ಇಂಟರ್ಫೇಸ್)',
        'location': 'ಸ್ಥಳ',
        'enter_location': 'ನಿಮ್ಮ ಸ್ಥಳವನ್ನು ನಮೂದಿಸಿ',
        'use_current_location': 'ಪ್ರಸ್ತುತ ಸ್ಥಳ ಬಳಸಿ',
        'select_on_map': 'ನಕ್ಷೆಯಲ್ಲಿ ಆಯ್ಕೆ ಮಾಡಿ',
        'submit': 'ಸಲ್ಲಿಸಿ',
        'loading': 'ಲೋಡ್ ಆಗುತ್ತಿದೆ...',
        'error': 'ಹೋಲೆ',
        'success': 'ಯಶಸ್ವಿ',
        'crop': 'ಫಸಲು',
        'weather': 'ಹವಾಮಾನ',
        'temperature': 'ತಾಪಮಾನ',
        'humidity': 'ಆರ್ದ್ರತೆ',
        'rainfall': 'ಮಳೆ',
        'get_recommendations': 'ಶಿಫಾರಸುಗಳನ್ನು ಪಡೆಯಿರಿ',
        'npk_ratio': 'NPK ಅನುಪಾತ',
        'fertilizer': 'ರಸಾಯನಿಕ',
        'pesticide': 'ಕೀಟನಾಶಕ',
        'irrigation': 'ನೀರಿನ ಸಾಧನ',
        'yield_prediction': 'ಇಳುವರಿ ಊಹೆ',
        'predicted_yield': 'ಊಹಿಸಿದ ಇಳುವರಿ',
        'ask_question': 'ಪ್ರಶ್ನೆ ಕೇಳಿ',
        'send': 'ಕಳುಹಿಸಿ',
        'chat_history': 'ಚಾಟ್ ಇತಿಹಾಸ',
        'clear_chat': 'ಚಾಟ್ ಸ್ವಚ್ಛ ಮಾಡಿ',
        'user_logs': 'ಬಳಕೆದಾರ ಲಾಗ್‌ಗಳು',
        'model_accuracy': 'ಮಾದರಿ ನಿಖುರತೆ',
        'predictions_made': 'ಕಥೆಗಳನ್ನು ಮಾಡಿದೆ',
        'back': 'ಹಿಂದಿರುಗಿ',
    },
    'hi': {
        'welcome': 'CropYield AI में आपका स्वागत है',
        'dashboard': 'डैशबोर्ड',
        'predict_crop': 'फसल की भविष्यवाणी करें',
        'predict_yield': 'उपज की भविष्यवाणी करें',
        'recommendations': 'सिफारिशें',
        'chatbot': 'कृषि सहायक',
        'history': 'इतिहास',
        'admin': 'प्रशासक पैनल',
        'logout': 'लॉगआउट',
        'login': 'लॉगिन',
        'register': 'पंजीकरण करें',
        'username': 'उपयोगकर्ता नाम',
        'password': 'पासवर्ड',
        'email': 'ईमेल',
        'education_level': 'शिक्षा स्तर',
        'literate': 'साक्षर',
        'illiterate': 'निरक्षर (सरल इंटरफेस)',
        'location': 'स्थान',
        'enter_location': 'अपना स्थान दर्ज करें',
        'use_current_location': 'वर्तमान स्थान का उपयोग करें',
        'select_on_map': 'मानचित्र पर चुनें',
        'submit': 'सबमिट करें',
        'loading': 'लोड हो रहा है...',
        'error': 'त्रुटि',
        'success': 'सफल',
        'crop': 'फसल',
        'weather': 'मौसम',
        'temperature': 'तापमान',
        'humidity': 'आर्द्रता',
        'rainfall': 'वर्षा',
        'get_recommendations': 'सिफारिशें प्राप्त करें',
        'npk_ratio': 'NPK अनुपात',
        'fertilizer': 'उर्वरक',
        'pesticide': 'कीटनाशक',
        'irrigation': 'सिंचाई',
        'yield_prediction': 'उपज की भविष्यवाणी',
        'predicted_yield': 'अनुमानित उपज',
        'ask_question': 'प्रश्न पूछें',
        'send': 'भेजें',
        'chat_history': 'चैट इतिहास',
        'clear_chat': 'चैट साफ करें',
        'user_logs': 'उपयोगकर्ता लॉग',
        'model_accuracy': 'मॉडल सटीकता',
        'predictions_made': 'भविष्यवाणियां की गईं',
        'back': 'वापस',
    }
}

def get_translation(language_code, key, default=None):
    """Get translation for a key in specified language"""
    language_code = language_code or 'en'
    
    if language_code not in TRANSLATIONS:
        language_code = 'en'
    
    translations = TRANSLATIONS[language_code]
    return translations.get(key, default or key)

def get_language_name(language_code):
    """Get readable name of language"""
    names = {
        'en': 'English',
        'kn': 'ಕನ್ನಡ',
        'hi': 'हिंदी'
    }
    return names.get(language_code, 'English')

def get_all_translations(language_code):
    """Get all translations for a language"""
    language_code = language_code or 'en'
    
    if language_code not in TRANSLATIONS:
        language_code = 'en'
    
    return TRANSLATIONS[language_code]

def add_translation(language_code, key, value):
    """Add or update a translation"""
    if language_code not in TRANSLATIONS:
        TRANSLATIONS[language_code] = {}
    
    TRANSLATIONS[language_code][key] = value

def get_supported_languages():
    """Get list of supported languages"""
    return {
        'en': 'English',
        'kn': 'ಕನ್ನಡ (Kannada)',
        'hi': 'हिंदी (Hindi)'
    }
