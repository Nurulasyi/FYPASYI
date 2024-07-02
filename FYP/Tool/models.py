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
        
class UserResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_pentest = models.CharField(max_length=255)
    type_software = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    type_password_attack = models.CharField(max_length=255)
    hash_type = models.CharField(max_length=255)
    suggested_tool_1 = models.CharField(max_length=255)
    suggested_tool_2 = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.created_at}' 
        
class ToolResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool_name = models.CharField(max_length=100)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tool_name} - {self.created_at}"
        