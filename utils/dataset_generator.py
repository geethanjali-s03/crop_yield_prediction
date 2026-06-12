import pandas as pd
import numpy as np
import os

def generate_crop_dataset(n=2000):
    np.random.seed(42)
    crops = ['Rice','Wheat','Maize','Cotton','Sugarcane','Soybean','Groundnut','Barley','Jowar','Bajra']
    soil_types = ['Clay','Sandy','Loamy','Silty','Chalky','Peaty']
    seasons = ['Kharif','Rabi','Zaid','Summer','Winter']
    weather = ['Sunny','Rainy','Cloudy','Humid','Dry']
    states = ['Punjab','Haryana','UP','MP','Maharashtra','Karnataka','AP','Gujarat','Rajasthan','Bihar']

    crop_base_yield = {
        'Rice':3500,'Wheat':3200,'Maize':2800,'Cotton':1500,'Sugarcane':70000,
        'Soybean':1800,'Groundnut':2200,'Barley':2600,'Jowar':1400,'Bajra':1600
    }

    data = []
    for _ in range(n):
        crop = np.random.choice(crops)
        soil = np.random.choice(soil_types)
        season = np.random.choice(seasons)
        weather_c = np.random.choice(weather)
        state = np.random.choice(states)
        area = np.random.uniform(0.5, 50.0)
        rainfall = np.random.uniform(200, 2500)
        temperature = np.random.uniform(15, 45)
        humidity = np.random.uniform(20, 95)
        fertilizer = np.random.uniform(50, 500)
        pesticide = np.random.uniform(0.1, 5.0)

        base = crop_base_yield[crop]
        rain_factor = 1 + 0.0002 * (rainfall - 800)
        temp_factor = 1 - 0.01 * abs(temperature - 25)
        hum_factor = 1 + 0.002 * (humidity - 50)
        fert_factor = 1 + 0.001 * (fertilizer - 150)
        pest_factor = 1 + 0.05 * pesticide
        noise = np.random.normal(1, 0.1)

        yield_per_hec = max(100, base * rain_factor * temp_factor * hum_factor * fert_factor * pest_factor * noise)
        total_yield = yield_per_hec * area

        data.append({
            'Crop': crop, 'State': state, 'Season': season, 'Soil_Type': soil,
            'Weather_Condition': weather_c, 'Area': round(area, 2),
            'Rainfall': round(rainfall, 1), 'Temperature': round(temperature, 1),
            'Humidity': round(humidity, 1), 'Fertilizer_Usage': round(fertilizer, 1),
            'Pesticide_Usage': round(pesticide, 2), 'Yield_Per_Hectare': round(yield_per_hec, 2),
            'Total_Yield': round(total_yield, 2)
        })
    df = pd.DataFrame(data)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/crop_yield_dataset.csv', index=False)
    return df

if __name__ == '__main__':
    df = generate_crop_dataset()
    print(f"Dataset generated: {df.shape}")
    print(df.head())
