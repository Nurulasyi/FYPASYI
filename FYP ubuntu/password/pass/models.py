# anomaly_detection/models.py

from django.db import models

class PasswordData(models.Model):
    password = models.CharField(max_length=255)
    strength = models.IntegerField()

    def __str__(self):
        return self.password
