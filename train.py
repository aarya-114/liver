import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import joblib

# Configure paths 
BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / 'data' / 'raw' / 'Liver Patient Dataset (LPD)_train.csv'
MODEL_DIR = BASE_DIR / 'models'
MODEL_DIR.mkdir(parents=True, exist_ok=True)

def train_and_save_model():
    # Load data
    df = pd.read_csv(DATA_PATH, encoding='unicode_escape')
    print(df.columns)
    
    # Preprocessing
    df['Gender of the patient'] = df['Gender of the patient'].map({'Female': 0, 'Male': 1})
    df = df.dropna()
    
    # Prepare features
    X = df.drop('Result', axis=1)
    y = df['Result']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Initialize and train ensemble model
    ensemble = VotingClassifier(
        estimators=[
            ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
            ('dt', DecisionTreeClassifier(max_depth=5, random_state=42)),
            ('lr', LogisticRegression(max_iter=1000)),
            ('svm', SVC(probability=True)),
            ('xgb', XGBClassifier(use_label_encoder=False, eval_metric='logloss')),
            ('lgbm', LGBMClassifier())
        ],
        voting='soft'
    )
    ensemble.fit(X_train_scaled, y_train)
    
    # Save artifacts
    joblib.dump(ensemble, MODEL_DIR / 'ensemble_model.pkl')
    joblib.dump(scaler, MODEL_DIR / 'scaler.pkl')
    print("Model trained and saved successfully!")

if __name__ == "__main__":
    train_and_save_model()

