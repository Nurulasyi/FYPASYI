from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_pentest = models.IntegerField(choices=[(1, 'Web Application'), (2, 'Network'), (3, 'Cloud')])
    type_software = models.IntegerField(choices=[(1, 'Web-based'), (2, 'Mobile'), (3, 'Network')])
    platform = models.IntegerField(choices=[(1, 'Windows'), (2, 'Linux'), (3, 'macOS'), (4, 'Cloud')])
    type_password_attack = models.IntegerField(choices=[(1, 'Brute Force'), (2, 'Dictionary'), (3, 'Hybrid')])
    hash_type = models.IntegerField(choices=[(0, 'MD5'), (1, 'SHA-1'), (2, 'SHA-256')])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Asset for user {self.user.username}"
        
class UserSuggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_pentest = models.CharField(max_length=100)
    type_software = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    type_password_attack = models.CharField(max_length=100)
    hash_type = models.CharField(max_length=100)
    suggested_tool = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.suggested_tool}"      