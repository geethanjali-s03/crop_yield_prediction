# 🌾 CropYield AI — Intelligent Crop Yield Prediction System
### AI/ML Final Year Project | Python Flask + MongoDB + Scikit-learn + XGBoost

---

## 📋 Abstract
CropYield AI is an end-to-end intelligent agricultural platform that leverages machine learning to predict crop yield based on environmental and agricultural parameters. The system integrates multiple ML algorithms, MongoDB NoSQL database, and a professional web dashboard to deliver accurate yield forecasts to farmers and agricultural organizations.

---

## 🏗️ Project Architecture
```
CropYield AI
├── Frontend   : HTML5 + Bootstrap 5 + JavaScript
├── Backend    : Python Flask (REST API + Server-side rendering)
├── ML Engine  : Scikit-learn + XGBoost (5 algorithms)
├── Database   : MongoDB (NoSQL — 5 collections)
└── Storage    : Joblib model persistence
```

---

## 📁 Project Structure
```
crop_yield_system/
├── app.py                         # Main Flask application
├── requirements.txt               # Python dependencies
├── data/
│   └── crop_yield_dataset.csv    # Generated agricultural dataset
├── models/
│   ├── ml_pipeline.py            # ML training & prediction pipeline
│   ├── best_model.pkl            # Serialised best model (after training)
│   ├── scaler.pkl                # Feature scaler
│   ├── encoders.pkl              # Label encoders
│   └── model_meta.json           # Model results & metadata
├── utils/
│   ├── dataset_generator.py      # Synthetic dataset generator
│   ├── db_utils.py               # MongoDB CRUD operations
│   └── visualizations.py        # EDA & chart generation
└── templates/
    ├── base.html                 # Base layout with sidebar nav
    ├── index.html                # Landing page
    ├── login.html                # Authentication
    ├── register.html             # User registration
    ├── dashboard.html            # Main dashboard
    ├── predict.html              # Yield prediction form
    ├── train.html                # Model training UI
    ├── eda.html                  # EDA & visualizations
    ├── history.html              # Prediction history
    ├── report.html               # Report generation
    └── admin.html                # Admin panel
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure MongoDB (optional)
```bash
# Local MongoDB (default)
mongod --dbpath /data/db

# OR set environment variable for Atlas
export MONGO_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
```

### 3. Run the Application
```bash
cd crop_yield_system
python app.py
```
Visit: http://localhost:5000

### 4. Demo Credentials
| Role   | Username | Password   |
|--------|----------|------------|
| Admin  | admin    | admin123   |
| Farmer | farmer   | farmer123  |

### 5. First Steps
1. Login → Navigate to **Train Models**
2. Click **Start Training** (takes ~30 seconds)
3. Go to **Predict Yield** → Enter parameters → Get prediction
4. View **EDA** for visualizations
5. Check **Reports** for history

---

## 🤖 ML Algorithms Implemented

| Algorithm | Type | Best For |
|-----------|------|----------|
| Linear Regression | Baseline | Simple linear relationships |
| Decision Tree | Non-linear | Interpretable rules |
| Random Forest | Ensemble | Robust, handles noise |
| **XGBoost** | **Gradient Boosting** | **Best accuracy (97.77%)** |
| SVM (SVR) | Kernel-based | High-dimensional data |

### Model Evaluation Metrics
- **R² Score** — Coefficient of determination (1.0 = perfect)
- **RMSE** — Root Mean Squared Error
- **MAE** — Mean Absolute Error
- **Accuracy %** — Derived from R² × 100

---

## 🗄️ MongoDB Collections

| Collection | Purpose | Key Fields |
|------------|---------|-----------|
| `users` | User accounts | username, email, password, role |
| `crop_data` | Agricultural dataset | Crop, Area, Rainfall, Temperature, Yield |
| `predictions` | Prediction history | input, result, timestamp, username |
| `reports` | Generated reports | data, created_at, username |
| `logs` | System audit logs | type, message, username, timestamp |

> The app uses these names directly in MongoDB when `MONGO_URI` is configured. If MongoDB is unavailable, the same data is stored in the SQLite fallback tables with matching names.

---

## 📊 Dataset Features

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| Crop | Categorical | 10 types | Crop variety |
| State | Categorical | 10 states | Geographic region |
| Season | Categorical | 5 seasons | Kharif/Rabi/etc |
| Soil_Type | Categorical | 6 types | Clay/Sandy/Loamy/etc |
| Weather_Condition | Categorical | 5 types | Sunny/Rainy/etc |
| Area | Numeric | 0.5–50 ha | Cultivation area |
| Rainfall | Numeric | 200–2500 mm | Annual rainfall |
| Temperature | Numeric | 15–45 °C | Average temperature |
| Humidity | Numeric | 20–95 % | Relative humidity |
| Fertilizer_Usage | Numeric | 50–500 kg/ha | Fertilizer amount |
| Pesticide_Usage | Numeric | 0.1–5 kg/ha | Pesticide amount |
| **Yield_Per_Hectare** | **Target** | Variable | **kg per hectare** |

---

## 🔧 API Endpoints

```
GET  /                  Landing page
GET  /login             Login form
POST /login             Authenticate user
GET  /register          Registration form
POST /register          Create new user
GET  /dashboard         Main dashboard
GET  /predict           Prediction form
POST /predict           Submit prediction
GET  /train             Training configuration
POST /train             Start model training
GET  /eda               EDA & visualizations
GET  /history           Prediction history
GET  /report            Report generation
GET  /admin             Admin panel (admin only)
POST /api/predict       REST API — JSON prediction
GET  /api/stats         REST API — statistics
```

---

## 📈 System Modules

### 1. User Module
- Register / Login / Logout with session management
- Role-based access (admin vs farmer)
- Input agricultural parameters via interactive form
- View predictions with confidence scores

### 2. Admin Module
- View all registered users
- Monitor all predictions and analytics
- View MongoDB dataset sample
- System event audit logs

### 3. Prediction Module
- 11 input parameters with sliders and dropdowns
- Real-time prediction using best-selected ML model
- Displays yield/hectare, total yield, confidence %, algorithm used
- Automatically saved to MongoDB

### 4. EDA & Visualization Module
- Yield distribution histogram & boxplot
- Rainfall vs Yield scatter plot
- Feature correlation heatmap
- Crop × Season yield comparison
- Feature importance bar chart
- Model accuracy comparison chart

### 5. Report Module
- Full prediction history table
- Summary statistics (avg yield, confidence)
- CSV export functionality
- Print-ready report view

---

## 🎓 PBL Review Coverage

| Review Criteria | Implementation |
|----------------|---------------|
| Problem Definition | Crop yield uncertainty → ML prediction system |
| Dataset Preparation | Synthetic generation + cleaning + encoding + scaling |
| EDA & Visualization | 6 chart types with Matplotlib/Seaborn |
| ML Model Design | 5 algorithms with systematic comparison |
| NoSQL Integration | MongoDB with 5 collections, full CRUD |
| System Architecture | Flask MVC + modular utils |
| Frontend-Backend Integration | Jinja2 templates + REST API |
| Module Functionality | 5 distinct modules, all functional |
| Prediction Output | kg/ha + total yield + confidence + algorithm |
| Reports | Exportable CSV, printable history |

---

## 🏆 Results

**Best Model: XGBoost Regressor**
- R² Score: 0.9777
- Accuracy: 97.77%
- Trained on 2000 samples (80/20 split)
- Features: 11 agricultural & environmental parameters

---

## 🔮 Future Scope
1. Real-time weather API integration (OpenWeatherMap)
2. Satellite imagery analysis with CNN
3. Mobile app (Flutter/React Native)
4. Government crop advisory API integration
5. IoT sensor data ingestion pipeline
6. Multi-language support (Hindi, Kannada, etc.)
7. Price prediction + profitability analysis
8. Deep Learning (LSTM) for time-series yield forecasting

---

## 📚 Technologies Used
- **Python 3.10+** — Core language
- **Flask 3.0** — Web framework
- **MongoDB / PyMongo** — NoSQL database
- **Scikit-learn** — ML algorithms
- **XGBoost** — Gradient boosting
- **Pandas / NumPy** — Data processing
- **Matplotlib / Seaborn** — Visualizations
- **Bootstrap 5** — Frontend UI
- **Joblib** — Model serialization

---

*© 2024 CropYield AI — AI/ML Final Year Project*
