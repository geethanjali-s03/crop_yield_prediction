"""
External API Integrations
Integrates with Cerebras AI for chatbot and other APIs
"""
import requests
import json
from datetime import datetime
import os
from config import Config

# Cerebras API Configuration
CEREBRAS_API_KEY = Config.CEREBRAS_API_KEY
CEREBRAS_API_URL = "https://api.cerebras.ai/v1/chat/completions"

class CerebrasAIClient:
    """Cerebras AI API Client for Agricultural Chatbot"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or CEREBRAS_API_KEY
        self.model = os.environ.get('CEREBRAS_MODEL', 'gpt-oss-120b')
        self.base_url = "https://api.cerebras.ai/v1"
        self.conversation_history = []
    
    def is_available(self):
        """Check if API key is configured"""
        return bool(self.api_key)
    
    def ask_agricultural_question(self, question, language='en', education_level='literate'):
        """
        Ask agriculture-related question to Cerebras AI
        Returns structured response with answer and recommendations
        """
        if not self.is_available():
            return {
                'status': 'error',
                'message': 'Cerebras API not configured. Please add API key to .env file',
                'answer': self._get_fallback_answer(language, question, education_level)
            }
        
        try:
            # Prepare system prompt for agricultural context
            system_prompt = self._get_agricultural_system_prompt(language, education_level)
            
            # Build messages
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
            
            # Call Cerebras API
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": 1024,
                    "temperature": 0.7
                },
                timeout=30
            )

            if not response.ok:
                raise requests.exceptions.RequestException(
                    f"HTTP {response.status_code}: {response.text.strip() or response.reason}"
                )

            result = response.json()
            
            answer = result['choices'][0]['message']['content']
            
            # Store conversation history
            self.conversation_history.append({
                'question': question,
                'answer': answer,
                'timestamp': datetime.now().isoformat(),
                'language': language
            })
            
            return {
                'status': 'success',
                'question': question,
                'answer': self._post_process_answer(answer, language, education_level),
                'timestamp': datetime.now().isoformat()
            }
        
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'message': f'API Error: {str(e)}',
                'question': question,
                'answer': self._get_fallback_answer(language, question, education_level)
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error: {str(e)}',
                'question': question,
                'answer': self._get_fallback_answer(language, question, education_level)
            }
    
    def get_crop_information(self, crop_name, language='en'):
        """Get detailed information about a specific crop"""
        prompt = f"""Provide comprehensive information about {crop_name} cultivation:
        1. Climate and weather requirements
        2. Soil type and preparation
        3. Planting method and spacing
        4. Water requirements and irrigation schedule
        5. Fertilizer and nutrient requirements
        6. Common pests and diseases
        7. Harvesting time and yield expectations
        8. Storage and post-harvest handling
        
        Keep response concise and practical for farmers.
        If language is Kannada or Hindi, answer fully in that language."""
        
        return self.ask_agricultural_question(prompt, language)
    
    def get_weather_advisory(self, weather_condition, crop, region, language='en'):
        """Get weather-based advisory for farming"""
        prompt = f"""Given {weather_condition} weather conditions in {region}, 
        provide advisory for {crop} farming:
        1. Immediate actions needed
        2. Pest/disease risks
        3. Irrigation recommendations
        4. Harvesting implications
        Keep it practical and actionable.
        If language is Kannada or Hindi, answer fully in that language."""
        
        return self.ask_agricultural_question(prompt, language)
    
    def get_disease_identification_advice(self, symptoms, crop, language='en'):
        """Get advice for crop disease identification and management"""
        prompt = f"""A farmer reports the following symptoms on {crop}:
        {symptoms}
        
        Please provide:
        1. Possible diseases
        2. Identification tips
        3. Treatment recommendations
        4. Prevention methods
        5. When to seek expert help"""
        
        return self.ask_agricultural_question(prompt, language)
    
    def get_yield_improvement_tips(self, crop, region, season, language='en'):
        """Get tips to improve yield"""
        prompt = f"""How can farmers improve the yield of {crop} in {region} during {season}?
        Provide 5-7 practical tips considering:
        1. Regional climate
        2. Soil conditions
        3. Market demand
        4. Cost-effectiveness
        5. Sustainable practices
        If language is Kannada or Hindi, answer fully in that language."""
        
        return self.ask_agricultural_question(prompt, language)
    
    def _get_agricultural_system_prompt(self, language='en', education_level='literate'):
        """Get system prompt for agricultural context"""
        style_guidance = """
        Answer with this style:
        - Use plain words and short sentences.
        - Prefer 3 to 6 bullet points or numbered steps.
        - Give direct farming advice only.
        - If the user asks about rain, weather, fertilizer, pesticide, irrigation, crops, soil, or yield, keep the answer practical.
        - Do not add unrelated disclaimers.
        """

        simple_guidance = """
        Farmer learning mode: simple picture mode.
        - Use very simple language.
        - Keep each point short.
        - Start with the most important action.
        - Avoid scientific jargon unless needed.
        - If you can, use examples from Indian farming.
        """

        advanced_guidance = """
        Farmer learning mode: studied/science mode.
        - Include scientific reasoning when helpful.
        - Mention soil, climate, nutrient and irrigation logic.
        - Keep the answer structured and easy to scan.
        """

        prompts = {
            'en': f"""You are an experienced agricultural extension officer helping farmers.
            Provide practical, evidence-based advice on crop selection, pests, diseases, soil, water, fertilizer, irrigation, and weather decisions.
            {simple_guidance if education_level == 'illiterate' else advanced_guidance}
            {style_guidance}
            Always answer in English.""",
            
            'kn': f"""ನೀವು ಅನುಭವೀ ಕೃಷಿ ಸಲಹೆಗಾರರು.
            ಬೆಳೆ ಆಯ್ಕೆ, ಕೀಟಗಳು, ರೋಗಗಳು, ಮಣ್ಣು, ನೀರು, ಗೊಬ್ಬರ, ನೀರಾವರಿ ಮತ್ತು ಹವಾಮಾನ ಕುರಿತು ರೈತನಿಗೆ ಸರಳವಾಗಿ, ನೇರವಾಗಿ ಮತ್ತು ಉಪಯೋಗವಾಗುವಂತೆ ಸಲಹೆ ನೀಡಿ.
            {simple_guidance if education_level == 'illiterate' else advanced_guidance}
            {style_guidance}
            Always answer in Kannada only. Use simple Kannada words. Do not switch to English unless the user asks for English.""",
            
            'hi': f"""आप एक अनुभवी कृषि सलाहकार हैं।
            फसल चयन, कीट, रोग, मिट्टी, पानी, उर्वरक, सिंचाई और मौसम के बारे में किसान को सरल, सीधे और उपयोगी सुझाव दें।
            {simple_guidance if education_level == 'illiterate' else advanced_guidance}
            {style_guidance}
            हमेशा हिंदी में उत्तर दें। सरल हिंदी का उपयोग करें।"""
        }
        
        return prompts.get(language, prompts['en'])

    def _get_fallback_answer(self, language, question, education_level):
        defaults = {
            'en': 'I am offline right now. Please try again later.',
            'kn': 'ನಾನು ಈಗ ಆಫ್‌ಲೈನ್ ಆಗಿದ್ದೇನೆ. ದಯವಿಟ್ಟು ಸ್ವಲ್ಪ ಸಮಯದ ನಂತರ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',
            'hi': 'मैं अभी ऑफलाइन हूं। कृपया थोड़ी देर बाद फिर से कोशिश करें।'
        }
        base = defaults.get(language, defaults['en'])
        if education_level == 'illiterate':
            return base + ' Use the crop buttons, map, or microphone for simple input.'
        return base + ' You can ask about crop, rain, fertilizer, pesticide, or irrigation.'

    def _post_process_answer(self, answer, language, education_level):
        answer = (answer or '').strip()
        if not answer:
            return self._get_fallback_answer(language, '', education_level)

        # Keep answers short and farmer-friendly if the model drifts too long.
        lines = [line.strip() for line in answer.splitlines() if line.strip()]
        if len(lines) > 12:
            lines = lines[:12]
            lines.append('...')
        return '\n'.join(lines)
    
    def get_conversation_history(self):
        """Get conversation history"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []

class FarmerProfileAnalyzer:
    """Analyze farmer profile and provide personalized recommendations"""
    
    @staticmethod
    def get_profile_based_interface(education_level):
        """
        Determine interface complexity based on education level
        Returns configuration for UI rendering
        """
        if education_level == 'illiterate':
            return {
                'interface_type': 'simple',
                'show_pictures': True,
                'use_voice_input': True,
                'use_voice_output': True,
                'hide_statistics': True,
                'large_text': True,
                'large_buttons': True,
                'color_scheme': 'bright_green',
                'show_graphs': False,
                'simplified_language': True,
                'emoji_support': True,
                'step_by_step_guides': True,
                'max_options': 3,
                'default_language': 'kn'  # Kannada default for local farmers
            }
        else:
            return {
                'interface_type': 'advanced',
                'show_pictures': True,
                'use_voice_input': True,
                'use_voice_output': False,
                'hide_statistics': False,
                'large_text': False,
                'large_buttons': False,
                'color_scheme': 'professional_green',
                'show_graphs': True,
                'simplified_language': False,
                'emoji_support': False,
                'step_by_step_guides': False,
                'max_options': 10,
                'show_scientific_data': True,
                'advanced_analytics': True,
                'default_language': 'en'
            }
    
    @staticmethod
    def generate_profile_report(farmer_data):
        """Generate comprehensive farmer profile report"""
        return {
            'farmer_id': farmer_data.get('username'),
            'education_level': farmer_data.get('education_level', 'literate'),
            'location': farmer_data.get('location'),
            'total_predictions': farmer_data.get('prediction_count', 0),
            'preferred_crops': farmer_data.get('preferred_crops', []),
            'recent_activities': farmer_data.get('recent_activities', []),
            'recommended_next_actions': FarmerProfileAnalyzer._get_recommended_actions(farmer_data),
            'success_rate': FarmerProfileAnalyzer._calculate_success_rate(farmer_data)
        }
    
    @staticmethod
    def _get_recommended_actions(farmer_data):
        """Get recommended actions based on profile"""
        actions = []
        
        # Check crop diversity
        crops = farmer_data.get('preferred_crops', [])
        if len(crops) < 2:
            actions.append("Consider growing additional crops for crop rotation")
        
        # Check activity frequency
        recent_activities = farmer_data.get('recent_activities', [])
        if len(recent_activities) < 5:
            actions.append("Make predictions more regularly for better planning")
        
        actions.append("Review fertilizer recommendations from past predictions")
        actions.append("Check weather forecast for upcoming month")
        
        return actions
    
    @staticmethod
    def _calculate_success_rate(farmer_data):
        """Calculate success rate based on historical data"""
        total_predictions = farmer_data.get('prediction_count', 0)
        if total_predictions == 0:
            return 0
        
        successful = farmer_data.get('successful_predictions', 0)
        return (successful / total_predictions * 100) if total_predictions > 0 else 0

# Create singleton instances
cerebras_client = CerebrasAIClient()
farmer_analyzer = FarmerProfileAnalyzer()
