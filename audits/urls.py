from django.urls import path
from audits import views

urlpatterns = [
    path('', views.index, name='audits'),
]
