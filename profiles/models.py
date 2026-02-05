"""
User Profile model for NFC card content.
Contains all the information displayed on the public profile page.
"""

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    """
    Extended user profile for NFC card content.
    Contains personal and professional information.
    """
    
    # Link to user
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True
    )
    
    # Personal Information
    full_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    
    # Profile Media
    profile_photo = models.ImageField(
        upload_to='profiles/photos/',
        blank=True,
        null=True
    )
    cover_photo = models.ImageField(
        upload_to='profiles/covers/',
        blank=True,
        null=True
    )
    
    # Professional Information
    bio = models.TextField(
        blank=True,
        max_length=500,
        help_text=_('Brief bio or tagline (max 500 characters)')
    )
    company = models.CharField(max_length=200, blank=True)
    designation = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('Job title or role')
    )
    department = models.CharField(max_length=100, blank=True)
    
    # Contact Information
    phone_primary = models.CharField(max_length=20, blank=True)
    phone_secondary = models.CharField(max_length=20, blank=True)
    email_public = models.EmailField(
        blank=True,
        help_text=_('Public email (different from login email if needed)')
    )
    website = models.URLField(blank=True)
    
    # Location
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Social Media Links (JSON structure for flexibility)
    social_links = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Social media links in format: {"platform": "url"}')
    )
    
    # Custom Fields (JSON for extensibility)
    custom_fields = models.JSONField(
        default=list,
        blank=True,
        help_text=_('Custom fields in format: [{"label": "", "value": "", "icon": ""}]')
    )
    
    # Settings
    show_profile_photo = models.BooleanField(default=True)
    show_cover_photo = models.BooleanField(default=True)
    show_save_contact_button = models.BooleanField(default=True)
    show_share_button = models.BooleanField(default=True)
    show_qr_code = models.BooleanField(default=True)
    
    # Profile completion tracking
    completion_percentage = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
    
    def __str__(self):
        return self.full_name or self.user.email
    
    def save(self, *args, **kwargs):
        # Calculate completion percentage
        self.completion_percentage = self.calculate_completion()
        super().save(*args, **kwargs)
    
    def calculate_completion(self):
        """Calculate profile completion percentage."""
        fields_to_check = [
            ('full_name', 15),
            ('profile_photo', 15),
            ('bio', 10),
            ('company', 10),
            ('designation', 10),
            ('phone_primary', 10),
            ('email_public', 10),
            ('website', 5),
            ('city', 5),
            ('social_links', 10),
        ]
        
        total = 0
        for field, weight in fields_to_check:
            value = getattr(self, field, None)
            if value:
                if isinstance(value, dict) and len(value) > 0:
                    total += weight
                elif isinstance(value, str) and value.strip():
                    total += weight
                elif value:  # For file fields
                    total += weight
        
        return min(100, total)
    
    @property
    def location(self):
        """Get formatted location string."""
        parts = [self.city, self.state, self.country]
        return ', '.join(part for part in parts if part)
    
    @property
    def full_address(self):
        """Get full formatted address."""
        parts = [
            self.address_line1,
            self.address_line2,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ', '.join(part for part in parts if part)
    
    def get_social_link(self, platform):
        """Get a specific social media link."""
        return self.social_links.get(platform, '')
    
    def generate_vcard(self):
        """Generate vCard string for contact download."""
        vcard_lines = [
            'BEGIN:VCARD',
            'VERSION:3.0',
            f'FN:{self.full_name}',
        ]
        
        if self.first_name or self.last_name:
            vcard_lines.append(f'N:{self.last_name};{self.first_name};;;')
        
        if self.company:
            vcard_lines.append(f'ORG:{self.company}')
        
        if self.designation:
            vcard_lines.append(f'TITLE:{self.designation}')
        
        if self.phone_primary:
            vcard_lines.append(f'TEL;TYPE=CELL:{self.phone_primary}')
        
        if self.phone_secondary:
            vcard_lines.append(f'TEL;TYPE=WORK:{self.phone_secondary}')
        
        if self.email_public:
            vcard_lines.append(f'EMAIL:{self.email_public}')
        elif self.user.email:
            vcard_lines.append(f'EMAIL:{self.user.email}')
        
        if self.website:
            vcard_lines.append(f'URL:{self.website}')
        
        if self.full_address:
            vcard_lines.append(f'ADR;TYPE=WORK:;;{self.address_line1};{self.city};{self.state};{self.postal_code};{self.country}')
        
        vcard_lines.append('END:VCARD')
        
        return '\n'.join(vcard_lines)


class ProfileContent(models.Model):
    """
    Additional content sections for profile pages.
    Allows users to add custom content blocks.
    """
    
    class ContentType(models.TextChoices):
        TEXT = 'TEXT', _('Text Block')
        LINK = 'LINK', _('Link')
        LINK_GROUP = 'LINK_GROUP', _('Link Group')
        IMAGE = 'IMAGE', _('Image')
        GALLERY = 'GALLERY', _('Image Gallery')
        VIDEO = 'VIDEO', _('Video Embed')
        DOCUMENT = 'DOCUMENT', _('Document')
        HTML = 'HTML', _('Custom HTML')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='content_sections'
    )
    
    # Content configuration
    content_type = models.CharField(max_length=20, choices=ContentType.choices)
    title = models.CharField(max_length=200, blank=True)
    content = models.JSONField(
        default=dict,
        help_text=_('Content data structure varies by content_type')
    )
    
    # Display settings
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('profile content')
        verbose_name_plural = _('profile contents')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.content_type} - {self.title or 'Untitled'}"
