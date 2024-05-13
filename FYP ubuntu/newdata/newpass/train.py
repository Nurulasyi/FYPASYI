# train.py

from sklearn.ensemble import IsolationForest
import joblib
import pandas as pd

# Load data from CSV
data = pd.read_csv('data.csv')['strength'].values.reshape(-1, 1)

# Train Isolation Forest model
model = IsolationForest(contamination=0.1)
model.fit(data)

# Save trained model
joblib.dump(model, 'model_IF.pkl')
