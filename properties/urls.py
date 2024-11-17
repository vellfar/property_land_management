from django.urls import path
from properties import views

urlpatterns = [
    path('', views.index, name="properties"),  # Includes properties app URLs
    path('transfers/', views.transfers, name="transfers"),  # Includes properties app URLs
    path('properties/', views.index, name='properties_index'),
    path('properties/<int:property_id>/edit/', views.edit_property, name='edit_property'),
    path('properties/<int:property_id>/view/', views.view_property, name='view_property'),
    path('properties/<int:property_id>/delete/confirm/', views.confirm_delete_property, name='confirm_delete_property'),
    path('add_property/', views.add_property, name='add_property'),
    path('initiate-transfer/', views.initiate_transfer, name='initiate_transfer'),
    path('confirm-transfer', views.confirm_transfer, name="confirm-transfer"),
]
