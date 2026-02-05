"""
Admin configuration for cards app.
"""

from django.contrib import admin
from .models import NFCCard, CardAssignment


@admin.register(NFCCard)
class NFCCardAdmin(admin.ModelAdmin):
    """Admin for NFC Card model."""
    
    list_display = (
        'url_slug', 'card_uid', 'user', 'status',
        'view_count_display', 'created_at'
    )
    list_filter = ('status', 'is_private', 'created_at')
    search_fields = ('url_slug', 'card_uid', 'user__email')
    readonly_fields = ('id', 'qr_code', 'created_at', 'updated_at', 'view_count_display')
    raw_id_fields = ('user', 'created_by', 'theme')
    
    fieldsets = (
        (None, {'fields': ('id', 'card_uid', 'url_slug')}),
        ('Ownership', {
            'fields': ('user', 'created_by'),
        }),
        ('Theme', {
            'fields': ('theme', 'custom_css'),
        }),
        ('Status', {
            'fields': ('status', 'activation_date', 'expiry_date'),
        }),
        ('Privacy', {
            'fields': ('is_private', 'password_hash', 'hide_from_search'),
        }),
        ('QR Code', {
            'fields': ('qr_code',),
        }),
        ('Analytics', {
            'fields': ('view_count_display',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def view_count_display(self, obj):
        return obj.view_count
    view_count_display.short_description = "Total Views"


@admin.register(CardAssignment)
class CardAssignmentAdmin(admin.ModelAdmin):
    """Admin for card assignments."""
    
    list_display = ('card', 'assigned_to', 'assigned_by', 'assigned_at')
    list_filter = ('assigned_at',)
    search_fields = ('card__url_slug', 'assigned_to__email')
    readonly_fields = ('id', 'assigned_at')
    raw_id_fields = ('card', 'assigned_to', 'assigned_by')
