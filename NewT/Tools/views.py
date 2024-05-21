from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import AssetForm, HashcatForm, HydraForm, NmapForm
from .models import Asset
import joblib
import pandas as pd
import subprocess

# Load the model when the server starts
model = joblib.load('model.pkl')

# Mapping of numeric identifiers to tool names
tool_names = {
    0: 'hydra',
    1: 'hashcat'
    # Add more mappings as needed
}

# Mapping of numeric identifiers to human-readable names
goal_pentest_map = {1: 'Web Application', 2: 'Network', 3: 'Cloud'}
type_software_map = {1: 'Web-based', 2: 'Mobile', 3: 'Network'}
platform_map = {1: 'Windows', 2: 'Linux', 3: 'macOS', 4: 'Cloud'}
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
            return redirect('result')
    else:
        form = AssetForm()
    return render(request, 'Tools/add_asset.html', {'form': form})

#@login_required
#def result(request):
 #   assets = Asset.objects.filter(user=request.user)
  #  if assets.exists():
   #     data = [[asset.goal_pentest, asset.type_software, asset.platform, asset.type_password_attack, asset.hash_type] for asset in assets]
    #    df = pd.DataFrame(data, columns=['goal', 'software', 'platform', 'attack', 'hash'])
     #   predictions = model.predict(df)
      #  results = [(tool_names.get(pred, 'Unknown Tool'), 'nmap') for pred in predictions]
    #else:
     #   results = []
    #return render(request, 'Tools/result.html', {'results': results})

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
                'goal_pentest': goal_pentest_map.get(asset.goal_pentest),
                'type_software': type_software_map.get(asset.type_software),
                'platform': platform_map.get(asset.platform),
                'type_password_attack': type_password_attack_map.get(asset.type_password_attack),
                'hash_type': hash_type_map.get(asset.hash_type),
                'suggested_tool_1': tool_names.get(pred),
                'suggested_tool_2': 'nmap'
            }
            for asset, pred in zip(assets, predictions)
        ]
    else:
        results = []
    return render(request, 'Tools/result.html', {'results': results})
#def run_nmap_scan(target):
 #   command = ['nmap', '-Pn', target]
  #  result = subprocess.run(command, capture_output=True, text=True)
   # return result.stdout

#@login_required
#def run_nmap(request):
 #   output = None
  #  if request.method == 'POST':
   #     target = request.POST.get('target', 'example.com')  # Default target
    #    output = run_nmap_scan(target)
    #return render(request, 'Tools/nmap.html', {'output': output})
    
#@login_required
#def nmap(request):
 #   return render(request, 'Tools/nmap.html')

#@login_required
#def hydra(request):
#    return render(request, 'Tools/hydra.html')

#@login_required
#def hashcat(request):
#    return render(request, 'Tools/hashcat.html')    
@login_required
def hashcat(request):
    if request.method == 'POST':
        form = HashcatForm(request.POST)
        if form.is_valid():
            hash_type = form.cleaned_data['hash_type']
            hash_value = form.cleaned_data['hash_value']
            # Process the hashcat command
            command = f'hashcat -m {hash_type} -a 0 {hash_value} hash.dict'
            try:
                result = subprocess.check_output(command, shell=True).decode()
            except subprocess.CalledProcessError as e:
                result = f"An error occurred: {e.output.decode()}"
            return render(request, 'Tools/hashcat.html', {'form': form, 'result': result})
    else:
        form = HashcatForm()
    return render(request, 'Tools/hashcat.html', {'form': form, 'result': None})

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
            # Process the hydra command
            command = f'hydra -l {username} -P passwords.txt {target_service}://{target_ip}'
            try:
                result = subprocess.check_output(command, shell=True).decode()
            except subprocess.CalledProcessError as e:
                result = f"An error occurred: {e.output.decode()}"
            return render(request, 'Tools/hydra.html', {'form': form, 'result': result})
    else:
        form = HydraForm()
    return render(request, 'Tools/hydra.html', {'form': form, 'result': None})   