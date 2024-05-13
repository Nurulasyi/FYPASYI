# newpass/pass/views.py

from django.shortcuts import render
from sklearn.ensemble import IsolationForest
import joblib

def detect_anomalies(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        
        # Preprocess the input data (e.g., remove non-numeric characters)
        password = preprocess_password(password)

        # Load trained model
        model = joblib.load('model_IF.pkl')

        # Predict anomaly
        prediction = model.predict([[password]])

        # Determine anomaly status
        anomaly_status = "anomali" if prediction == -1 else "normal"

        return render(request, 'pass/detection_result.html', {'password': password, 'anomaly_status': anomaly_status})

    return render(request, 'pass/anomaly_detection.html')

#def preprocess_password(password):
    # Implement your preprocessing logic here
    # For example, you can remove non-numeric characters
   # return ''.join(filter(str.isdigit, password))
def preprocess_password(password):
    # Keep only numeric characters in the password
    numeric_password = ''.join(char for char in password if char.isdigit())
    return numeric_password

