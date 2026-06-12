from datetime import datetime
import json
import os
import sqlite3

from pymongo import MongoClient

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('DB_NAME', 'crop_yield_db')
SQLITE_PATH = os.environ.get('SQLITE_PATH', os.path.join('data', 'crop_yield.db'))


def _now():
    return datetime.utcnow()


def _parse_dt(value):
    if isinstance(value, datetime) or value is None:
        return value
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None


def get_db():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1200)
        client.server_info()
        return client[DB_NAME]
    except Exception:
        return None


def _sqlite_conn():
    os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    _init_sqlite(conn)
    return conn


def _init_sqlite(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            education_level TEXT DEFAULT 'literate',
            language TEXT DEFAULT 'en',
            phone TEXT,
            location TEXT,
            active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            input_json TEXT NOT NULL,
            result_json TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            message TEXT NOT NULL,
            username TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS crop_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_json TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            data_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chatbot_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            question TEXT,
            answer TEXT,
            language TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()


def _row_to_user(row):
    if not row:
        return None
    data = dict(row)
    data['active'] = bool(data.get('active'))
    data['created_at'] = _parse_dt(data.get('created_at'))
    return data


def _mongo_or_sqlite_collection(collection_name):
    db = get_db()
    return getattr(db, collection_name) if db is not None else None


def create_user(username, email, password_hash, role='user', education_level='literate',
                language='en', phone='', location=''):
    db = get_db()
    payload = {
        'username': username,
        'email': email,
        'password': password_hash,
        'role': role,
        'education_level': education_level,
        'language': language,
        'phone': phone,
        'location': location,
        'created_at': _now(),
        'active': True,
    }
    if db is not None:
        if db.users.find_one({'username': username}):
            return False
        db.users.insert_one(payload)
        return True

    with _sqlite_conn() as conn:
        if conn.execute('SELECT username FROM users WHERE username=?', (username,)).fetchone():
            return False
        conn.execute("""
            INSERT INTO users
            (username, email, password, role, education_level, language, phone, location, active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username, email, password_hash, role, education_level, language,
            phone, location, 1, payload['created_at'].isoformat()
        ))
        conn.commit()
    return True


def get_user(username):
    db = get_db()
    if db is not None:
        return db.users.find_one({'username': username})
    with _sqlite_conn() as conn:
        return _row_to_user(conn.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone())


def get_all_users():
    db = get_db()
    if db is not None:
        return list(db.users.find({}, {'password': 0}))
    with _sqlite_conn() as conn:
        rows = conn.execute("""
            SELECT username, email, role, education_level, language, phone, location, active, created_at
            FROM users ORDER BY created_at DESC
        """).fetchall()
        return [_row_to_user(row) for row in rows]


def update_user_preferences(username, **preferences):
    allowed = {'language', 'education_level', 'phone', 'location'}
    preferences = {k: v for k, v in preferences.items() if k in allowed}
    if not preferences:
        return
    db = get_db()
    if db is not None:
        db.users.update_one({'username': username}, {'$set': preferences})
        return
    with _sqlite_conn() as conn:
        assignments = ', '.join([f'{key}=?' for key in preferences])
        conn.execute(
            f'UPDATE users SET {assignments} WHERE username=?',
            tuple(preferences.values()) + (username,)
        )
        conn.commit()


def save_prediction(username, input_data, result):
    db = get_db()
    payload = {
        'username': username,
        'input': input_data,
        'result': result,
        'timestamp': _now(),
    }
    if db is not None:
        db.predictions.insert_one(payload)
        return
    with _sqlite_conn() as conn:
        conn.execute(
            'INSERT INTO predictions (username, input_json, result_json, timestamp) VALUES (?, ?, ?, ?)',
            (username, json.dumps(input_data), json.dumps(result), payload['timestamp'].isoformat())
        )
        conn.commit()


def get_predictions(username=None, limit=50):
    db = get_db()
    if db is not None:
        q = {'username': username} if username else {}
        return list(db.predictions.find(q, {'_id': 0}).sort('timestamp', -1).limit(limit))
    with _sqlite_conn() as conn:
        if username:
            rows = conn.execute(
                'SELECT * FROM predictions WHERE username=? ORDER BY timestamp DESC LIMIT ?',
                (username, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                'SELECT * FROM predictions ORDER BY timestamp DESC LIMIT ?',
                (limit,)
            ).fetchall()
        return [{
            'username': row['username'],
            'input': json.loads(row['input_json']),
            'result': json.loads(row['result_json']),
            'timestamp': _parse_dt(row['timestamp']),
        } for row in rows]


def get_prediction_stats():
    predictions = get_predictions(limit=10000)
    by_crop = {}
    for pred in predictions:
        crop = pred.get('input', {}).get('Crop')
        yield_value = pred.get('result', {}).get('yield_per_hectare')
        if not crop or yield_value is None:
            continue
        by_crop.setdefault(crop, {'_id': crop, 'count': 0, 'total_yield': 0.0})
        by_crop[crop]['count'] += 1
        by_crop[crop]['total_yield'] += float(yield_value)
    crop_stats = []
    for item in by_crop.values():
        item['avg_yield'] = item['total_yield'] / item['count']
        item.pop('total_yield', None)
        crop_stats.append(item)
    return {'total': len(predictions), 'by_crop': crop_stats}


def store_dataset_sample(records):
    db = get_db()
    if db is not None:
        db.crop_data.drop()
        if records:
            db.crop_data.insert_many(records)
        return
    with _sqlite_conn() as conn:
        conn.execute('DELETE FROM crop_data')
        conn.executemany(
            'INSERT INTO crop_data (data_json) VALUES (?)',
            [(json.dumps(record),) for record in records]
        )
        conn.commit()


def get_crop_data(limit=100):
    db = get_db()
    if db is not None:
        return list(db.crop_data.find({}, {'_id': 0}).limit(limit))
    with _sqlite_conn() as conn:
        rows = conn.execute('SELECT data_json FROM crop_data LIMIT ?', (limit,)).fetchall()
        return [json.loads(row['data_json']) for row in rows]


def save_report(username, report_data):
    db = get_db()
    payload = {'username': username, 'data': report_data, 'created_at': _now()}
    if db is not None:
        db.reports.insert_one(payload)
        return
    with _sqlite_conn() as conn:
        conn.execute(
            'INSERT INTO reports (username, data_json, created_at) VALUES (?, ?, ?)',
            (username, json.dumps(report_data), payload['created_at'].isoformat())
        )
        conn.commit()


def get_reports(username=None):
    db = get_db()
    if db is not None:
        q = {'username': username} if username else {}
        return list(db.reports.find(q, {'_id': 0}).sort('created_at', -1).limit(20))
    with _sqlite_conn() as conn:
        if username:
            rows = conn.execute(
                'SELECT * FROM reports WHERE username=? ORDER BY created_at DESC LIMIT 20',
                (username,)
            ).fetchall()
        else:
            rows = conn.execute('SELECT * FROM reports ORDER BY created_at DESC LIMIT 20').fetchall()
        return [{
            'username': row['username'],
            'data': json.loads(row['data_json']),
            'created_at': _parse_dt(row['created_at']),
        } for row in rows]


def log_event(event_type, message, username=None):
    db = get_db()
    payload = {
        'type': event_type,
        'message': message,
        'username': username,
        'timestamp': _now(),
    }
    if db is not None:
        db.logs.insert_one(payload)
        return
    with _sqlite_conn() as conn:
        conn.execute(
            'INSERT INTO logs (type, message, username, timestamp) VALUES (?, ?, ?, ?)',
            (event_type, message, username, payload['timestamp'].isoformat())
        )
        conn.commit()


def get_logs(limit=100):
    db = get_db()
    if db is not None:
        return list(db.logs.find({}, {'_id': 0}).sort('timestamp', -1).limit(limit))
    with _sqlite_conn() as conn:
        rows = conn.execute('SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?', (limit,)).fetchall()
        return [{
            'type': row['type'],
            'message': row['message'],
            'username': row['username'],
            'timestamp': _parse_dt(row['timestamp']),
        } for row in rows]


def save_chat_log(username, question, answer, language='en'):
    db = get_db()
    payload = {
        'username': username,
        'question': question,
        'answer': answer,
        'language': language,
        'timestamp': _now(),
    }
    if db is not None:
        db.chatbot_logs.insert_one(payload)
        return
    with _sqlite_conn() as conn:
        conn.execute(
            'INSERT INTO chatbot_logs (username, question, answer, language, timestamp) VALUES (?, ?, ?, ?, ?)',
            (username, question, answer, language, payload['timestamp'].isoformat())
        )
        conn.commit()


def get_chat_logs(username, limit=20):
    db = get_db()
    if db is not None:
        return list(db.chatbot_logs.find({'username': username}, {'_id': 0}).sort('timestamp', -1).limit(limit))
    with _sqlite_conn() as conn:
        rows = conn.execute(
            'SELECT * FROM chatbot_logs WHERE username=? ORDER BY timestamp DESC LIMIT ?',
            (username, limit)
        ).fetchall()
        return [{
            'username': row['username'],
            'question': row['question'],
            'answer': row['answer'],
            'language': row['language'],
            'timestamp': _parse_dt(row['timestamp']),
        } for row in rows]
