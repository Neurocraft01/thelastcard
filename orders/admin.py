from django.contrib import admin
from .models import CardOrder, Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """Admin configuration for Coupon model."""

    list_display = ['code', 'discount_type', 'discount_value', 'is_active', 'used_count', 'usage_limit', 'valid_from', 'valid_until']
    list_filter = ['is_active', 'discount_type', 'created_at']
    search_fields = ['code', 'description']
    list_editable = ['is_active']
    readonly_fields = ['used_count', 'created_at']

    fieldsets = (
        ('Coupon Details', {
            'fields': ('code', 'description', 'is_active')
        }),
        ('Discount', {
            'fields': ('discount_type', 'discount_value', 'max_discount', 'min_order_amount')
        }),
        ('Usage & Validity', {
            'fields': ('usage_limit', 'used_count', 'valid_from', 'valid_until')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


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
        ('Coupon & Discount', {
            'fields': ('coupon', 'discount_amount')
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
