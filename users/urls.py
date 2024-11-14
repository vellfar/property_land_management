from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    #path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    #path('logout/', views.LogoutView.as_view(), name='logout'),
]
