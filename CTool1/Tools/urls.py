from django.contrib import admin
from django.urls import path
from Tools import views as tools_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tools_views.home, name='home'),
    path('signup/', tools_views.signup, name='signup'),
    path('login/', tools_views.user_login, name='login'),
    path('add_asset/', tools_views.add_asset, name='add_asset'),
    path('result/', tools_views.result, name='result'),
    path('run_nmap/', views.run_nmap, name='run_nmap'),
]

