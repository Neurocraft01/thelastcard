"""
Admin configuration for cards app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import NFCCard, CardAssignment


@admin.register(NFCCard)
class NFCCardAdmin(admin.ModelAdmin):
    """Admin for NFC Card model."""
    
    list_display = (
        'url_slug', 'card_uid', 'user_info', 'qr_code_preview', 'status',
        'view_count_display', 'created_at'
    )
    list_filter = ('status', 'is_private', 'created_at')
    search_fields = ('url_slug', 'card_uid', 'user__email')
    readonly_fields = ('id', 'qr_code', 'qr_code_preview_large', 'created_at', 'updated_at', 'view_count_display')
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
            'fields': ('qr_code', 'qr_code_preview_large'),
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

    def user_info(self, obj):
        """Display user email and name."""
        if obj.user:
            details = obj.user.email
            if hasattr(obj.user, 'profile') and obj.user.profile.full_name:
                details += f" ({obj.user.profile.full_name})"
            return details
        return "-"
    user_info.short_description = "Owner"

    def qr_code_preview(self, obj):
        """Small QR preview for list view."""
        if obj.qr_code:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 4px;" />', obj.qr_code.url)
        return "-"
    qr_code_preview.short_description = "QR"

    def qr_code_preview_large(self, obj):
        """Large QR preview for detail view."""
        if obj.qr_code:
            return format_html('<a href="{}" target="_blank"><img src="{}" width="200" height="200" /></a>', obj.qr_code.url, obj.qr_code.url)
        return "No QR Code generated yet."
    qr_code_preview_large.short_description = "QR Preview"


@admin.register(CardAssignment)
class CardAssignmentAdmin(admin.ModelAdmin):
    """Admin for card assignments."""
    
    list_display = ('card', 'assigned_to', 'assigned_by', 'assigned_at')
    list_filter = ('assigned_at',)
    search_fields = ('card__url_slug', 'assigned_to__email')
    readonly_fields = ('id', 'assigned_at')
    raw_id_fields = ('card', 'assigned_to', 'assigned_by')
