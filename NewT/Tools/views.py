from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import AssetForm, HydraForm, NmapForm, NcrackForm
from .models import Asset, UserSuggestion
import joblib
import pandas as pd
import subprocess
import re
import os

# Load the model when the server starts
model = joblib.load('model.pkl')

# Mapping of numeric identifiers to tool names
tool_names = {
    0: {'name': 'Hydra', 'url_name': 'Hydra'},
    1: {'name': 'Ncrack', 'url_name': 'Ncrack'},
}

# Mapping of numeric identifiers to human-readable names
goal_pentest_map = {1: 'Web Application', 2: 'Network', 3: 'Cloud'}
type_software_map = {1: 'Web-based', 2: 'Mobile', 3: 'Network'}
platform_map = {1: 'Windows', 2: 'Linux', 3: 'MacOS', 4: 'Cloud'}
type_password_attack_map = {1: 'Brute Force', 2: 'Dictionary', 3: 'Hybrid'}
hash_type_map = {0: 'MD5', 1: 'SHA-1', 2: 'SHA-256'}

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
            return redirect('user_results')
    else:
        form = AssetForm()
    return render(request, 'Tools/add_asset.html', {'form': form})
    
@login_required
def user_results(request):
    asset = Asset.objects.filter(user=request.user).order_by('-created_at').first()
    results = []
    if asset:
        data = [[asset.goal_pentest, asset.type_software, asset.platform, asset.type_password_attack, asset.hash_type]]
        df = pd.DataFrame(data, columns=['goal', 'software', 'platform', 'attack', 'hash'])
        predictions = model.predict(df)
        results = [
            {
                'goal_pentest': goal_pentest_map.get(asset.goal_pentest),
                'type_software': type_software_map.get(asset.type_software),
                'platform': platform_map.get(asset.platform),
                'type_password_attack': type_password_attack_map.get(asset.type_password_attack),
                'hash_type': hash_type_map.get(asset.hash_type),
                'suggested_tool_1': tool_names.get(pred).get('name'),
                'suggested_tool_1_url_name': tool_names.get(pred).get('url_name'),
                'suggested_tool_2': 'Nmap',
                'suggested_tool_2_url_name': 'Nmap'
            }
            for pred in predictions
        ]
    return render(request, 'Tools/user_results.html', {'results': results})

@login_required
def result(request):
    assets = Asset.objects.filter(user=request.user)
    if assets.exists():
        data = [
            [asset.goal_pentest, asset.type_software, asset.platform, asset.type_password_attack, asset.hash_type]
            for asset in assets
        ]
        df = pd.DataFrame(data, columns=['goal', 'software', 'platform', 'attack', 'hash'])
        predictions = model.predict(df)
        results = [
            {
                'asset_id': asset.id,
                'goal_pentest': goal_pentest_map.get(asset.goal_pentest),
                'type_software': type_software_map.get(asset.type_software),
                'platform': platform_map.get(asset.platform),
                'type_password_attack': type_password_attack_map.get(asset.type_password_attack),
                'hash_type': hash_type_map.get(asset.hash_type),
                'suggested_tool_1': tool_names.get(pred).get('name'),
                'suggested_tool_1_url_name': tool_names.get(pred).get('url_name'),
                'suggested_tool_2': 'Nmap',
                'suggested_tool_2_url_name': 'nmap',
                'created_at': asset.created_at
            }
            for asset, pred in zip(assets, predictions)
        ]
    else:
        results = []
    return render(request, 'Tools/result.html', {'results': results})
    
from django.http import JsonResponse

@login_required
def suggestion(request):
    if request.method == 'POST':
        goal_pentest = request.POST.get('goal_pentest')
        type_software = request.POST.get('type_software')
        platform = request.POST.get('platform')
        type_password_attack = request.POST.get('type_password_attack')
        hash_type = request.POST.get('hash_type')
        suggested_tool = request.POST.get('suggested_tool')
        
        UserSuggestion.objects.create(
            user=request.user,
            goal_pentest=goal_pentest,
            type_software=type_software,
            platform=platform,
            type_password_attack=type_password_attack,
            hash_type=hash_type,
            suggested_tool=suggested_tool
        )
        
        # Mengirimkan balasan JSON
        return JsonResponse({'success': True, 'suggested_tool': suggested_tool})
    return JsonResponse({'success': False}, status=400)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Asset

@login_required
def delete_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if asset.user == request.user:
        asset.delete()
        return redirect('result')
    else:
        return HttpResponseForbidden("You are not allowed to delete this asset.")

@login_required
def ncrack_view(request):
    result = None
    if request.method == 'POST':
        form = NcrackForm(request.POST)
        if form.is_valid():
            target_ip = form.cleaned_data['target_ip']
            username = form.cleaned_data['username']
            protocol = form.cleaned_data['protocol']

            # Path to the password file
            password_file_path = '/home/syiqin/NewT/passwords.txt'

            # Execute Ncrack command
            command = f'ncrack -p {protocol} -u {username} -P {password_file_path} {target_ip}'
            try:
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()
            except subprocess.CalledProcessError as e:
                result = f"An error occurred: {e.output.decode()}"
    else:
        form = NcrackForm()

    return render(request, 'Tools/ncrack.html', {'form': form, 'result': result})

@login_required
def nmap(request):
    if request.method == 'POST':
        form = NmapForm(request.POST)
        if form.is_valid():
            target_ip = form.cleaned_data['target_ip']
            scan_type = form.cleaned_data['scan_type']
            # Process the nmap command
            command = f'nmap -{scan_type} {target_ip}'
            try:
                result = subprocess.check_output(command, shell=True).decode()
            except subprocess.CalledProcessError as e:
                result = f"An error occurred: {e.output.decode()}"
            return render(request, 'Tools/nmap.html', {'form': form, 'result': result})
    else:
        form = NmapForm()
    return render(request, 'Tools/nmap.html', {'form': form, 'result': None})

def check_password_strength(password):
    """Check the strength of a password."""
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[ @#$%^&+=]", password) is None
    
    # Calculate the strength
    errors = [length_error, digit_error, uppercase_error, lowercase_error, symbol_error]
    strength = "strong"
    if sum(errors) == 1:
        strength = "medium"
    elif sum(errors) > 1:
        strength = "weak"
    
    return strength

# Example usage:
passwords = []

for pwd in passwords:
    print(f"{pwd}: {check_password_strength(pwd)}")

@login_required
def hydra(request):
    if request.method == 'POST':
        form = HydraForm(request.POST)
        if form.is_valid():
            target_service = form.cleaned_data['target_service']
            target_ip = form.cleaned_data['target_ip']
            username = form.cleaned_data['username']
            password_list = form.cleaned_data['password_list']
            
            # Write the password list to a temporary file
            with open('passwords.txt', 'w') as f:
                f.write(password_list)
            
            # Analyze password strength
            password_strengths = {}
            for password in password_list.splitlines():
                password_strengths[password] = check_password_strength(password)
            
            # Adjust Hydra command based on the service type
            if target_service == 'http-get':
                command = f'hydra -l {username} -P passwords.txt {target_service}://{target_ip}/'
            else:
                command = f'hydra -l {username} -P passwords.txt {target_service}://{target_ip}'
            
            # Limit the number of parallel tasks to avoid SSH configuration issues
            command += ' -t 4'
            
            try:
                result = subprocess.check_output(command, shell=True, text=True)
            except subprocess.CalledProcessError as e:
                result = f"An error occurred: {e.output.decode()}"
                
            return render(request, 'Tools/hydra.html', {'form': form, 'result': result, 'password_strengths': password_strengths})
    else:
        form = HydraForm()
        
    return render(request, 'Tools/hydra.html', {'form': form, 'result': None})