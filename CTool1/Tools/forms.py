from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['goal', 'typeS', 'toolsC', 'platform']
        labels = {
            'goal': 'Penetration Testing Goal',
            'typeS': 'Asset Type',
            'toolsC': 'Tools Category',
            'platform': 'Target Platform',
        }
