from django.contrib import admin
from .models import CardOrder


@admin.register(CardOrder)
class CardOrderAdmin(admin.ModelAdmin):
    """Admin configuration for CardOrder model."""
    
    list_display = ['order_number', 'user', 'card_type', 'quantity', 'status', 'payment_status', 'amount_paid', 'created_at']
    list_filter = ['status', 'payment_status', 'card_type', 'created_at']
    search_fields = ['user__email', 'id', 'tracking_number', 'razorpay_order_id', 'razorpay_payment_id']
    readonly_fields = ['id', 'user', 'created_at', 'updated_at', 'order_number', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'order_number', 'user', 'status', 'created_at', 'updated_at')
        }),
        ('Product Details', {
            'fields': ('card_type', 'quantity', 'custom_text', 'custom_design')
        }),
        ('Payment Details', {
            'fields': ('payment_status', 'amount_paid', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature')
        }),
        ('Shipping & Tracking', {
            'fields': ('shipping_address', 'tracking_number')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def order_number(self, obj):
        return obj.order_number
    order_number.short_description = 'Order #'
