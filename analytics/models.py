"""
Analytics models for tracking profile views and interactions.
Provides insights for users and admins.
"""

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class ProfileAnalytics(models.Model):
    """
    Track individual interactions with NFC card profiles.
    Captures views, clicks, and other engagements.
    """
    
    class InteractionType(models.TextChoices):
        VIEW = 'VIEW', _('Profile View')
        CONTACT_SAVE = 'CONTACT_SAVE', _('Save Contact')
        PHONE_CLICK = 'PHONE_CLICK', _('Phone Click')
        EMAIL_CLICK = 'EMAIL_CLICK', _('Email Click')
        WEBSITE_CLICK = 'WEBSITE_CLICK', _('Website Click')
        SOCIAL_CLICK = 'SOCIAL_CLICK', _('Social Link Click')
        SHARE = 'SHARE', _('Profile Share')
        QR_DOWNLOAD = 'QR_DOWNLOAD', _('QR Code Download')
        CUSTOM_LINK_CLICK = 'CUSTOM_LINK_CLICK', _('Custom Link Click')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Link to card
    card = models.ForeignKey(
        'cards.NFCCard',
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    
    # Interaction details
    interaction_type = models.CharField(
        max_length=30,
        choices=InteractionType.choices,
        default=InteractionType.VIEW
    )
    
    # Additional data for specific interactions
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Additional interaction data (e.g., which social link was clicked)')
    )
    
    # Visitor information (anonymized for GDPR)
    visitor_ip_hash = models.CharField(
        max_length=64,
        blank=True,
        help_text=_('Hashed IP address for unique visitor counting')
    )
    user_agent = models.CharField(max_length=255, blank=True)
    referrer = models.URLField(blank=True)
    
    # Location (derived from IP, anonymized)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    # Device information
    device_type = models.CharField(
        max_length=20,
        choices=[
            ('MOBILE', 'Mobile'),
            ('TABLET', 'Tablet'),
            ('DESKTOP', 'Desktop'),
            ('OTHER', 'Other'),
        ],
        default='OTHER'
    )
    browser = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=50, blank=True)
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        verbose_name = _('profile analytics')
        verbose_name_plural = _('profile analytics')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['card', 'interaction_type']),
            models.Index(fields=['card', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.card.url_slug} - {self.interaction_type} - {self.timestamp}"


class DailyAnalyticsSummary(models.Model):
    """
    Aggregated daily analytics for performance.
    Pre-computed summaries for faster dashboard loading.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    card = models.ForeignKey(
        'cards.NFCCard',
        on_delete=models.CASCADE,
        related_name='daily_summaries'
    )
    date = models.DateField(db_index=True)
    
    # View counts
    total_views = models.PositiveIntegerField(default=0)
    unique_views = models.PositiveIntegerField(default=0)
    
    # Interaction counts
    contact_saves = models.PositiveIntegerField(default=0)
    phone_clicks = models.PositiveIntegerField(default=0)
    email_clicks = models.PositiveIntegerField(default=0)
    website_clicks = models.PositiveIntegerField(default=0)
    social_clicks = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    
    # Device breakdown
    mobile_views = models.PositiveIntegerField(default=0)
    desktop_views = models.PositiveIntegerField(default=0)
    tablet_views = models.PositiveIntegerField(default=0)
    
    # Top locations (JSON: {"US": 50, "UK": 30, ...})
    top_countries = models.JSONField(default=dict)
    top_cities = models.JSONField(default=dict)
    
    # Top referrers
    top_referrers = models.JSONField(default=dict)
    
    class Meta:
        verbose_name = _('daily analytics summary')
        verbose_name_plural = _('daily analytics summaries')
        ordering = ['-date']
        unique_together = ['card', 'date']
    
    def __str__(self):
        return f"{self.card.url_slug} - {self.date}"
    
    @property
    def total_interactions(self):
        """Get total non-view interactions for the day."""
        return (
            self.contact_saves +
            self.phone_clicks +
            self.email_clicks +
            self.website_clicks +
            self.social_clicks +
            self.shares
        )
    
    @property
    def engagement_rate(self):
        """Calculate engagement rate (interactions / views)."""
        if self.total_views == 0:
            return 0
        return round((self.total_interactions / self.total_views) * 100, 2)


class UserAnalyticsSummary(models.Model):
    """
    Aggregated analytics summary for a user (across all their cards).
    """
    
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='analytics_summary',
        primary_key=True
    )
    
    # Totals
    total_views = models.PositiveIntegerField(default=0)
    total_unique_views = models.PositiveIntegerField(default=0)
    total_contact_saves = models.PositiveIntegerField(default=0)
    total_interactions = models.PositiveIntegerField(default=0)
    
    # Current period (last 30 days)
    views_last_30_days = models.PositiveIntegerField(default=0)
    views_previous_30_days = models.PositiveIntegerField(default=0)
    
    # Trends
    views_trend_percentage = models.FloatField(default=0)
    
    # Last activity
    last_view_at = models.DateTimeField(null=True, blank=True)
    
    # Last updated
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('user analytics summary')
        verbose_name_plural = _('user analytics summaries')
    
    def __str__(self):
        return f"Analytics for {self.user.email}"


class OrganizationAnalytics(models.Model):
    """
    Aggregated analytics for an entire organization.
    """
    
    organization = models.OneToOneField(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='analytics_summary',
        primary_key=True
    )
    
    # User stats
    total_users = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    
    # Card stats
    total_cards = models.PositiveIntegerField(default=0)
    active_cards = models.PositiveIntegerField(default=0)
    
    # View stats
    total_views = models.PositiveIntegerField(default=0)
    views_last_30_days = models.PositiveIntegerField(default=0)
    
    # Top performing cards
    top_cards = models.JSONField(default=list)
    
    # Last updated
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('organization analytics')
        verbose_name_plural = _('organization analytics')
    
    def __str__(self):
        return f"Analytics for {self.organization.name}"
