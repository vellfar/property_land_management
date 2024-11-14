from django.urls import path
from properties import views

urlpatterns = [
    path('', views.index, name="properties"),  # Includes properties app URLs
    path('transfers/', views.transfers, name="transfers"),  # Includes properties app URLs
]
