from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('Tresults/', views.historyresults, name='historyresults'),
    path('add_asset/', views.add_asset, name='add_asset'),
    path('hydra/', views.hydra, name='hydra'),  # Nama view dalam huruf kecil
    path('nmap/', views.nmap, name='Nmap'),  # Nama view dalam huruf kecil
    path('medusa/', views.medusa_view, name='medusa'),
    path('wfuzz/', views.wfuzz_view, name='wfuzz'),
    path('hydra/', views.hydra, name='Hydra'),  # Nama view dalam huruf kecil
    path('nmap/', views.nmap, name='Nmap'),  # Nama view dalam huruf kecil
    path('medusa/', views.medusa_view, name='Medusa'),
    path('wfuzz/', views.wfuzz_view, name='Wfuzz'),
    path('user_results/', views.user_results, name='user_results'),
    path('result/', views.result, name='result'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('delete_tool_result/<int:result_id>/', views.delete_tool_result, name='delete_tool_result'),
    path('delete_asset/<int:asset_id>/', views.delete_asset, name='delete_asset'),
]
