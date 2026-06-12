"""
CropYield AI — One-click setup and launcher
Run: python setup_and_run.py
"""
import subprocess, sys, os

def run(cmd, desc):
    print(f"\n[...] {desc}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[WARN] {result.stderr[:200]}")
    else:
        print(f"[OK]  {desc}")

print("=" * 55)
print("  CropYield AI — Setup & Launch")
print("=" * 55)

# Install dependencies
run(f"{sys.executable} -m pip install flask pymongo scikit-learn xgboost pandas numpy matplotlib seaborn joblib werkzeug --quiet", "Installing Python packages")

# Generate dataset and train models
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("\n[...] Generating dataset (2000 samples)...")
from utils.dataset_generator import generate_crop_dataset
df = generate_crop_dataset(2000)
print(f"[OK]  Dataset: {df.shape[0]} rows × {df.shape[1]} cols")

print("[...] Training 5 ML models...")
from models.ml_pipeline import train_models
meta = train_models(df)
best = meta['best_model']
acc  = meta['results'][best]['Accuracy']
print(f"[OK]  Best model: {best} — {acc}% accuracy")

print("\n" + "=" * 55)
print("  Setup complete! Starting Flask server...")
print("  URL:  http://localhost:5000")
print("  Admin:  admin / admin123")
print("  Farmer: farmer / farmer123")
print("=" * 55 + "\n")

from app import app, init_app
init_app()
app.run(debug=False, host='0.0.0.0', port=5000)
