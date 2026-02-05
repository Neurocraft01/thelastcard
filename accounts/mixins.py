"""
Mixins for role-based access control.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


class SuperAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Require Super Admin role to access view."""
    
    def test_func(self):
        return self.request.user.is_super_admin
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('accounts:login')
        messages.error(self.request, 'You do not have permission to access this page.')
        return redirect('accounts:dashboard_redirect')


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Require Admin or Super Admin role to access view."""
    
    def test_func(self):
        return self.request.user.is_admin or self.request.user.is_super_admin
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('accounts:login')
        messages.error(self.request, 'You do not have permission to access this page.')
        return redirect('accounts:dashboard_redirect')


class UserRequiredMixin(LoginRequiredMixin):
    """Require any authenticated user to access view."""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)



