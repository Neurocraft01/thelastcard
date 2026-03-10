"""
Views for cards app.
"""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from .models import NFCCard


class CardListView(LoginRequiredMixin, ListView):
    """List user's cards."""
    model = NFCCard
    template_name = 'cards/list.html'
    context_object_name = 'cards'
    
    def get_queryset(self):
        return NFCCard.objects.filter(user=self.request.user)


class CardDetailView(LoginRequiredMixin, DetailView):
    """View card details."""
    model = NFCCard
    template_name = 'cards/detail.html'
    context_object_name = 'card'
    
    def get_queryset(self):
        if self.request.user.is_super_admin:
            return NFCCard.objects.all()
        elif self.request.user.is_admin and self.request.user.organization:
            return NFCCard.objects.filter(user__organization=self.request.user.organization)
        return NFCCard.objects.filter(user=self.request.user)


class CardCreateView(LoginRequiredMixin, CreateView):
    """Create new card."""
    model = NFCCard
    template_name = 'cards/create.html'
    fields = ['card_uid', 'url_slug']
    success_url = reverse_lazy('cards:list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        if self.request.user.is_regular_user:
            form.instance.user = self.request.user
        messages.success(self.request, 'Card created successfully!')
        return super().form_valid(form)


class CardEditView(LoginRequiredMixin, UpdateView):
    """Edit card."""
    model = NFCCard
    template_name = 'cards/edit.html'
    fields = ['url_slug', 'theme', 'is_private', 'hide_from_search']
    success_url = reverse_lazy('cards:list')
    
    def get_queryset(self):
        if self.request.user.is_super_admin:
            return NFCCard.objects.all()
        return NFCCard.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Card updated successfully!')
        return super().form_valid(form)


class CardDeleteView(LoginRequiredMixin, DeleteView):
    """Delete card."""
    model = NFCCard
    template_name = 'cards/delete.html'
    success_url = reverse_lazy('cards:list')
    
    def get_queryset(self):
        if self.request.user.is_super_admin:
            return NFCCard.objects.all()
        return NFCCard.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Card deleted successfully!')
        return super().delete(request, *args, **kwargs)


class CardActivateView(LoginRequiredMixin, View):
    """Activate a card."""
    
    def post(self, request, pk):
        card = get_object_or_404(NFCCard, pk=pk)
        
        # Check permissions
        if not request.user.is_super_admin:
            if request.user.is_admin:
                if not (card.user and card.user.organization == request.user.organization):
                    messages.error(request, 'Permission denied.')
                    return redirect('cards:list')
            elif card.user != request.user:
                messages.error(request, 'Permission denied.')
                return redirect('cards:list')
        
        card.activate()
        messages.success(request, 'Card activated successfully!')
        return redirect('cards:detail', pk=pk)


class CardDeactivateView(LoginRequiredMixin, View):
    """Deactivate a card."""
    
    def post(self, request, pk):
        card = get_object_or_404(NFCCard, pk=pk)
        
        # Check permissions
        if not request.user.is_super_admin:
            if request.user.is_admin:
                if not (card.user and card.user.organization == request.user.organization):
                    messages.error(request, 'Permission denied.')
                    return redirect('cards:list')
            elif card.user != request.user:
                messages.error(request, 'Permission denied.')
                return redirect('cards:list')
        
        card.deactivate()
        messages.success(request, 'Card deactivated successfully!')
        return redirect('cards:detail', pk=pk)


class CardAssignView(LoginRequiredMixin, View):
    """Assign card to a user."""
    
    def post(self, request, pk):
        from accounts.models import User
        from .models import CardAssignment
        
        card = get_object_or_404(NFCCard, pk=pk)
        user_id = request.POST.get('user_id')
        
        if not user_id:
            messages.error(request, 'Please select a user.')
            return redirect('cards:detail', pk=pk)
        
        try:
            target_user = User.objects.get(pk=user_id)
            
            # Check permissions
            if request.user.is_admin and request.user.organization:
                if target_user.organization != request.user.organization:
                    messages.error(request, 'User must be in your organization.')
                    return redirect('cards:detail', pk=pk)
            
            # Assign card
            card.user = target_user
            card.save()
            
            # Record assignment
            CardAssignment.objects.create(
                card=card,
                assigned_to=target_user,
                assigned_by=request.user
            )
            
            messages.success(request, f'Card assigned to {target_user.email}!')
            
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
        
        return redirect('cards:detail', pk=pk)
