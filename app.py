from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Config
from config import Config, config

# Utilities
from utils.dataset_generator import generate_crop_dataset
from models.ml_pipeline import train_models, predict_yield, recommend_best_crops
from utils.db_utils import (create_user, get_user, get_all_users, save_prediction,
                             get_predictions, get_prediction_stats, store_dataset_sample,
                             get_crop_data, save_report, get_reports, log_event, get_logs, get_db,
                             update_user_preferences, save_chat_log, get_chat_logs)
from utils.visualizations import (plot_yield_distribution, plot_rainfall_yield,
                                   plot_correlation_heatmap, plot_model_comparison,
                                   plot_crop_season_yield, plot_feature_importance, eda_summary)
from utils.weather_handler import (get_weather_data, get_weather_forecast, 
                                    get_location_from_ip, get_location_from_name,
                                    validate_coordinates, interpret_weather_code,
                                    get_suitable_crops_for_weather)
from utils.recommendations import recommendation_engine
from utils.language_handler import (get_translation, get_supported_languages,
                                     get_language_name, get_all_translations)
from utils.api_integrations import cerebras_client, farmer_analyzer


def make_json_safe(value):
    if isinstance(value, dict):
        return {key: make_json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [make_json_safe(item) for item in value]
    if hasattr(value, 'item') and not isinstance(value, (str, bytes)):
        try:
            return value.item()
        except Exception:
            pass
    if hasattr(value, 'isoformat') and not isinstance(value, str):
        try:
            return value.isoformat()
        except Exception:
            pass
    return value

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cropyield_secret_2024')
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_UPLOAD_SIZE

@app.template_filter('enumerate')
def jinja_enumerate(iterable):
    return list(enumerate(iterable))

CROP_LIST = ['Rice','Wheat','Maize','Cotton','Sugarcane','Soybean','Groundnut','Barley','Jowar','Bajra']
SOIL_LIST = ['Clay','Sandy','Loamy','Silty','Chalky','Peaty']
SEASON_LIST = ['Kharif','Rabi','Zaid','Summer','Winter']
WEATHER_LIST = ['Sunny','Rainy','Cloudy','Humid','Dry']
STATE_LIST = ['Punjab','Haryana','UP','MP','Maharashtra','Karnataka','AP','Gujarat','Rajasthan','Bihar']

MODEL_FILES = ['models/best_model.pkl', 'models/scaler.pkl', 'models/encoders.pkl', 'models/model_meta.json']


def normalize_education_level(value):
    value = (value or 'literate').strip().lower()
    if value in {'studied', 'study', 'educated', 'literate', 'read'}:
        return 'literate'
    if value in {'illiterate', 'simple', 'picture', 'visual', 'voice'}:
        return 'illiterate'
    return 'literate'


def build_interface_context(username):
    user = get_user(username) if username else None
    education_level = normalize_education_level((user or {}).get('education_level') or session.get('education_level'))
    language = (user or {}).get('language') or session.get('language') or 'en'
    profile_config = farmer_analyzer.get_profile_based_interface(education_level)
    return {
        'education_level': education_level,
        'education_label': 'Illiterate / Picture mode' if education_level == 'illiterate' else 'Studied / Science mode',
        'language': language,
        'profile_config': profile_config,
    }

def ensure_model_ready():
    """Create a Kaggle-style training CSV and model artifacts for first run."""
    if all(os.path.exists(path) for path in MODEL_FILES):
        return
    df = generate_crop_dataset(2500)
    store_dataset_sample(df.head(200).to_dict(orient='records'))
    train_models(df)
    log_event('TRAIN', 'Auto-trained starter model from Kaggle-style crop yield dataset')

# ─── Auth Decorators ──────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated

# ─── Routes ───────────────────────────────────────────────
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        preferred_level = normalize_education_level(request.form.get('education_level'))
        preferred_language = request.form.get('language', 'en')
        user = get_user(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['role'] = user.get('role','user')
            session['education_level'] = normalize_education_level(user.get('education_level') or preferred_level)
            session['language'] = user.get('language', preferred_language)
            log_event('LOGIN', f'{username} logged in', username)
            return redirect(url_for('dashboard'))
        # Demo fallback
        if username == 'admin' and password == 'admin123':
            session['username'] = 'admin'
            session['role'] = 'admin'
            session['education_level'] = 'literate'
            session['language'] = 'en'
            return redirect(url_for('dashboard'))
        if username == 'farmer' and password == 'farmer123':
            session['username'] = 'farmer'
            session['role'] = 'user'
            session['education_level'] = 'illiterate'
            session['language'] = 'kn'
            return redirect(url_for('dashboard'))
        if username == 'farmer_educated' and password == 'farmer123':
            session['username'] = 'farmer_educated'
            session['role'] = 'user'
            session['education_level'] = 'literate'
            session['language'] = 'en'
            return redirect(url_for('dashboard'))
        if username == 'farmer_illiterate' and password == 'farmer123':
            session['username'] = 'farmer_illiterate'
            session['role'] = 'user'
            session['education_level'] = 'illiterate'
            session['language'] = 'kn'
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        education_level = normalize_education_level(request.form.get('education_level'))
        language = request.form.get('language', 'en')
        phone = request.form.get('phone', '')
        location = request.form.get('location', '')
        hashed = generate_password_hash(password)
        ok = create_user(username, email, hashed, 'user', education_level, language, phone, location)
        if ok:
            flash('Registration successful! Please login.', 'success')
            log_event('REGISTER', f'New user: {username}')
            return redirect(url_for('login'))
        else:
            flash('Username already exists', 'danger')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    stats = get_prediction_stats()
    recent = get_predictions(limit=5)
    model_meta = {}
    try:
        with open('models/model_meta.json') as f:
            model_meta = json.load(f)
    except: pass
    interface_context = build_interface_context(session['username'])
    return render_template('dashboard.html', stats=stats, recent=recent,
                           model_meta=model_meta, username=session['username'],
                           role=session.get('role','user'),
                           education_level=interface_context['education_level'],
                           education_label=interface_context['education_label'],
                           profile_config=interface_context['profile_config'],
                           language=interface_context['language'])

@app.route('/predict', methods=['GET','POST'])
@login_required
def predict():
    result = None
    recommendations = None
    weather_payload = None
    best_crops = []
    suitable_crops = []
    form_data = {}
    if request.method == 'POST':
        area_acres = float(request.form.get('area_acres') or request.form.get('area') or 0)
        area_hectares = area_acres * 0.404686
        rainfall = request.form.get('rainfall') or 0
        temperature = request.form.get('temperature') or 0
        humidity = request.form.get('humidity') or 0
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        if latitude and longitude and request.form.get('use_weather') == 'on':
            weather_payload = get_weather_data(float(latitude), float(longitude))
            if weather_payload.get('status') == 'success':
                rainfall = weather_payload.get('rainfall', rainfall)
                temperature = weather_payload.get('temperature', temperature)
                humidity = weather_payload.get('humidity', humidity)

        form_data = {
            'Crop': request.form['crop'],
            'State': request.form['state'],
            'Season': request.form['season'],
            'Soil_Type': request.form['soil_type'],
            'Weather_Condition': request.form['weather'],
            'Area': area_hectares,
            'Area_Acres': area_acres,
            'Rainfall': rainfall,
            'Temperature': temperature,
            'Humidity': humidity,
            'Fertilizer_Usage': request.form['fertilizer'],
            'Pesticide_Usage': request.form['pesticide'],
            'Location_Name': request.form.get('location_name', ''),
            'Latitude': latitude,
            'Longitude': longitude
        }
        try:
            ensure_model_ready()
            result = predict_yield(form_data)
            best_crops = recommend_best_crops(form_data, CROP_LIST, top_n=5)
            if best_crops:
                form_data['Best_Crop'] = best_crops[0]['crop']
            recommendations = recommendation_engine.get_comprehensive_recommendation(
                form_data['Crop'],
                form_data['Soil_Type'],
                form_data['Season'],
                form_data['Weather_Condition'],
                float(form_data['Rainfall'] or 0),
                float(form_data['Temperature'] or 0)
            )
            result['recommendations'] = recommendations
            result['weather'] = weather_payload
            result['best_crops'] = best_crops
            if weather_payload and weather_payload.get('status') == 'success':
                suitable_crops = get_suitable_crops_for_weather(weather_payload)
                result['suitable_crops'] = suitable_crops
            safe_result = make_json_safe(result)
            safe_form_data = make_json_safe(form_data)
            save_prediction(session['username'], safe_form_data, safe_result)
            log_event('PREDICTION', f"Predicted yield for {form_data['Crop']}: {safe_result['yield_per_hectare']} kg/ha", session['username'])
            result = safe_result
        except Exception as e:
            flash(f'Prediction error: {str(e)}. Please train the model first.', 'danger')

    return render_template('predict.html', result=result, form_data=form_data,
                           recommendations=recommendations, weather_payload=weather_payload,
                           best_crops=best_crops, suitable_crops=suitable_crops,
                           crops=CROP_LIST, soils=SOIL_LIST, seasons=SEASON_LIST,
                           weathers=WEATHER_LIST, states=STATE_LIST,
                           username=session['username'], role=session.get('role','user'),
                           education_level=session.get('education_level', 'literate'),
                           language=session.get('language', 'en'),
                           chatbot_available=bool(Config.CEREBRAS_API_KEY))

@app.route('/train', methods=['GET','POST'])
@login_required
def train():
    status = None
    model_meta = {}
    if request.method == 'POST':
        try:
            df = generate_crop_dataset(int(request.form.get('n_samples', 2500)))
            # Store sample in MongoDB
            sample = df.head(200).to_dict(orient='records')
            store_dataset_sample(sample)
            meta = train_models(df)
            status = 'success'
            model_meta = meta
            log_event('TRAIN', f"Models trained by {session['username']}", session['username'])
            flash('Models trained successfully!', 'success')
        except Exception as e:
            status = 'error'
            flash(f'Training error: {str(e)}', 'danger')

    try:
        with open('models/model_meta.json') as f:
            model_meta = json.load(f)
    except: pass

    return render_template('train.html', status=status, model_meta=model_meta,
                           username=session['username'], role=session.get('role','user'))

@app.route('/eda')
@login_required
def eda():
    plots = {}
    summary = {}
    try:
        import pandas as pd
        df = pd.read_csv('data/crop_yield_dataset.csv')
        summary = eda_summary(df)
        plots['distribution'] = plot_yield_distribution(df)
        plots['rainfall_yield'] = plot_rainfall_yield(df)
        plots['correlation'] = plot_correlation_heatmap(df)
        plots['crop_season'] = plot_crop_season_yield(df)
        plots['feature_importance'] = plot_feature_importance(df)
    except Exception as e:
        flash(f'EDA error: {str(e)} — please train model first.', 'warning')

    model_meta = {}
    try:
        with open('models/model_meta.json') as f:
            model_meta = json.load(f)
        plots['model_comparison'] = plot_model_comparison(model_meta['results'])
    except: pass

    return render_template('eda.html', plots=plots, summary=summary, model_meta=model_meta,
                           username=session['username'], role=session.get('role','user'))

@app.route('/history')
@login_required
def history():
    if session.get('role') == 'admin':
        predictions = get_predictions(limit=100)
    else:
        predictions = get_predictions(session['username'])
    return render_template('history.html', predictions=predictions,
                           username=session['username'], role=session.get('role','user'))

@app.route('/admin')
@login_required
@admin_required
def admin():
    users = get_all_users()
    logs = get_logs(50)
    stats = get_prediction_stats()
    dataset = get_crop_data(20)
    model_meta = {}
    try:
        with open('models/model_meta.json') as f:
            model_meta = json.load(f)
    except Exception:
        pass
    return render_template('admin.html', users=users, logs=logs, stats=stats,
                           dataset=dataset, model_meta=model_meta,
                           username=session['username'], role='admin')

@app.route('/report')
@login_required
def report():
    preds = get_predictions(session['username'] if session.get('role') != 'admin' else None)
    return render_template('report.html', predictions=preds,
                           username=session['username'], role=session.get('role','user'))

# ─── API endpoints ────────────────────────────────────────
@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()
    try:
        ensure_model_ready()
        result = make_json_safe(predict_yield(data))
        return jsonify({'status': 'success', 'result': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/stats')
def api_stats():
    return jsonify(get_prediction_stats())

# ─── Weather & Location APIs ──────────────────────────────
@app.route('/api/weather', methods=['GET'])
def api_weather():
    """Get weather data for coordinates"""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lon', type=float)
    
    if lat is None or lng is None:
        return jsonify({'status': 'error', 'message': 'Latitude and longitude required'}), 400
    
    is_valid, lat, lng = validate_coordinates(lat, lng)
    if not is_valid:
        return jsonify({'status': 'error', 'message': 'Invalid coordinates'}), 400
    
    weather = get_weather_data(lat, lng)
    forecast = get_weather_forecast(lat, lng)
    suitable_crops = get_suitable_crops_for_weather(weather)
    
    return jsonify({
        'status': 'success',
        'weather': weather,
        'forecast': forecast,
        'suitable_crops': suitable_crops
    })

@app.route('/api/best-crops', methods=['POST'])
@login_required
def api_best_crops():
    """Rank best crops for a farmer's land and current conditions."""
    data = request.get_json() or {}
    try:
        ensure_model_ready()
        area_acres = float(data.get('area_acres') or data.get('Area_Acres') or 1)
        latitude = data.get('latitude') or data.get('Latitude')
        longitude = data.get('longitude') or data.get('Longitude')
        weather_payload = None
        if latitude and longitude and data.get('use_weather', True):
            weather_payload = get_weather_data(float(latitude), float(longitude))
            if weather_payload.get('status') == 'success':
                data['Rainfall'] = weather_payload.get('rainfall', data.get('Rainfall', 0))
                data['Temperature'] = weather_payload.get('temperature', data.get('Temperature', 28))
                data['Humidity'] = weather_payload.get('humidity', data.get('Humidity', 65))
        payload = {
            'Crop': data.get('Crop', 'Rice'),
            'State': data.get('State', data.get('state', 'Karnataka')),
            'Season': data.get('Season', data.get('season', 'Kharif')),
            'Soil_Type': data.get('Soil_Type', data.get('soil_type', 'Loamy')),
            'Weather_Condition': data.get('Weather_Condition', data.get('weather', 'Sunny')),
            'Area': area_acres * 0.404686,
            'Rainfall': data.get('Rainfall', data.get('rainfall', 800)),
            'Temperature': data.get('Temperature', data.get('temperature', 28)),
            'Humidity': data.get('Humidity', data.get('humidity', 65)),
            'Fertilizer_Usage': data.get('Fertilizer_Usage', data.get('fertilizer', 180)),
            'Pesticide_Usage': data.get('Pesticide_Usage', data.get('pesticide', 1.5)),
        }
        ranked = recommend_best_crops(payload, CROP_LIST, top_n=5)
        return jsonify({'status': 'success', 'best_crops': ranked, 'weather': weather_payload})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/weather/forecast', methods=['GET'])
def api_weather_forecast():
    """Get weather forecast for location"""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lon', type=float)
    days = request.args.get('days', 7, type=int)
    
    if lat is None or lng is None:
        return jsonify({'status': 'error', 'message': 'Coordinates required'}), 400
    
    forecast = get_weather_forecast(lat, lng, days)
    return jsonify(forecast)

@app.route('/api/location/ip', methods=['GET'])
def api_location_ip():
    """Get user's approximate location from IP"""
    location = get_location_from_ip()
    return jsonify(location)

@app.route('/api/location/search', methods=['POST'])
def api_location_search():
    """Search location by city name"""
    data = request.get_json()
    city = data.get('city')
    state = data.get('state')
    
    if not city:
        return jsonify({'status': 'error', 'message': 'City name required'}), 400
    
    location = get_location_from_name(city, state)
    return jsonify(location)

# ─── Recommendations APIs ─────────────────────────────────
@app.route('/api/recommendations', methods=['POST'])
@login_required
def api_recommendations():
    """Get comprehensive crop recommendations"""
    data = request.get_json()
    
    crop = data.get('crop')
    soil_type = data.get('soil_type', 'Loamy')
    season = data.get('season', 'Kharif')
    weather = data.get('weather', 'Sunny')
    rainfall = data.get('rainfall', 100)
    temperature = data.get('temperature', 25)
    
    if not crop:
        return jsonify({'status': 'error', 'message': 'Crop required'}), 400
    
    recommendations = recommendation_engine.get_comprehensive_recommendation(
        crop, soil_type, season, weather, rainfall, temperature
    )
    
    # Save to database
    db = get_db()
    if db is not None:
        db.recommendations.insert_one({
            'username': session.get('username'),
            'crop': crop,
            'recommendations': recommendations,
            'timestamp': datetime.utcnow()
        })
    
    return jsonify({
        'status': 'success',
        'recommendations': recommendations
    })

@app.route('/api/npk-ratio/<crop>', methods=['GET'])
def api_npk_ratio(crop):
    """Get NPK ratio for crop"""
    npk = recommendation_engine.get_npk_recommendation(crop)
    return jsonify({
        'status': 'success',
        'crop': crop,
        'npk': npk
    })

@app.route('/api/fertilizer-recommendation', methods=['POST'])
def api_fertilizer():
    """Get fertilizer recommendations"""
    data = request.get_json()
    crop = data.get('crop')
    soil_type = data.get('soil_type', 'Loamy')
    weather = data.get('weather', 'Sunny')
    
    if not crop:
        return jsonify({'status': 'error', 'message': 'Crop required'}), 400
    
    recommendations = recommendation_engine.get_fertilizer_recommendation(
        crop, soil_type, weather
    )
    return jsonify({
        'status': 'success',
        'recommendations': recommendations
    })

@app.route('/api/pesticide-recommendation', methods=['POST'])
def api_pesticide():
    """Get pesticide recommendations"""
    data = request.get_json()
    crop = data.get('crop')
    season = data.get('season', 'Kharif')
    weather = data.get('weather', 'Sunny')
    
    if not crop:
        return jsonify({'status': 'error', 'message': 'Crop required'}), 400
    
    recommendations = recommendation_engine.get_pesticide_recommendation(
        crop, season, weather
    )
    return jsonify({
        'status': 'success',
        'recommendations': recommendations
    })

@app.route('/api/irrigation-schedule', methods=['POST'])
def api_irrigation():
    """Get irrigation schedule recommendations"""
    data = request.get_json()
    crop = data.get('crop')
    season = data.get('season', 'Kharif')
    rainfall = data.get('rainfall', 100)
    temperature = data.get('temperature', 25)
    
    if not crop:
        return jsonify({'status': 'error', 'message': 'Crop required'}), 400
    
    schedule = recommendation_engine.get_irrigation_schedule(
        crop, season, rainfall, temperature
    )
    return jsonify({
        'status': 'success',
        'schedule': schedule
    })

# ─── Chatbot APIs ─────────────────────────────────────────
@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """Chat with agricultural chatbot"""
    data = request.get_json()
    question = data.get('question')
    language = data.get('language', 'en')
    education_level = session.get('education_level', 'literate')
    
    if not question:
        return jsonify({'status': 'error', 'message': 'Question required'}), 400
    
    response = cerebras_client.ask_agricultural_question(question, language, education_level)
    
    save_chat_log(session.get('username'), question, response.get('answer'), language)

    return jsonify(response)

@app.route('/api/chat/history', methods=['GET'])
@login_required
def api_chat_history():
    """Get chatbot conversation history"""
    limit = request.args.get('limit', 20, type=int)
    
    logs = get_chat_logs(session.get('username'), limit)
    
    return jsonify({
        'status': 'success',
        'history': logs
    })

@app.route('/api/crop-info/<crop>', methods=['GET'])
def api_crop_info(crop):
    """Get detailed crop information from chatbot"""
    language = request.args.get('language', 'en')
    
    response = cerebras_client.get_crop_information(crop, language)
    return jsonify(response)

# ─── Admin APIs ────────────────────────────────────────────
@app.route('/api/admin/users', methods=['GET'])
@login_required
@admin_required
def api_admin_users():
    """Get all users"""
    users = get_all_users()
    return jsonify({
        'status': 'success',
        'users': users,
        'total': len(users)
    })

@app.route('/api/admin/logs', methods=['GET'])
@login_required
@admin_required
def api_admin_logs():
    """Get system logs"""
    limit = request.args.get('limit', 50, type=int)
    event_type = request.args.get('type')
    
    logs = get_logs(limit)
    if event_type:
        logs = [log for log in logs if log.get('type') == event_type]
    
    return jsonify({
        'status': 'success',
        'logs': logs,
        'total': len(logs)
    })

@app.route('/api/admin/model-accuracy', methods=['GET'])
@login_required
@admin_required
def api_model_accuracy():
    """Get model accuracy statistics"""
    try:
        with open('models/model_meta.json') as f:
            meta = json.load(f)
        return jsonify({
            'status': 'success',
            'model_accuracy': meta.get('results', {})
        })
    except:
        return jsonify({
            'status': 'error',
            'message': 'Model metadata not found'
        }), 404

@app.route('/api/admin/predictions-stats', methods=['GET'])
@login_required
@admin_required
def api_predictions_stats():
    """Get prediction statistics"""
    stats = get_prediction_stats()
    return jsonify({
        'status': 'success',
        'stats': stats
    })

# ─── Translation API ──────────────────────────────────────
@app.route('/api/translations/<language_code>', methods=['GET'])
def api_translations(language_code):
    """Get all translations for a language"""
    translations = get_all_translations(language_code)
    return jsonify({
        'status': 'success',
        'language': get_language_name(language_code),
        'translations': translations
    })

@app.route('/api/languages', methods=['GET'])
def api_languages():
    """Get supported languages"""
    languages = get_supported_languages()
    return jsonify({
        'status': 'success',
        'languages': languages
    })

# ─── User Profile APIs ────────────────────────────────────
@app.route('/api/user/profile', methods=['GET'])
@login_required
def api_user_profile():
    """Get user profile"""
    user = get_user(session.get('username'))
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    profile_config = farmer_analyzer.get_profile_based_interface(
        user.get('education_level', 'literate')
    )
    
    return jsonify({
        'status': 'success',
        'username': user.get('username'),
        'email': user.get('email'),
        'role': user.get('role'),
        'education_level': user.get('education_level'),
        'profile_config': profile_config
    })

@app.route('/api/user/preferences', methods=['POST'])
@login_required
def api_user_preferences():
    """Update user preferences"""
    data = request.get_json()
    
    update_user_preferences(
        session.get('username'),
        language=data.get('language', 'en'),
        education_level=normalize_education_level(data.get('education_level', 'literate')),
        phone=data.get('phone', ''),
        location=data.get('location', '')
    )
    session['language'] = data.get('language', 'en')
    session['education_level'] = normalize_education_level(data.get('education_level', 'literate'))
    
    return jsonify({
        'status': 'success',
        'message': 'Preferences updated'
    })

# ─── Analytics API ────────────────────────────────────────
@app.route('/api/analytics', methods=['POST'])
def api_analytics():
    """Log user analytics"""
    data = request.get_json()
    
    db = get_db()
    if db is not None:
        db.analytics.insert_one({
            'username': session.get('username'),
            'event': data.get('event'),
            'data': data.get('data'),
            'timestamp': datetime.utcnow()
        })
    
    return jsonify({'status': 'success'})

# ─── Init ─────────────────────────────────────────────────
def init_app():
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('static/images/crops', exist_ok=True)
    try:
        create_user('admin', 'admin@cropai.com', generate_password_hash('admin123'), 'admin', 'literate', 'en')
        create_user('farmer', 'farmer@cropai.com', generate_password_hash('farmer123'), 'user', 'illiterate', 'kn')
        create_user('farmer_educated', 'farmer1@cropai.com', generate_password_hash('farmer123'), 'user', 'literate', 'en')
        create_user('farmer_illiterate', 'farmer2@cropai.com', generate_password_hash('farmer123'), 'user', 'illiterate', 'hi')
    except: pass
    try:
        ensure_model_ready()
    except Exception as exc:
        print(f"Starter model training skipped: {exc}")
    print("=" * 50)
    print("CropYield AI System started")
    print("Demo users: admin/admin123, farmer/farmer123, farmer_educated/farmer123, farmer_illiterate/farmer123")
    print("Weather: Open-Meteo | Location: OpenStreetMap | Chatbot: Cerebras")
    print("=" * 50)

if __name__ == '__main__':
    init_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
