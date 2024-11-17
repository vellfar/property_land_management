from django.http import HttpResponseForbidden
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator to restrict view access to users with specific roles.
    :param allowed_roles: List of allowed roles (e.g., [1, 2])
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have permission to access this page.")
        return _wrapped_view
    return decorator

def is_admin(view_func):
    """Decorator to restrict access to Admins."""
    return role_required([1])(view_func)

def is_government_official(view_func):
    """Decorator to restrict access to Government Officials."""
    return role_required([2])(view_func)

def is_landowner(view_func):
    """Decorator to restrict access to Landowners."""
    return role_required([3])(view_func)
