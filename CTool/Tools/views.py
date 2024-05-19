from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import AssetForm
from .models import Asset
import joblib
import pandas as pd

# Load the model when the server starts
model = joblib.load('model.pkl')

# Mapping of numeric identifiers to tool names
tool_names = {
    0: 'Nikto',
    1: 'Burp Suite'
    # Add more mappings as needed
}

def home(request):
    return render(request, 'Tools/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'Tools/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('add_asset')
    else:
        form = AuthenticationForm()
    return render(request, 'Tools/login.html', {'form': form})

@login_required
def add_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.user = request.user
            asset.save()
            return redirect('result')
    else:
        form = AssetForm()
    return render(request, 'Tools/add_asset.html', {'form': form})

@login_required
def result(request):
    assets = Asset.objects.filter(user=request.user)
    if assets.exists():
        data = [[asset.goal, asset.typeS, asset.toolsC, asset.platform] for asset in assets]
        df = pd.DataFrame(data, columns=['goal', 'typeS', 'toolsC', 'platform'])
        predictions = model.predict(df)
        results = [(tool_names.get(pred, 'Unknown Tool'), 'Nmap') for pred in predictions]
    else:
        results = []
    return render(request, 'Tools/result.html', {'results': results})
