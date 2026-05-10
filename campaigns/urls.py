from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_home, name='search_home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_campaign, name='add_campaign'),
    path('scan/', views.scanner, name='scanner'),
    path('results/', views.search_results, name='search_results'),
]
