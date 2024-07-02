from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('add_asset/', views.add_asset, name='add_asset'),
    path('hydra/', views.hydra, name='hydra'),  # Nama view dalam huruf kecil
    path('ncrack/', views.ncrack_view, name='ncrack'),  # Nama view dalam huruf kecil
    path('nmap/', views.nmap, name='Nmap'),  # Nama view dalam huruf kecil
    path('medusa/', views.medusa_view, name='medusa'),
    path('aircrackng/', views.aircrackng_view, name='aircrackng'),
    # Tambahkan path untuk tool lain di sini
    path('user_results/', views.user_results, name='user_results'),
    path('result/', views.result, name='result'),
    path('suggestion/', views.suggestion, name='suggestion'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('delete_asset/<int:asset_id>/', views.delete_asset, name='delete_asset'),
]
