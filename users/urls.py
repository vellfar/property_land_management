from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    #path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    #path('logout/', views.LogoutView.as_view(), name='logout'),
]
