"""
Recommendations Engine
Provides NPK, Fertilizer, Pesticide, and Irrigation recommendations
"""
from config import Config

class RecommendationEngine:
    """Generate recommendations based on crop and conditions"""
    
    def __init__(self):
        self.npk_data = Config.NPK_RECOMMENDATIONS
        self.fertilizer_types = Config.FERTILIZER_TYPES
        self.pesticide_data = Config.PESTICIDE_RECOMMENDATIONS
        self.irrigation_data = Config.IRRIGATION_SCHEDULE
    
    def get_npk_recommendation(self, crop):
        """Get NPK ratio recommendation for crop"""
        return self.npk_data.get(crop, {
            'N': '50-100',
            'P': '30-60',
            'K': '30-60'
        })
    
    def get_fertilizer_recommendation(self, crop, soil_type, weather):
        """
        Recommend fertilizer based on crop and conditions
        Returns: List of recommended fertilizers with rationale
        """
        recommendations = []
        npk = self.get_npk_recommendation(crop)
        
        # Extract N value (take average of range)
        try:
            n_range = npk['N'].split('-')
            n_value = (int(n_range[0]) + int(n_range[1])) // 2
        except:
            n_value = 60
        
        # Recommend based on N content
        if n_value > 100:
            fert_type = 'high_nitrogen'
            rationale = f"High nitrogen requirement ({n_value} kg/ha) for {crop}"
        elif n_value < 30:
            fert_type = 'low_nitrogen'
            rationale = f"Crop {crop} (legume/pulse) requires minimal nitrogen"
        else:
            fert_type = 'balanced'
            rationale = f"Balanced fertilizer recommended for {crop}"
        
        if fert_type in self.fertilizer_types:
            for fertilizer in self.fertilizer_types[fert_type][:3]:
                recommendations.append({
                    'fertilizer': fertilizer,
                    'npk_ratio': npk,
                    'quantity_per_hectare': f"{n_value} kg/ha",
                    'rationale': rationale,
                    'application_time': self._get_application_timing(crop)
                })
        
        return recommendations
    
    def get_pesticide_recommendation(self, crop, season, weather):
        """
        Recommend pesticides based on crop and season
        Weather influences pest patterns
        """
        base_pesticides = self.pesticide_data.get(crop, [
            'Neem Oil',
            'Insecticidal Soap',
            'Pyrethrin'
        ])
        
        recommendations = []
        
        # Wet weather promotes fungal diseases
        if weather == 'Rainy':
            additional = ['Mancozeb', 'Carbendazim', 'Propiconazole']
            reason = "Rainy season - fungal disease prevention"
        # Dry weather promotes pest infestations
        elif weather == 'Dry':
            additional = ['Spinosad', 'Neem Oil']
            reason = "Dry season - insect pest control"
        else:
            additional = []
            reason = "Regular pest management"
        
        combined = list(set(base_pesticides + additional))[:5]
        
        for pesticide in combined:
            recommendations.append({
                'pesticide': pesticide,
                'type': self._get_pesticide_type(pesticide),
                'dosage': self._get_dosage(pesticide),
                'frequency': self._get_spray_frequency(season),
                'reason': reason,
                'safety_period': self._get_safety_period(pesticide)
            })
        
        return recommendations
    
    def get_irrigation_schedule(self, crop, season, rainfall, temperature):
        """
        Recommend irrigation schedule based on conditions
        """
        schedule = self.irrigation_data.get(crop, {
            'frequency': 'Every 15-20 days',
            'depth': '50mm',
            'season': 'General'
        })
        
        recommendations = {
            'base_schedule': schedule,
            'adjustments': [],
            'total_water_per_season': 0
        }
        
        # Adjust for rainfall
        if rainfall > 50:  # High rainfall
            recommendations['adjustments'].append(
                "Reduce frequency by 20-30% due to high rainfall"
            )
            recommendations['adjusted_frequency'] = "Reduce irrigation as needed"
        elif rainfall < 20:  # Low rainfall
            recommendations['adjustments'].append(
                "Increase frequency by 10-20% due to low rainfall"
            )
            recommendations['adjusted_frequency'] = "Increase irrigation frequency"
        
        # Adjust for temperature
        if temperature > 35:  # High temperature
            recommendations['adjustments'].append(
                "Increase irrigation frequency due to high evaporation"
            )
        elif temperature < 15:  # Low temperature
            recommendations['adjustments'].append(
                "Reduce irrigation frequency due to low evaporation"
            )
        
        # Calculate water requirement
        recommendations['water_requirement_per_application'] = schedule['depth']
        recommendations['season_duration_days'] = self._get_season_duration(season)
        
        return recommendations
    
    def get_comprehensive_recommendation(self, crop, soil_type, season, weather, rainfall, temperature):
        """
        Get all recommendations in one call
        """
        return {
            'crop': crop,
            'conditions': {
                'soil_type': soil_type,
                'season': season,
                'weather': weather,
                'rainfall': rainfall,
                'temperature': temperature
            },
            'npk': self.get_npk_recommendation(crop),
            'fertilizers': self.get_fertilizer_recommendation(crop, soil_type, weather),
            'pesticides': self.get_pesticide_recommendation(crop, season, weather),
            'irrigation': self.get_irrigation_schedule(crop, season, rainfall, temperature),
            'additional_tips': self._get_additional_tips(crop, season)
        }
    
    # Helper methods
    def _get_application_timing(self, crop):
        """Get optimal timing for fertilizer application"""
        timing = {
            'Rice': 'At planting, early growth, and panicle initiation',
            'Wheat': 'At sowing and tillering stage',
            'Maize': 'At planting and V8-V10 growth stage',
            'Cotton': 'At flowering and boll development',
            'Sugarcane': 'At planting and monsoon onset'
        }
        return timing.get(crop, 'As per local recommendations')
    
    def _get_pesticide_type(self, pesticide):
        """Categorize pesticide type"""
        if 'Neem' in pesticide or 'Organic' in pesticide:
            return 'Organic'
        elif 'Oil' in pesticide or 'Soap' in pesticide:
            return 'Bio-pesticide'
        else:
            return 'Chemical'
    
    def _get_dosage(self, pesticide):
        """Get recommended dosage for pesticide"""
        dosages = {
            'Neem Oil': '30-50 ml/litre water',
            'Carbofuran': '500g-1kg/hectare',
            'Imidacloprid': '500ml/hectare',
            'Spinosad': '500ml/hectare',
            'Thiamethoxam': '250g/hectare'
        }
        return dosages.get(pesticide, '1-2 kg/hectare')
    
    def _get_spray_frequency(self, season):
        """Get recommended spray frequency"""
        return '7-14 days interval' if season in ['Kharif', 'Rabi'] else '10-15 days interval'
    
    def _get_safety_period(self, pesticide):
        """Get days before harvest to stop spraying"""
        safety_periods = {
            'Neem Oil': '0-3 days',
            'Organic Pesticides': '0-3 days',
            'Imidacloprid': '7-10 days',
            'Carbofuran': '15 days',
            'Spinosad': '7-10 days'
        }
        return safety_periods.get(pesticide, '10-15 days')
    
    def _get_season_duration(self, season):
        """Get approximate duration of growing season"""
        durations = {
            'Kharif': 120,
            'Rabi': 140,
            'Zaid': 90,
            'Summer': 100,
            'Winter': 150
        }
        return durations.get(season, 120)
    
    def _get_additional_tips(self, crop, season):
        """Get additional cultivation tips"""
        tips = {
            'Rice': [
                'Maintain water level of 5-7 cm during growing season',
                'Apply first fertilizer at 20-25 days after transplanting',
                'Monitor for pests like stem borer and brown planthopper'
            ],
            'Wheat': [
                'Sow 20-25 kg seeds per hectare',
                'Apply first irrigation at CRI (Crown Root Initiation) stage',
                'Control weeds through herbicides or manual weeding'
            ],
            'Maize': [
                'Use quality seeds with high germination rate',
                'Maintain plant population of 60,000-80,000 plants/hectare',
                'Harvest when moisture content reaches 20-25%'
            ],
            'Cotton': [
                'Provide proper spacing (60x90 cm)',
                'Regular hoeing and weeding for first 90 days',
                'Pick cotton at peak maturity for better quality'
            ],
            'Sugarcane': [
                'Plant cane at 75 cm spacing',
                'Provide 8-10 irrigations during season',
                'Harvest at 12 months for higher sucrose content'
            ]
        }
        return tips.get(crop, ['Follow regional guidelines for optimal results'])

# Create singleton instance
recommendation_engine = RecommendationEngine()
