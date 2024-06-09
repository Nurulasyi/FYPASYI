from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('add_asset/', views.add_asset, name='add_asset'),
    path('result/', views.result, name='result'),
    path('nmap/', views.nmap, name='Nmap'),
    path('hydra/', views.hydra, name='Hydra'),
    path('ncrack/', views.ncrack_view, name='Ncrack'),
    #path('john/', views.john, name='John'),
    #path('hashcat/', views.hashcat, name='hashcat'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    #path('run_nmap/', views.run_nmap, name='run_nmap'),
]
