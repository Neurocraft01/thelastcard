import json
import razorpay
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from .models import CardOrder
from .forms import OrderForm


def get_razorpay_client():
    """Return a configured Razorpay client."""
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class OrderCreateView(LoginRequiredMixin, CreateView):
    """Create a new NFC card order and initiate Razorpay payment."""
    model = CardOrder
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    
    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            form.instance.status = 'payment_pending'
            form.instance.payment_status = 'created'
            order = form.save()

            # Create Razorpay Order
            client = get_razorpay_client()
            amount_in_paise = int(order.total_price * 100)
            razorpay_order = client.order.create({
                'amount': amount_in_paise,
                'currency': 'INR',
                'receipt': str(order.id),
                'notes': {
                    'order_number': order.order_number,
                    'email': self.request.user.email,
                }
            })

            order.razorpay_order_id = razorpay_order['id']
            order.save(update_fields=['razorpay_order_id', 'status', 'payment_status'])

            # Redirect to payment page
            return redirect('orders:payment', pk=order.pk)
        except Exception as e:
            messages.error(self.request, 'There was an error processing your order. Please try again or contact support.')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below and try again.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'profile'):
            profile = self.request.user.profile
            if not context['form'].initial.get('shipping_address') and profile.full_address:
                context['form'].initial['shipping_address'] = profile.full_address
        return context


class OrderPaymentView(LoginRequiredMixin, DetailView):
    """Show Razorpay checkout for the order."""
    model = CardOrder
    template_name = 'orders/order_payment.html'
    context_object_name = 'order'

    def get_queryset(self):
        return CardOrder.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        # If already paid, redirect to detail
        if order.payment_status == 'captured':
            return redirect('orders:order_detail', pk=order.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        context['razorpay_key_id'] = settings.RAZORPAY_KEY_ID
        context['razorpay_order_id'] = order.razorpay_order_id
        context['amount'] = int(order.total_price * 100)
        context['currency'] = 'INR'
        context['user_email'] = self.request.user.email
        context['user_name'] = getattr(self.request.user, 'first_name', '') or self.request.user.email
        context['callback_url'] = self.request.build_absolute_uri(
            reverse('orders:payment_callback', kwargs={'pk': order.pk})
        )
        return context


@method_decorator(csrf_exempt, name='dispatch')
class OrderPaymentCallbackView(View):
    """Handle Razorpay payment callback / verification."""

    def post(self, request, pk):
        order = get_object_or_404(CardOrder, pk=pk)

        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')

        client = get_razorpay_client()

        try:
            # Verify payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature,
            })

            # Payment is verified
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.payment_status = 'captured'
            order.amount_paid = order.total_price
            order.status = 'paid'
            order.save()

            messages.success(request, f'Payment successful! Your order #{order.order_number} has been placed.')
            return redirect('orders:order_detail', pk=order.pk)

        except razorpay.errors.SignatureVerificationError:
            order.payment_status = 'failed'
            order.save(update_fields=['payment_status'])
            messages.error(request, 'Payment verification failed. Please try again or contact support.')
            return redirect('orders:payment', pk=order.pk)

        except Exception as e:
            order.payment_status = 'failed'
            order.save(update_fields=['payment_status'])
            messages.error(request, 'Payment processing error. Please try again.')
            return redirect('orders:payment', pk=order.pk)


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
        return CardOrder.objects.filter(user=self.request.user)


class OrderCancelView(LoginRequiredMixin, View):
    """Cancel an order (only if status is pending or payment_pending)."""
    
    def post(self, request, pk):
        order = get_object_or_404(CardOrder, pk=pk, user=request.user)
        
        if order.status in ('pending', 'payment_pending'):
            order.status = 'cancelled'
            order.save()
            messages.success(request, f'Order #{order.order_number} has been cancelled successfully.')
        else:
            messages.error(request, 'This order cannot be cancelled. Only pending orders can be cancelled.')
        
        return redirect('orders:order_detail', pk=pk)
