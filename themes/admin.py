"""
Admin configuration for themes app.
"""

from django.contrib import admin
from .models import Theme


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    """Admin for Theme model."""
    
    list_display = (
        'name', 'slug', 'theme_type', 'is_premium',
        'is_active', 'dark_mode', 'created_at'
    )
    list_filter = ('theme_type', 'is_premium', 'is_active', 'dark_mode')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id', 'created_at', 'updated_at')
    raw_id_fields = ('created_by',)
    
    fieldsets = (
        (None, {'fields': ('id', 'name', 'slug', 'description', 'theme_type')}),
        ('Preview', {
            'fields': ('preview_image',),
        }),
        ('Colors', {
            'fields': (
                'primary_color', 'secondary_color', 'accent_color',
                'background_color', 'text_color'
            ),
        }),
        ('Background', {
            'fields': ('background_type', 'background_gradient', 'background_image'),
        }),
        ('Typography', {
            'fields': ('font_family_heading', 'font_family_body'),
        }),
        ('Layout', {
            'fields': ('border_radius', 'card_shadow', 'dark_mode'),
        }),
        ('Custom CSS', {
            'fields': ('custom_css',),
            'classes': ('collapse',),
        }),
        ('Settings', {
            'fields': ('is_premium', 'is_active', 'is_public', 'created_by'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
