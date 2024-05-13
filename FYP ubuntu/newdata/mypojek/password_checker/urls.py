# password_checker/urls.py
from django.urls import path
from .views import check_password

urlpatterns = [
    path('check-password/', check_password, name='check_password'),
]
