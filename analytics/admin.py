"""
Admin configuration for analytics app.
"""

from django.contrib import admin
from .models import (
    ProfileAnalytics, DailyAnalyticsSummary,
    UserAnalyticsSummary, OrganizationAnalytics
)


@admin.register(ProfileAnalytics)
class ProfileAnalyticsAdmin(admin.ModelAdmin):
    """Admin for individual analytics events."""
    
    list_display = (
        'card', 'interaction_type', 'device_type',
        'country', 'timestamp'
    )
    list_filter = ('interaction_type', 'device_type', 'country', 'timestamp')
    search_fields = ('card__url_slug',)
    readonly_fields = (
        'id', 'card', 'interaction_type', 'metadata',
        'visitor_ip_hash', 'user_agent', 'referrer',
        'country', 'city', 'device_type', 'browser', 'os', 'timestamp'
    )
    ordering = ('-timestamp',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(DailyAnalyticsSummary)
class DailyAnalyticsSummaryAdmin(admin.ModelAdmin):
    """Admin for daily analytics summaries."""
    
    list_display = (
        'card', 'date', 'total_views', 'unique_views',
        'total_interactions_display', 'engagement_rate_display'
    )
    list_filter = ('date',)
    search_fields = ('card__url_slug',)
    readonly_fields = (
        'id', 'card', 'date', 'total_views', 'unique_views',
        'contact_saves', 'phone_clicks', 'email_clicks',
        'website_clicks', 'social_clicks', 'shares',
        'mobile_views', 'desktop_views', 'tablet_views',
        'top_countries', 'top_cities', 'top_referrers'
    )
    ordering = ('-date',)
    
    def total_interactions_display(self, obj):
        return obj.total_interactions
    total_interactions_display.short_description = "Interactions"
    
    def engagement_rate_display(self, obj):
        return f"{obj.engagement_rate}%"
    engagement_rate_display.short_description = "Engagement"
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserAnalyticsSummary)
class UserAnalyticsSummaryAdmin(admin.ModelAdmin):
    """Admin for user analytics summaries."""
    
    list_display = (
        'user', 'total_views', 'views_last_30_days',
        'views_trend_percentage', 'updated_at'
    )
    search_fields = ('user__email',)
    readonly_fields = (
        'user', 'total_views', 'total_unique_views',
        'total_contact_saves', 'total_interactions',
        'views_last_30_days', 'views_previous_30_days',
        'views_trend_percentage', 'last_view_at', 'updated_at'
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(OrganizationAnalytics)
class OrganizationAnalyticsAdmin(admin.ModelAdmin):
    """Admin for organization analytics."""
    
    list_display = (
        'organization', 'total_users', 'total_cards',
        'total_views', 'views_last_30_days', 'updated_at'
    )
    search_fields = ('organization__name',)
    readonly_fields = (
        'organization', 'total_users', 'active_users',
        'total_cards', 'active_cards', 'total_views',
        'views_last_30_days', 'top_cards', 'updated_at'
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
