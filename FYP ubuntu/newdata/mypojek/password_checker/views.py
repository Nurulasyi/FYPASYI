# password_checker/views.py
from django.shortcuts import render
from django.http import JsonResponse
from password_checker.models import PasswordData
from sklearn.ensemble import IsolationForest

def check_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        
        # Load data from database
        passwords = PasswordData.objects.values_list('password', flat=True)
        
        # Convert to pandas DataFrame
        data = pd.DataFrame({'password': passwords})
        
        # Train Isolation Forest
        clf = IsolationForest()
        clf.fit(data)
        
        # Predict if password is anomaly
        if clf.predict([[password]])[0] == -1:
            result = "Password is anomalous"
        else:
            result = "Password is not anomalous"
        
        return JsonResponse({'result': result})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def show_password_form(request):
    return render(request, 'check_password.html')
    
def home(request):
    return render(request, 'home.html')
