from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['goal_pentest', 'type_software', 'platform', 'type_password_attack', 'hash_type']

#class HashcatForm(forms.Form):
 #   hash_type = forms.ChoiceField(choices=[('0', 'MD5'), ('1', 'SHA-1'), ('2', 'SHA-256')])
  #  hash_value = forms.CharField(widget=forms.Textarea)

class HydraForm(forms.Form):
    target_service = forms.CharField(max_length=100, help_text="e.g., ftp, ssh, http")
    target_ip = forms.GenericIPAddressField()
    username = forms.CharField(max_length=100)
    password_list = forms.CharField(widget=forms.Textarea, help_text="Enter passwords separated by newlines")

class NmapForm(forms.Form):
    target_ip = forms.GenericIPAddressField()
    scan_type = forms.ChoiceField(choices=[('sT', 'TCP Connect Scan'), ('sS', 'SYN Scan'), ('sP', 'Ping Scan')])

#class JohnTheRipperForm(forms.Form):
 #   hash_type = forms.ChoiceField(choices=[('0', 'MD5'), ('1', 'SHA-1'), ('2', 'SHA-256')])
  #  hash_value = forms.CharField(max_length=256)

#class JohnTheRipperForm(forms.Form):
 #   HASH_TYPE_CHOICES = [
  #      ('MD5', 'MD5'),
   #     ('SHA-1', 'SHA-1'),
    #    ('SHA-256', 'SHA-256')
    #]
    #hash_type = forms.ChoiceField(choices=HASH_TYPE_CHOICES, label='Hash type')
    #hash_value = forms.CharField(label='Hash value', max_length=256)

class NcrackForm(forms.Form):
    protocol_choices = [('ssh', 'SSH'), ('ftp', 'FTP'), ('http', 'HTTP')]
    target_ip = forms.CharField(label='Target IP', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password_list = forms.CharField(label='Password List', widget=forms.Textarea)
    protocol = forms.ChoiceField(label='Protocol', choices=protocol_choices)

