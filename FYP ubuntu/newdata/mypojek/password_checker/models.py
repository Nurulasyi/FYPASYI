# password_checker/models.py
from django.db import models

class PasswordData(models.Model):
    password = models.CharField(max_length=100)
    strength = models.IntegerField()

