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
CEREBRAS_API_KEY = os.environ.get('CEREBRAS_API_KEY', '')
CEREBRAS_API_URL = "https://api.cerebras.ai/v1/chat/completions"

class CerebrasAIClient:
    """Cerebras AI API Client for Agricultural Chatbot"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or CEREBRAS_API_KEY
        self.model = "llama-3.1-8b"
        self.base_url = "https://api.cerebras.ai/v1"
        self.conversation_history = []
    
    def is_available(self):
        """Check if API key is configured"""
        return bool(self.api_key)
    
    def ask_agricultural_question(self, question, language='en'):
        """
        Ask agriculture-related question to Cerebras AI
        Returns structured response with answer and recommendations
        """
        if not self.is_available():
            return {
                'status': 'error',
                'message': 'Cerebras API not configured. Please add API key to .env file',
                'answer': 'I am currently offline. Please try again later.'
            }
        
        try:
            # Prepare system prompt for agricultural context
            system_prompt = self._get_agricultural_system_prompt(language)
            
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
            
            response.raise_for_status()
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
                'answer': answer,
                'timestamp': datetime.now().isoformat()
            }
        
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'message': f'API Error: {str(e)}',
                'question': question,
                'answer': 'Sorry, I could not process your question at this time.'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error: {str(e)}',
                'question': question,
                'answer': 'An unexpected error occurred.'
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
        
        Keep response concise and practical for farmers."""
        
        return self.ask_agricultural_question(prompt, language)
    
    def get_weather_advisory(self, weather_condition, crop, region, language='en'):
        """Get weather-based advisory for farming"""
        prompt = f"""Given {weather_condition} weather conditions in {region}, 
        provide advisory for {crop} farming:
        1. Immediate actions needed
        2. Pest/disease risks
        3. Irrigation recommendations
        4. Harvesting implications
        Keep it practical and actionable."""
        
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
        5. Sustainable practices"""
        
        return self.ask_agricultural_question(prompt, language)
    
    def _get_agricultural_system_prompt(self, language='en'):
        """Get system prompt for agricultural context"""
        prompts = {
            'en': """You are an experienced agricultural extension officer helping farmers.
            Provide practical, evidence-based advice on:
            - Crop selection and cultivation
            - Pest and disease management
            - Soil and water management
            - Fertilizer and nutrient management
            - Yield improvement techniques
            - Weather-based farming decisions
            
            Keep responses concise, clear, and actionable for farmers with varying education levels.
            Use local knowledge and proven practices.""",
            
            'kn': """You are an experienced agricultural extension officer. Provide practical advice in Kannada on farming topics.
            Respond in Kannada language.""",
            
            'hi': """You are an experienced agricultural extension officer. Provide practical advice in Hindi on farming topics.
            Respond in Hindi language."""
        }
        
        return prompts.get(language, prompts['en'])
    
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
