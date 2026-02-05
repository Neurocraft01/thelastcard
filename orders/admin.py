from django.contrib import admin
from .models import CardOrder


@admin.register(CardOrder)
class CardOrderAdmin(admin.ModelAdmin):
    """Admin configuration for CardOrder model."""
    
    list_display = ['order_number', 'user', 'card_type', 'quantity', 'status', 'created_at']
    list_filter = ['status', 'card_type', 'created_at']
    search_fields = ['user__email', 'user__username', 'id', 'tracking_number']
    readonly_fields = ['id', 'user', 'created_at', 'updated_at', 'order_number']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'order_number', 'user', 'status', 'created_at', 'updated_at')
        }),
        ('Product Details', {
            'fields': ('card_type', 'quantity', 'custom_text', 'custom_design')
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
