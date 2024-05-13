# anomaly_detection/views.py

#from django.shortcuts import render
#from .models import PasswordData
#from sklearn.ensemble import IsolationForest

#def detect_anomalies(request):
    # Ambil data dari database
 #   data = PasswordData.objects.all().values_list('strength', flat=True)
 #   data = list(data)

    # Training Isolation Forest model
  #  model = IsolationForest(contamination=0.1)
  #  model.fit([[x] for x in data])

    # Prediksi anomali
   # predictions = model.predict([[x] for x in data])

    # Tampilkan password yang dianggap anomali
  #  anomalies = [password for password, prediction in zip(data, predictions) if prediction == -1]

   # return render(request, 'anomaly_detection.html', {'anomalies': anomalies})#

# anomaly_detection/views.py

#from django.shortcuts import render
#from .models import PasswordData
#from sklearn.ensemble import IsolationForest
#import numpy as np  # import numpy library

#def detect_anomalies(request):
    # Ambil data dari database
#    data = PasswordData.objects.all().values_list('strength', flat=True)
#    data = list(data)

    # Ubah array menjadi 2D
#    data = np.array(data).reshape(-1, 1)

    # Training Isolation Forest model
#    model = IsolationForest(contamination=0.1)
#    model.fit(data)

    # Prediksi anomali
#    predictions = model.predict(data)

    # Tampilkan password yang dianggap anomali
#    anomalies = [password for password, prediction in zip(data, predictions) if prediction == -1]

#    return render(request, 'anomaly_detection.html', {'anomalies': anomalies})


#def detect_anomalies(request):
    # Ambil data dari database
#    data = PasswordData.objects.all().values_list('strength', flat=True)
#    data = list(data)

#    if len(data) == 0:
        # Tidak ada data yang tersedia
 #       anomalies = []
  #  else:
        # Training Isolation Forest model
   #     model = IsolationForest(contamination=0.1)
    #    model.fit([[x] for x in data])

        # Prediksi anomali
     #   predictions = model.predict([[x] for x in data])

        # Tampilkan password yang dianggap anomali
      #  anomalies = [password for password, prediction in zip(data, predictions) if prediction == -1]

 #   return render(request, 'anomaly_detection.html', {'anomalies': anomalies})
from django.shortcuts import render
from sklearn.ensemble import IsolationForest
import joblib

def detect_anomalies(request):
    if request.method == 'POST':
        password = request.POST.get('password')

        # Load trained model
        model = joblib.load('model_IF.pkl')

        # Predict anomaly
        prediction = model.predict([[password]])

        # Determine anomaly status
        anomaly_status = "anomali" if prediction == -1 else "normal"

        return render(request, 'pass/detection_result.html', {'password': password, 'anomaly_status': anomaly_status})

    return render(request, 'pass/anomaly_detection.html')
