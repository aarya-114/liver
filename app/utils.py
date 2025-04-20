# app/utils.py
import plotly.graph_objs as go
import pandas as pd

def generate_gauge_chart(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Risk Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "red" if score > 70 else "orange" if score > 35 else "green"},
            'steps': [
                {'range': [0, 35], 'color': "lightgreen"},
                {'range': [35, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "tomato"}
            ]
        }
    ))
    return fig.to_html(full_html=False)

def generate_bar_chart(user_data):
    healthy_avg = pd.Series({
        'Total Bilirubin': 0.8,
        'Direct Bilirubin': 0.3,
        'Alkaline Phosphotase': 80,
        'Alamine Aminotransferase': 25,
        'Aspartate Aminotransferase': 25,
        'Albumin': 4.2
    })

    patient = user_data[healthy_avg.index]
    df = pd.DataFrame({'User': patient, 'Healthy Avg': healthy_avg})
    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(go.Bar(name=col, x=df.index, y=df[col]))
    fig.update_layout(barmode='group', title='Biomarker Comparison')
    return fig.to_html(full_html=False)

def generate_radar_chart(user_data):
    features = ['Total Bilirubin', 'Direct Bilirubin', 'Alkaline Phosphotase',
                'Alamine Aminotransferase', 'Aspartate Aminotransferase', 'Albumin']
    healthy_avg = pd.Series([0.8, 0.3, 80, 25, 25, 4.2], index=features)
    user_vals = user_data[features]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=healthy_avg, theta=features, fill='toself', name='Healthy Avg'))
    fig.add_trace(go.Scatterpolar(r=user_vals, theta=features, fill='toself', name='User'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True, title='Liver Profile Radar')
    return fig.to_html(full_html=False)
