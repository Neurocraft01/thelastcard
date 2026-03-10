"""
Organization model for multi-tenant support.
Organizations group multiple users under a single admin.
"""

import uuid
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Organization(models.Model):
    """
    Organization/Company model for multi-tenant architecture.
    Each Admin can manage one organization with multiple users.
    """
    
    class SubscriptionTier(models.TextChoices):
        FREE = 'FREE', _('Free')
        STARTER = 'STARTER', _('Starter')
        PROFESSIONAL = 'PROFESSIONAL', _('Professional')
        ENTERPRISE = 'ENTERPRISE', _('Enterprise')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    description = models.TextField(blank=True)
    
    # Branding
    logo = models.ImageField(upload_to='organizations/logos/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#6366f1')  # Hex color
    secondary_color = models.CharField(max_length=7, default='#4f46e5')
    
    # Domain and settings
    custom_domain = models.CharField(max_length=255, blank=True, unique=True, null=True)
    website = models.URLField(blank=True)
    
    # Contact information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Subscription
    subscription_tier = models.CharField(
        max_length=20,
        choices=SubscriptionTier.choices,
        default=SubscriptionTier.FREE
    )
    subscription_valid_until = models.DateTimeField(null=True, blank=True)
    max_users = models.PositiveIntegerField(default=5)
    max_cards = models.PositiveIntegerField(default=10)
    
    # Settings
    allow_custom_themes = models.BooleanField(default=False)
    allow_analytics = models.BooleanField(default=True)
    allow_password_protection = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure unique slug
            original_slug = self.slug
            counter = 1
            while Organization.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    @property
    def admin_user(self):
        """Get the admin user of this organization."""
        from accounts.models import User
        return self.members.filter(role=User.Role.ADMIN).first()
    
    @property
    def user_count(self):
        """Get total number of users in organization."""
        return self.members.count()
    
    @property
    def card_count(self):
        """Get total number of cards in organization."""
        return sum(member.cards.count() for member in self.members.all())
    
    @property
    def can_add_user(self):
        """Check if organization can add more users."""
        return self.user_count < self.max_users
    
    @property
    def can_add_card(self):
        """Check if organization can add more cards."""
        return self.card_count < self.max_cards


class OrganizationInvite(models.Model):
    """
    Track pending invitations to join an organization.
    """
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        ACCEPTED = 'ACCEPTED', _('Accepted')
        DECLINED = 'DECLINED', _('Declined')
        EXPIRED = 'EXPIRED', _('Expired')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='invites'
    )
    email = models.EmailField()
    invited_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='sent_invites'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('organization invite')
        verbose_name_plural = _('organization invites')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invite to {self.email} for {self.organization.name}"
