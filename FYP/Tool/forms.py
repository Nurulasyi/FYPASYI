from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['goal_pentest', 'type_software', 'platform', 'type_password_attack', 'hash_type']

class HydraForm(forms.Form):
    target_service = forms.CharField(max_length=100, help_text="")
    target_ip = forms.GenericIPAddressField()
    username = forms.CharField(max_length=100)
    password_list = forms.CharField(widget=forms.Textarea, help_text="Enter passwords separated by newlines")

class NmapForm(forms.Form):
    target_ip = forms.GenericIPAddressField()
    scan_type = forms.ChoiceField(choices=[('sT', 'TCP Connect Scan'), ('sS', 'SYN Scan'), ('sP', 'Ping Scan')])
    
class MedusaForm(forms.Form):
    target_ip = forms.CharField(label='Target IP', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password_list = forms.CharField(label='Password List', widget=forms.Textarea)
    protocol = forms.CharField(label='Protocol', max_length=50)

class WfuzzForm(forms.Form):
    target_url = forms.CharField(label='Target URL', max_length=200)
    wordlist = forms.CharField(label='Wordlist', widget=forms.Textarea)