# anomaly_detection/admin.py

from django.contrib import admin
from .models import PasswordData

admin.site.register(PasswordData)
