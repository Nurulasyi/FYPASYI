from django.shortcuts import render, redirect, get_object_or_404
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpResponseForbidden
from .forms import AssetForm, HydraForm, NmapForm, MedusaForm, WfuzzForm, UploadCSVForm, UploadModelForm
from .models import Asset, UserResult, ToolResult
from django.core.exceptions import SuspiciousFileOperation
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd
import subprocess
import re
import os


def load_data_from_db():
    records = Asset.objects.all()
    data = [{
        'goal_pentest': record.goal_pentest,
        'type_software': record.type_software,
        'platform': record.platform,
        'type_password_attack': record.type_password_attack,
        'hash_type': record.hash_type,
        'suggest': record.suggest
    } for record in records]
    return pd.DataFrame(data)

def preprocess_data(df):
    le = LabelEncoder()
    for column in df.columns:
        df[column] = le.fit_transform(df[column])
    return df

def prepare_data(df):
    X = df.drop('suggest', axis=1)
    y = df['suggest']
    return X, y

def train_random_forest(X, y):
    print("Train Model function is being execute")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, 'model1.pkl')
    print("Finished executing Train Model function")
    return model

def load_model():
    print("Load Model function is being executed")
    try:
        with open('model1.pkl', 'rb') as f:
            model = joblib.load(f)
    except FileNotFoundError:
        df = load_data_from_db()
        if df.empty:
            return None
        df = preprocess_data(df)
        X, y = prepare_data(df)
        model = train_random_forest(X, y)
    print("Finished executing Load Model function")
    return model

model = joblib.load('model1.pkl')

tool_names = {
    0: {'name': 'Hydra', 'url_name': 'hydra'},
    1: {'name': 'Medusa', 'url_name': 'medusa'},
    2: {'name': 'Wfuzz', 'url_name': 'wfuzz'},
}

goal_pentest_map = {1: 'Web Application', 2: 'Network', 3: 'Cloud'}
type_software_map = {1: 'Web-based', 2: 'Mobile', 3: 'Network'}
platform_map = {1: 'Windows', 2: 'Linux', 3: 'MacOS', 4: 'Cloud'}
type_password_attack_map = {1: 'Brute Force', 2: 'Dictionary', 3: 'Hybrid'}
hash_type_map = {0: 'MD5', 1: 'SHA-1', 2: 'SHA-256'}

def home(request):
    print('Home function is being executed')
    return render(request, 'Tool/home.html')
    print("Finished executing Home function")


def signup(request):
    print('Signup function is being executed')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST.get('email') 
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        print("Finished executing Signup function")
        form = UserCreationForm()
    return render(request, 'Tool/signup.html', {'form': form})

def user_login(request):
    print('Login function is being executed')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        print("Finished executing Login function")
        form = AuthenticationForm()
    return render(request, 'Tool/login.html', {'form': form})

@login_required
def add_asset(request):
    print('Fill Requirement function is being executed')
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.user = request.user
            asset.save()
            return redirect('user_results')
    else:
        form = AssetForm()
    print("Finished executing Fill Requirement function.")
    return render(request, 'Tool/add_asset.html', {'form': form})

@login_required
@csrf_protect
def user_results(request):
    print('Tool Suggestion Result function is being executed.')
    if request.method == "POST":
        goal_pentest = request.POST.get('goal_pentest')
        type_software = request.POST.get('type_software')
        platform = request.POST.get('platform')
        type_password_attack = request.POST.get('type_password_attack')
        hash_type = request.POST.get('hash_type')
        suggested_tool = request.POST.get('suggested_tool')
        
        print(f'User {request.user.username} disagree, User submitted user results with goal: {goal_pentest}, type_software: {type_software}, platform: {platform}, type_password_attack: {type_password_attack}, hash_type: {hash_type}, suggested_tool: {suggested_tool}')
        
        UserResult.objects.create(
            user=request.user,
            goal_pentest=goal_pentest,
            type_software=type_software,
            platform=platform,
            type_password_attack=type_password_attack,
            hash_type=hash_type,
            suggested_tool_1=suggested_tool,
            suggested_tool_2='Nmap',
            user_agreed=False
            
        )
        
        return JsonResponse({'success': True})

    asset = Asset.objects.filter(user=request.user).order_by('-created_at').first()
    results = []
    if asset:
        data = [[asset.goal_pentest, asset.type_software, asset.platform, asset.type_password_attack, asset.hash_type]]
        df = pd.DataFrame(data, columns=['goal', 'software', 'platform', 'attack', 'hash'])
        predictions = model.predict(df)
        for pred in predictions:
            result = {
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
            results.append(result)
            
            print(f'User {request.user.username} agreed with shown results goal: {result["goal_pentest"]}, type_software: {result["type_software"]}, platform: {result["platform"]}, type_password_attack: {result["type_password_attack"]}, hash_type: {result["hash_type"]}, suggested_tool_1: {result["suggested_tool_1"]}, suggested_tool_2: {result["suggested_tool_2"]}')
            
            UserResult.objects.create(
                user=request.user,
                goal_pentest=result['goal_pentest'],
                type_software=result['type_software'],
                platform=result['platform'],
                type_password_attack=result['type_password_attack'],
                hash_type=result['hash_type'],
                suggested_tool_1=result['suggested_tool_1'],
                suggested_tool_2=result['suggested_tool_2'],
                user_agreed=True
            )
    print("Finished executing Tool Suggestion Result function")
    return render(request, 'Tool/user_results.html', {'results': results})

@login_required
def result(request):
    print('All Suggestion Result function is being executed')
    user_results = UserResult.objects.filter(user=request.user)
    results = []
    for user_result in user_results:
        result = {
            'result_id': user_result.id,
            'goal_pentest': user_result.goal_pentest,
            'type_software': user_result.type_software,
            'platform': user_result.platform,
            'type_password_attack': user_result.type_password_attack,
            'hash_type': user_result.hash_type,
            'suggested_tool_1': user_result.suggested_tool_1,
            'suggested_tool_1_url_name': user_result.suggested_tool_1,
            'suggested_tool_2': user_result.suggested_tool_2,
            'suggested_tool_2_url_name': user_result.suggested_tool_2,
            'created_at': user_result.created_at
        }
        results.append(result)

    print("Finished executing All Suggestion Result function")
    return render(request, 'Tool/result.html', {'results': results})


@login_required
def dashboard(request):
    print('Dashboard function is being executed')
    return render(request, 'Tool/dashboard.html', {'username': request.user.username})
    print("Finished executing Dasboard function")

@login_required
def historyresults(request):
    print('Tool History function is being executed')
    results = ToolResult.objects.filter(user=request.user).order_by('-created_at')
    print("Finished executing Tool History function")
    return render(request, 'Tool/historyresults.html', {'results': results})

@login_required
def delete_asset(request, asset_id):
    print('Deleting Suggestion function is being executed')
    user_result = get_object_or_404(UserResult, id=asset_id)
    if user_result.user == request.user:
        user_result.delete()
        return redirect('result')
    else:
        print("Finished executing Deleting Suggestion function")
        return HttpResponseForbidden("You are not allowed to delete this result.")
        
def check_password_strength(password):
    print('Checking Password Strength is being executed')
    """Simple password strength checker."""
    if len(password) < 6:
        return "Weak"
    elif len(password) < 10:
        return "Moderate"
    else:
        print("Finished executing Checking Password Strength function")
        return "Strong"

@login_required
def hydra(request):
    print('Hydra function is being executed')
    result = None
    password_strengths = {}
    if request.method == 'POST':
        form = HydraForm(request.POST, request.FILES)
        if form.is_valid():
            target_service = form.cleaned_data['target_service']
            target_ip = form.cleaned_data['target_ip']
            username = form.cleaned_data['username']
            password_file = request.FILES['password_file']

            fs = FileSystemStorage()
            filename = fs.save(password_file.name, password_file)
            uploaded_file_path = fs.path(filename)

            with open(uploaded_file_path, 'r') as f:
                password_list = f.readlines()
                for password in password_list:
                    password = password.strip()
                    password_strengths[password] = check_password_strength(password)

            if target_service == 'http-get':
                command = f'hydra -l {username} -P {uploaded_file_path} {target_service}://{target_ip}/'
            else:
                command = f'hydra -l {username} -P {uploaded_file_path} {target_service}://{target_ip}'

            command += ' -t 4'

            try:
                result = subprocess.check_output(command, shell=True, text=True)
            except subprocess.CalledProcessError as e:
                result = f"An error occurred: {e.output.decode()}"

            ToolResult.objects.create(user=request.user, tool_name="Hydra", result=result)
            fs.delete(filename)  
            print("Successfully executing Hydra function")
            return render(request, 'Tool/hydra.html', {'form': form, 'result': result, 'password_strengths': password_strengths})

    else:
        form = HydraForm()

    print("Finished executing Hydra function")
    return render(request, 'Tool/hydra.html', {'form': form, 'result': None, 'password_strengths': password_strengths})
    
def remove_ansi_escape_sequences(text):
    print('Removing ansi is being executed')
    ansi_escape = re.compile(r'''
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    ''', re.VERBOSE)
    return ansi_escape.sub('', text)
    
@login_required
def medusa_view(request):
    print('Medusa function is being executed')
    result = None
    password_strengths = {}
    if request.method == 'POST':
        form = MedusaForm(request.POST, request.FILES)
        if form.is_valid():
            target_ip = form.cleaned_data['target_ip']
            username = form.cleaned_data['username']
            password_file = request.FILES['password_file']
            protocol = form.cleaned_data['protocol']

            fs = FileSystemStorage()
            filename = fs.save(password_file.name, password_file)
            uploaded_file_path = fs.path(filename)

            with open(uploaded_file_path, 'r') as f:
                password_list = f.readlines()
                for password in password_list:
                    password = password.strip()
                    password_strengths[password] = check_password_strength(password)

            command = f'medusa -h {target_ip} -u {username} -P {uploaded_file_path} -M {protocol}'
            try:
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()
            except subprocess.CalledProcessError as e:
                result = f"An error occurred: {e.output.decode()}"

            ToolResult.objects.create(user=request.user, tool_name="Medusa", result=result)
            fs.delete(filename)  
            print("Successfully executing Medusa function")
            return render(request, 'Tool/medusa.html', {'form': form, 'result': result, 'password_strengths': password_strengths})

    else:
        form = MedusaForm()

    print("Finished executing Medusa function")
    return render(request, 'Tool/medusa.html', {'form': form, 'result': None, 'password_strengths': password_strengths})
    
    
@login_required
def nmap(request):
    print('Nmap function is being executed')
    if request.method == 'POST':
        form = NmapForm(request.POST)
        if form.is_valid():
            target_ip = form.cleaned_data['target_ip']
            scan_type = form.cleaned_data['scan_type']

            if scan_type == 'sS':
                command = f'sudo nmap -{scan_type} {target_ip}'
            else:
                command = f'nmap -{scan_type} {target_ip}'
            try:
                result = subprocess.check_output(command, shell=True).decode()
            except subprocess.CalledProcessError as e:
                result = f"An error occurred: {e.output.decode()}"

            ToolResult.objects.create(user=request.user, tool_name="Nmap", result=result)
            print("Successfully executing Nmap function")
            print("Finished executing Nmap function")
            return render(request, 'Tool/nmap.html', {'form': form, 'result': result})
    else:
        form = NmapForm()
    return render(request, 'Tool/nmap.html', {'form': form, 'result': None})

@login_required
def wfuzz_view(request):
    print('Wfuzz function is being executed')
    result = None
    if request.method == 'POST':
        form = WfuzzForm(request.POST, request.FILES)
        if form.is_valid():
            target_url = form.cleaned_data['target_url']
            wordlist_file = request.FILES['wordlist_file']

            fs = FileSystemStorage()
            filename = fs.save(wordlist_file.name, wordlist_file)
            uploaded_file_path = fs.path(filename)

            command = f'wfuzz -c -z file,{uploaded_file_path} -u {target_url}'
            try:
                raw_result = subprocess.check_output(command, shell=True, text=True)
                result = remove_ansi_escape_sequences(raw_result)
            except subprocess.CalledProcessError as e:
                result = f"An error occurred: {e.output.decode()}"

            ToolResult.objects.create(user=request.user, tool_name="Wfuzz", result=result)
            fs.delete(filename)  
            print("Successfully executing Wfuzz function")
    else:
        form = WfuzzForm()

    print("Finished executing Wfuzz function")
    return render(request, 'Tool/wfuzz.html', {'form': form, 'result': result})

@login_required
def delete_tool_result(request, result_id):
    print('Deleting tool function is being executed')
    tool_result = get_object_or_404(ToolResult, id=result_id)
    if tool_result.user == request.user:
        tool_result.delete()
        return redirect('historyresults')
    else:
        print("Finished executing Deleting Tool function")
        return HttpResponseForbidden("You are not allowed to delete this result.")

@login_required
def train_model_view(request):
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    uploaded_csvs_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded_csvs')
    trained_models_dir = os.path.join(settings.MEDIA_ROOT, 'trained_models')

    if not os.path.exists(uploaded_csvs_dir):
        os.makedirs(uploaded_csvs_dir)

    if not os.path.exists(trained_models_dir):
        os.makedirs(trained_models_dir)

    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            form = UploadCSVForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                file_name = default_storage.save('uploaded_csvs/' + csv_file.name, ContentFile(csv_file.read()))
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)

                data = pd.read_csv(file_path)

                X = data.iloc[:, :-1]
                y = data.iloc[:, -1]

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model.fit(X_train, y_train)

                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)

                pkl_file_path = os.path.join(trained_models_dir, 'model.pkl')
                joblib.dump(model, pkl_file_path)

                download_link = os.path.join(settings.MEDIA_URL, 'trained_models', 'model.pkl')
                return render(request, 'Tool/train_model.html', {
                    'form': form,
                    'upload_model_form': UploadModelForm(),
                    'accuracy': accuracy,
                    'download_link': download_link,
                })

        elif 'model_file' in request.FILES:
            upload_model_form = UploadModelForm(request.POST, request.FILES)
            if upload_model_form.is_valid():
                model_file = request.FILES['model_file']
                model_file_name = 'model.pkl'
                model_file_path = os.path.join(trained_models_dir, model_file_name)

                try:
                    if os.path.exists(model_file_path):
                        os.rename(model_file_path, os.path.join(trained_models_dir, 'model.bak'))

                    with open(model_file_path, 'wb+') as destination:
                        for chunk in model_file.chunks():
                            destination.write(chunk)

                    return render(request, 'Tool/train_model.html', {
                        'form': UploadCSVForm(),
                        'upload_model_form': upload_model_form,
                        'message': 'Model uploaded successfully and the old model was changed into .bak file.'
                    })

                except SuspiciousFileOperation:
                    return render(request, 'Tool/train_model.html', {
                        'form': UploadCSVForm(),
                        'upload_model_form': upload_model_form,
                        'message': 'Invalid file operation detected.'
                    })

    else:
        form = UploadCSVForm()
        upload_model_form = UploadModelForm()

    return render(request, 'Tool/train_model.html', {
        'form': form,
        'upload_model_form': upload_model_form
    })
