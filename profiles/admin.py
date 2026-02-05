"""
Admin configuration for profiles app.
"""

from django.contrib import admin
from .models import UserProfile, ProfileContent


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model."""
    
    list_display = (
        'full_name', 'user', 'company', 'designation',
        'completion_percentage', 'updated_at'
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('full_name', 'user__email', 'company')
    readonly_fields = ('completion_percentage', 'created_at', 'updated_at')
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Personal Information', {
            'fields': ('full_name', 'first_name', 'last_name', 'bio'),
        }),
        ('Media', {
            'fields': ('profile_photo', 'cover_photo'),
        }),
        ('Professional', {
            'fields': ('company', 'designation', 'department'),
        }),
        ('Contact', {
            'fields': (
                'phone_primary', 'phone_secondary',
                'email_public', 'website'
            ),
        }),
        ('Location', {
            'fields': (
                'address_line1', 'address_line2', 'city',
                'state', 'country', 'postal_code'
            ),
        }),
        ('Social Links', {
            'fields': ('social_links',),
        }),
        ('Custom Fields', {
            'fields': ('custom_fields',),
            'classes': ('collapse',),
        }),
        ('Display Settings', {
            'fields': (
                'show_profile_photo', 'show_cover_photo',
                'show_save_contact_button', 'show_share_button',
                'show_qr_code'
            ),
        }),
        ('Stats', {
            'fields': ('completion_percentage', 'created_at', 'updated_at'),
        }),
    )


@admin.register(ProfileContent)
class ProfileContentAdmin(admin.ModelAdmin):
    """Admin for profile content sections."""
    
    list_display = ('title', 'profile', 'content_type', 'order', 'is_visible')
    list_filter = ('content_type', 'is_visible')
    search_fields = ('title', 'profile__full_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    raw_id_fields = ('profile',)
    ordering = ('profile', 'order')
