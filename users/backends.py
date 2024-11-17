from django.contrib.auth.backends import ModelBackend
from django.shortcuts import redirect

class RoleBasedRedirectBackend(ModelBackend):
    """
    Custom backend to handle role-based redirection after login.
    """
    def user_dashboard_redirect(self, user):
        """
        Redirect user based on their role.
        :param user: Authenticated User instance
        """
        if user.role == 1:  # Admin
            return redirect('admin_dashboard')
        elif user.role == 2:  # Government Official
            return redirect('gov_dashboard')
        elif user.role == 3:  # Landowner
            return redirect('landowner_dashboard')
        return redirect('default_dashboard')  # Fallback if role is unknown
