import numpy as np
from flask import Blueprint, render_template, request, redirect, url_for
import joblib
from pathlib import Path
from .visualizer import generate_bar_chart, generate_radar_chart, generate_gauge_chart

main = Blueprint('main', __name__)

# Go up one level from `app/` to root project directory
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / 'models'  # Assuming model is in root/models/

model = joblib.load(MODEL_DIR / 'ensemble_model.pkl')
scaler = joblib.load(MODEL_DIR / 'scaler.pkl')

# Mapping form keys to dataset keys
column_map = {
    'Age': 'Age_of_the_patient',
    'Gender': 'Gender_of_the_patient',
    'Total Bilirubin': 'Total_Bilirubin',
    'Direct Bilirubin': 'Direct_Bilirubin',
    'Alkaline Phosphatase': 'Alkphos_Alkaline_Phosphotase',
    'Alamine Aminotransferase': 'Sgpt_Alamine_Aminotransferase',
    'Aspartate Aminotransferase': 'Sgot_Aspartate_Aminotransferase',
    'Total Protiens': 'Total_Protiens',
    'Albumin': 'ALB_Albumin',
    'Albumin and Globulin Ratio': 'A/G_Ratio_Albumin_and_Globulin_Ratio'
}

# Feature names (as in your dataset and form)
FEATURES = list(column_map.keys())

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Retrieve and convert form values
            input_values = []
            for feat in FEATURES:
                val = request.form.get(feat)
                if val is None or val == "":
                    return f"Missing input for {feat}", 400
                input_values.append(float(val))

        except ValueError as e:
            return f"Invalid input: {e}", 400

        X_input = np.array(input_values).reshape(1, -1)
        X_scaled = scaler.transform(X_input)
        proba = model.predict_proba(X_scaled)[0][1]  # probability for liver disease

        # Determine risk level
        if proba < 0.3:
            risk = "✅ Low Risk"
        elif proba < 0.7:
            risk = "⚠️ Moderate Risk"
        else:
            risk = "❗ High Risk"

        # Prepare dictionary for visualization functions (with cleaned column names)
        input_dict = {column_map[feat]: input_values[i] for i, feat in enumerate(FEATURES)}
        
        bar_chart = generate_bar_chart(input_dict)
        radar_chart = generate_radar_chart(input_dict)
        gauge_chart = generate_gauge_chart(proba * 100)

        return render_template(
            'result.html',
            risk_score=round(proba * 100, 2),
            risk_level=risk,
            bar_chart=bar_chart,
            radar_chart=radar_chart,
            gauge_chart=gauge_chart
        )
        
    return render_template('predict.html')
