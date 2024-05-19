import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import joblib

# Load the dataset
data = pd.read_csv('pentest.csv')

# Assume the dataset has the same structure as the user input
X = data[['goal', 'typeS', 'toolsC', 'platform']]
y = data['suggest']  # The target column

# Train the GBM model
model = GradientBoostingClassifier()
model.fit(X, y)

# Save the model
joblib.dump(model, 'model.pkl')
