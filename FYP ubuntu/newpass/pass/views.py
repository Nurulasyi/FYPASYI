# newpass/pass/views.py

from django.shortcuts import render
from sklearn.ensemble import IsolationForest
import joblib
import subprocess


def detect_anomalies(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        target = request.POST.get('target')
        
        # Preprocess the input data (e.g., remove non-numeric characters)
        password = preprocess_password(password)

        # Load trained model
        model = joblib.load('model_IF.pkl')

        # Predict anomaly
        prediction = model.predict([[password]])

        # Determine anomaly status
        anomaly_status = "anomali" if prediction == -1 else "normal"

                # Run Nmap scan if the password is considered normal
        if anomaly_status == "normal":
            # Replace 'target_ip_or_hostname' with the actual target IP or hostname
            #target = 'target_ip_or_hostname'
           # nmap_output = run_nmap_scan(target)
            nikto_output = run_nikto_scan(target)
            return render(request, 'pass/detection_result.html', {'password': password, 'anomaly_status': anomaly_status, 'nmap_output': nmap_output, 'nikto_output': nikto_output})

        return render(request, 'pass/detection_result.html', {'password': password, 'anomaly_status': anomaly_status})

    return render(request, 'pass/anomaly_detection.html')

def preprocess_password(password):
    # Keep only numeric characters in the password
    numeric_password = ''.join(char for char in password if char.isdigit())
    return numeric_password

#def run_nmap_scan(target):
 #   command = ['nmap', '-Pn', target]
   # result = subprocess.run(command, capture_output=True, text=True)
    #return result.stdout
        
  # newpass/pass/views.py

def run_nikto_scan(target):
    command = ['nikto', '-h', target]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout
      
        
        
        
      #  return render(request, 'pass/detection_result.html', {'password': password, 'anomaly_status': anomaly_status})

    #return render(request, 'pass/anomaly_detection.html')

#def preprocess_password(password):
    # Implement your preprocessing logic here
    # For example, you can remove non-numeric characters
   # return ''.join(filter(str.isdigit, password))
#def preprocess_password(password):
    # Keep only numeric characters in the password
    #numeric_password = ''.join(char for char in password if char.isdigit())
    #return numeric_password

#def run_nmap_scan(target):
    #command = ['nmap', '-Pn', target]
    #result = subprocess.run(command, capture_output=True, text=True)
    #return result.stdout

