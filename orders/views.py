from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import CardOrder
from .forms import OrderForm


class OrderCreateView(LoginRequiredMixin, CreateView):
    """Create a new NFC card order."""
    model = CardOrder
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    
    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            messages.success(self.request, 'Your order has been placed successfully! We will contact you shortly.')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'There was an error processing your order. Please try again or contact support.')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below and try again.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get user's profile for pre-filling address if available
        if hasattr(self.request.user, 'profile'):
            profile = self.request.user.profile
            if not context['form'].initial.get('shipping_address') and profile.full_address:
                context['form'].initial['shipping_address'] = profile.full_address
        return context


class OrderListView(LoginRequiredMixin, ListView):
    """List all orders for the current user."""
    model = CardOrder
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        return CardOrder.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    """View details of a specific order."""
    model = CardOrder
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        # Users can only view their own orders
        return CardOrder.objects.filter(user=self.request.user)


class OrderCancelView(LoginRequiredMixin, View):
    """Cancel an order (only if status is pending)."""
    
    def post(self, request, pk):
        order = get_object_or_404(CardOrder, pk=pk, user=request.user)
        
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            messages.success(request, f'Order #{order.order_number} has been cancelled successfully.')
        else:
            messages.error(request, 'This order cannot be cancelled. Only pending orders can be cancelled.')
        
        return redirect('orders:order_detail', pk=pk)
