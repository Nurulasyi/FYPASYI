from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    GOAL_CHOICES = [
        (1, 'Web App'),
        (2, 'Network'),
        (3, 'Cloud'),
    ]

    TYPE_CHOICES = [
        (1, 'Web-Based'),
        (2, 'Mobile'),
        (3, 'Network'),
    ]

    TOOL_CHOICES = [
        (1, 'Web App'),
        (2, 'Network'),
        (3, 'Code Analysis'),
        (4, 'Password Cracking'),
    ]

    PLATFORM_CHOICES = [
        (1, 'Windows'),
        (2, 'Linux'),
        (3, 'MacOS'),
        (4, 'Cloud'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.IntegerField(choices=GOAL_CHOICES)
    typeS = models.IntegerField(choices=TYPE_CHOICES)
    toolsC = models.IntegerField(choices=TOOL_CHOICES)
    platform = models.IntegerField(choices=PLATFORM_CHOICES)

