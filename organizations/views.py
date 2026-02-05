"""
Views for organizations app.
"""

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from accounts.mixins import SuperAdminRequiredMixin, AdminRequiredMixin
from .models import Organization


class OrganizationListView(SuperAdminRequiredMixin, ListView):
    """List all organizations (Super Admin only)."""
    model = Organization
    template_name = 'organizations/list.html'
    context_object_name = 'organizations'


class OrganizationDetailView(AdminRequiredMixin, DetailView):
    """View organization details."""
    model = Organization
    template_name = 'organizations/detail.html'
    context_object_name = 'organization'
    
    def get_queryset(self):
        if self.request.user.is_super_admin:
            return Organization.objects.all()
        return Organization.objects.filter(pk=self.request.user.organization.pk)


class OrganizationCreateView(SuperAdminRequiredMixin, CreateView):
    """Create new organization (Super Admin only)."""
    model = Organization
    template_name = 'organizations/create.html'
    fields = ['name', 'description', 'email', 'phone', 'subscription_tier', 'max_users', 'max_cards']
    success_url = reverse_lazy('organizations:list')


class OrganizationEditView(AdminRequiredMixin, UpdateView):
    """Edit organization."""
    model = Organization
    template_name = 'organizations/edit.html'
    fields = ['name', 'description', 'logo', 'primary_color', 'secondary_color', 'email', 'phone', 'website', 'address']
    
    def get_queryset(self):
        if self.request.user.is_super_admin:
            return Organization.objects.all()
        return Organization.objects.filter(pk=self.request.user.organization.pk)
    
    def get_success_url(self):
        return reverse_lazy('organizations:detail', kwargs={'pk': self.object.pk})
