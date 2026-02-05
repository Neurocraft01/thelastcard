"""
Admin configuration for organizations app.
"""

from django.contrib import admin
from .models import Organization, OrganizationInvite


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin for Organization model."""
    
    list_display = (
        'name', 'slug', 'subscription_tier', 'user_count_display',
        'is_active', 'created_at'
    )
    list_filter = ('subscription_tier', 'is_active', 'created_at')
    search_fields = ('name', 'slug', 'email')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {'fields': ('id', 'name', 'slug', 'description')}),
        ('Branding', {
            'fields': ('logo', 'primary_color', 'secondary_color'),
        }),
        ('Contact', {
            'fields': ('email', 'phone', 'website', 'address'),
        }),
        ('Subscription', {
            'fields': (
                'subscription_tier', 'subscription_valid_until',
                'max_users', 'max_cards'
            ),
        }),
        ('Settings', {
            'fields': (
                'allow_custom_themes', 'allow_analytics',
                'allow_password_protection', 'is_active'
            ),
        }),
        ('Domain', {
            'fields': ('custom_domain',),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def user_count_display(self, obj):
        return f"{obj.user_count} / {obj.max_users}"
    user_count_display.short_description = "Users"


@admin.register(OrganizationInvite)
class OrganizationInviteAdmin(admin.ModelAdmin):
    """Admin for organization invites."""
    
    list_display = ('email', 'organization', 'status', 'invited_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('email', 'organization__name')
    readonly_fields = ('id', 'token', 'created_at')
