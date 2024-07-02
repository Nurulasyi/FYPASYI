import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv('pentest.csv')

# Check dataset balance
print(df['suggest'].value_counts())

# Preprocess data
X = df[['goal', 'typeS', 'toolsC', 'platform']]
y = df['suggest']

# Label Encoding
label_encoder = LabelEncoder()
for col in X.columns:
    X[col] = label_encoder.fit_transform(X[col])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = GradientBoostingClassifier()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save model and label encoder
joblib.dump(model, 'GBM_model.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')
print("Model and label encoder saved.")
