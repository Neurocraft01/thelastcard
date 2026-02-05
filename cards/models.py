"""
NFC Card model for managing digital business cards.
Each card has a unique slug for public access.
"""

import uuid
import secrets
import string
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def generate_card_slug():
    """Generate a unique, URL-safe slug for NFC cards."""
    alphabet = string.ascii_lowercase + string.digits
    while True:
        slug = ''.join(secrets.choice(alphabet) for _ in range(8))
        if not NFCCard.objects.filter(url_slug=slug).exists():
            return slug


class NFCCard(models.Model):
    """
    NFC Card model representing a digital business card.
    Each card has a unique URL slug for public access.
    """
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending Activation')
        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        EXPIRED = 'EXPIRED', _('Expired')
        SUSPENDED = 'SUSPENDED', _('Suspended')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Card identification
    card_uid = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Physical NFC card unique identifier (optional)')
    )
    url_slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True,
        blank=True,
        help_text=_('Unique URL slug for public profile access (auto-generated from username)')
    )
    
    # Ownership
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='cards',
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_cards'
    )
    
    # Theme and customization
    theme = models.ForeignKey(
        'themes.Theme',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cards'
    )
    custom_css = models.TextField(blank=True)
    
    # Status and dates
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    activation_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    
    # Privacy settings
    is_private = models.BooleanField(
        default=False,
        help_text=_('If true, card requires password to view')
    )
    password_hash = models.CharField(max_length=128, blank=True)
    hide_from_search = models.BooleanField(default=False)
    
    # QR Code
    qr_code = models.ImageField(
        upload_to='qrcodes/',
        blank=True,
        null=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('NFC card')
        verbose_name_plural = _('NFC cards')
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from user's username if not set."""
        if not self.url_slug and self.user and hasattr(self.user, 'username'):
            self.url_slug = self.user.username
        elif not self.url_slug:
            # Fallback to random slug if no username
            self.url_slug = generate_card_slug()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Card {self.url_slug}"
    
    def get_absolute_url(self):
        """Return the public URL for this card's profile."""
        return reverse('profiles:public_profile', kwargs={'slug': self.url_slug})
    
    def activate(self):
        """Activate the card."""
        self.status = self.Status.ACTIVE
        self.activation_date = timezone.now()
        self.save(update_fields=['status', 'activation_date'])
    
    def deactivate(self):
        """Deactivate the card."""
        self.status = self.Status.INACTIVE
        self.save(update_fields=['status'])
    
    @property
    def is_active(self):
        """Check if card is currently active."""
        if self.status != self.Status.ACTIVE:
            return False
        if self.expiry_date and timezone.now() > self.expiry_date:
            return False
        return True
    
    @property
    def view_count(self):
        """Get total view count for this card."""
        return self.analytics.filter(interaction_type='VIEW').count()
    
    @property
    def public_url(self):
        """Get the full public URL for this card."""
        from django.conf import settings
        return f"{settings.SITE_URL}/u/{self.url_slug}"


class CardAssignment(models.Model):
    """
    Track card assignment history.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card = models.ForeignKey(
        NFCCard,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='card_assignments'
    )
    assigned_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_cards'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = _('card assignment')
        verbose_name_plural = _('card assignments')
        ordering = ['-assigned_at']
    
    def __str__(self):
        return f"Card {self.card.url_slug} assigned to {self.assigned_to.email}"
