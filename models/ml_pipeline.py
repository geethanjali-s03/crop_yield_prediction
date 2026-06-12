import pandas as pd
import numpy as np
import joblib, os, json, warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

def train_models(df=None):
    if df is None:
        df = pd.read_csv('data/crop_yield_dataset.csv')

    df = df.dropna()
    cat_cols = ['Crop','State','Season','Soil_Type','Weather_Condition']
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    feature_cols = ['Crop','State','Season','Soil_Type','Weather_Condition',
                    'Area','Rainfall','Temperature','Humidity','Fertilizer_Usage','Pesticide_Usage']
    X = df[feature_cols]
    y = df['Yield_Per_Hectare']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    models = {
        'Linear Regression': LinearRegression(),
        'Decision Tree': DecisionTreeRegressor(max_depth=10, random_state=42),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        'XGBoost': XGBRegressor(n_estimators=100, random_state=42, verbosity=0),
        'SVM': SVR(kernel='rbf', C=100, gamma=0.1)
    }

    results = {}
    best_model_name = None
    best_r2 = -999

    for name, model in models.items():
        if name in ['SVM', 'Linear Regression']:
            model.fit(X_train_s, y_train)
            preds = model.predict(X_test_s)
        else:
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)
        acc = max(0, r2) * 100

        results[name] = {'MAE': round(mae,2),'RMSE': round(rmse,2),'R2': round(r2,4),'Accuracy': round(acc,2)}
        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name

    os.makedirs('models', exist_ok=True)
    joblib.dump(models[best_model_name], 'models/best_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(encoders, 'models/encoders.pkl')

    meta = {
        'best_model': best_model_name,
        'results': results,
        'feature_cols': feature_cols,
        'cat_cols': cat_cols,
        'encoder_classes': {col: list(encoders[col].classes_) for col in cat_cols}
    }
    with open('models/model_meta.json','w') as f:
        json.dump(meta, f)

    print(f"Best model: {best_model_name} | R²: {best_r2:.4f}")
    return meta

def predict_yield(input_data: dict) -> dict:
    with open('models/model_meta.json') as f:
        meta = json.load(f)

    model = joblib.load('models/best_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    encoders = joblib.load('models/encoders.pkl')

    row = {}
    for col in meta['cat_cols']:
        val = input_data.get(col,'')
        classes = list(encoders[col].classes_)
        if val in classes:
            row[col] = classes.index(val)
        else:
            row[col] = 0

    num_cols = ['Area','Rainfall','Temperature','Humidity','Fertilizer_Usage','Pesticide_Usage']
    for col in num_cols:
        row[col] = float(input_data.get(col, 0))

    X = pd.DataFrame([row])[meta['feature_cols']]
    best = meta['best_model']
    if best in ['SVM','Linear Regression']:
        X_s = scaler.transform(X)
        pred = model.predict(X_s)[0]
    else:
        pred = model.predict(X)[0]

    total = pred * row['Area']
    r2 = meta['results'][best]['R2']
    confidence = round(max(0, r2) * 100, 1)

    return {
        'yield_per_hectare': round(pred, 2),
        'total_yield': round(total, 2),
        'model_used': best,
        'confidence': confidence,
        'accuracy': meta['results'][best]['Accuracy']
    }

if __name__ == '__main__':
    from utils.dataset_generator import generate_crop_dataset
    df = generate_crop_dataset()
    train_models(df)
