from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Define the fields to display in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
    
    # Fields to use as filters in the admin list view
    list_filter = ('role', 'is_active', 'is_staff')
    
    # Fields to search for in the admin search bar
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Fields to display on the "Edit User" page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'nin')}),
        ('Roles & Permissions', {'fields': ('role', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Status', {'fields': ('is_active',)}),
    )
    
    # Fields to display on the "Add User" page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2'),
        }),
    )
    
    # Default ordering in the admin panel
    ordering = ('username',)

# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)
