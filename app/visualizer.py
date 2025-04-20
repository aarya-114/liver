import plotly.graph_objs as go
import pandas as pd
from pathlib import Path

# Path to the dataset (used for population statistics)
BASE_DIR = Path(__file__).resolve().parent.parent  # go up to project root
DATA_PATH = BASE_DIR / 'data' / 'raw' / 'Liver Patient Dataset (LPD)_train.csv'

def load_population_stats():
    df = pd.read_csv(DATA_PATH, encoding='unicode_escape')
    
    # Strip and normalize column names
    df.columns = df.columns.str.strip().str.replace(' ', '_')

    # Map gender to binary
    df['Gender_of_the_patient'] = df['Gender_of_the_patient'].map({'Female': 0, 'Male': 1})
    df.dropna(inplace=True)
    
    healthy = df[df['Result'] == 0]
    diseased = df[df['Result'] == 1]

    # Use the cleaned column names
    features = [
        'Age_of_the_patient',
        'Total_Bilirubin',
        'Direct_Bilirubin',
        'Alkphos_Alkaline_Phosphotase',
        'Sgpt_Alamine_Aminotransferase',
        'Sgot_Aspartate_Aminotransferase',
        'Total_Protiens',
        'ALB_Albumin',
        'A/G_Ratio_Albumin_and_Globulin_Ratio',
        'Gender_of_the_patient'
    ]

    healthy_mean = healthy[features].mean()
    diseased_mean = diseased[features].mean()
    
    return healthy_mean, diseased_mean

def generate_bar_chart(user_input_dict):
    healthy_mean, diseased_mean = load_population_stats()

    features = [f for f in user_input_dict if f != 'Gender of the patient']
    user_vals = [user_input_dict[f] for f in features]
    healthy_vals = [healthy_mean[f] for f in features]
    diseased_vals = [diseased_mean[f] for f in features]

    trace_user = go.Bar(name='User', x=features, y=user_vals, marker_color='blue')
    trace_healthy = go.Bar(name='Healthy Avg', x=features, y=healthy_vals, marker_color='green')
    trace_diseased = go.Bar(name='Diseased Avg', x=features, y=diseased_vals, marker_color='red')

    fig = go.Figure(data=[trace_user, trace_healthy, trace_diseased])
    fig.update_layout(title='Biomarker Comparison', barmode='group')
    return fig.to_html(full_html=False)

def generate_radar_chart(user_input_dict):
    healthy_mean, diseased_mean = load_population_stats()

    features = [f for f in user_input_dict if f != 'Gender of the patient']
    user_vals = [user_input_dict[f] for f in features]
    healthy_vals = [healthy_mean[f] for f in features]
    diseased_vals = [diseased_mean[f] for f in features]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=user_vals, theta=features, fill='toself', name='User'))
    fig.add_trace(go.Scatterpolar(r=healthy_vals, theta=features, fill='toself', name='Healthy Avg'))
    fig.add_trace(go.Scatterpolar(r=diseased_vals, theta=features, fill='toself', name='Diseased Avg'))

    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), title='Profile Radar Chart', showlegend=True)
    return fig.to_html(full_html=False)

def generate_gauge_chart(risk_score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        delta={'reference': 50},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "orange"},
            'steps': [
                {'range': [0, 30], 'color': "green"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"},
            ],
        },
        title={'text': "Risk Score Gauge"}
    ))
    return fig.to_html(full_html=False)
