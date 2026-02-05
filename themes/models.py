"""
Theme model for NFC card customization.
Provides pre-built and custom themes for profile pages.
"""

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Theme(models.Model):
    """
    Theme templates for NFC card profiles.
    Includes both system themes and custom user themes.
    """
    
    class ThemeType(models.TextChoices):
        SYSTEM = 'SYSTEM', _('System Theme')
        CUSTOM = 'CUSTOM', _('Custom Theme')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Theme type
    theme_type = models.CharField(
        max_length=20,
        choices=ThemeType.choices,
        default=ThemeType.SYSTEM
    )
    
    # Preview
    preview_image = models.ImageField(
        upload_to='themes/previews/',
        blank=True,
        null=True
    )
    
    # Colors
    primary_color = models.CharField(max_length=7, default='#6366f1')
    secondary_color = models.CharField(max_length=7, default='#4f46e5')
    background_color = models.CharField(max_length=7, default='#ffffff')
    text_color = models.CharField(max_length=7, default='#0f172a')
    accent_color = models.CharField(max_length=7, default='#818cf8')
    
    # Background settings
    background_type = models.CharField(
        max_length=20,
        choices=[
            ('SOLID', 'Solid Color'),
            ('GRADIENT', 'Gradient'),
            ('IMAGE', 'Image'),
        ],
        default='SOLID'
    )
    background_gradient = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('CSS gradient value, e.g., "linear-gradient(135deg, #6366f1, #4f46e5)"')
    )
    background_image = models.ImageField(
        upload_to='themes/backgrounds/',
        blank=True,
        null=True
    )
    
    # Typography
    font_family_heading = models.CharField(
        max_length=100,
        default='Plus Jakarta Sans'
    )
    font_family_body = models.CharField(
        max_length=100,
        default='Inter'
    )
    
    # Layout
    border_radius = models.CharField(max_length=20, default='0.75rem')
    card_shadow = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    
    # Custom CSS (for advanced customization)
    custom_css = models.TextField(blank=True)
    
    # Ownership
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_themes'
    )
    
    # Premium and visibility
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('theme')
        verbose_name_plural = _('themes')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_css_variables(self):
        """Generate CSS custom properties for this theme."""
        css_vars = {
            '--theme-primary': self.primary_color,
            '--theme-secondary': self.secondary_color,
            '--theme-background': self.background_color,
            '--theme-text': self.text_color,
            '--theme-accent': self.accent_color,
            '--theme-font-heading': f"'{self.font_family_heading}', sans-serif",
            '--theme-font-body': f"'{self.font_family_body}', sans-serif",
            '--theme-radius': self.border_radius,
        }
        
        if self.background_type == 'GRADIENT' and self.background_gradient:
            css_vars['--theme-bg-gradient'] = self.background_gradient
        
        return css_vars
    
    def generate_style_tag(self):
        """Generate a complete <style> tag with theme variables."""
        css_vars = self.get_css_variables()
        vars_str = '\n'.join(f'  {k}: {v};' for k, v in css_vars.items())
        
        style = f"""<style>
:root {{
{vars_str}
}}
{self.custom_css}
</style>"""
        return style


# Create default system themes
DEFAULT_THEMES = [
    {
        'name': 'Professional',
        'slug': 'professional',
        'description': 'Clean, professional theme with indigo accents.',
        'primary_color': '#6366f1',
        'secondary_color': '#4f46e5',
        'background_color': '#ffffff',
        'text_color': '#0f172a',
    },
    {
        'name': 'Dark Mode',
        'slug': 'dark-mode',
        'description': 'Sleek dark theme with cyan accents.',
        'primary_color': '#22d3ee',
        'secondary_color': '#06b6d4',
        'background_color': '#0f172a',
        'text_color': '#f8fafc',
        'dark_mode': True,
    },
    {
        'name': 'Gradient',
        'slug': 'gradient',
        'description': 'Modern gradient background with glass-morphism.',
        'primary_color': '#8b5cf6',
        'secondary_color': '#6366f1',
        'background_type': 'GRADIENT',
        'background_gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    },
    {
        'name': 'Minimal',
        'slug': 'minimal',
        'description': 'Ultra-clean minimal design.',
        'primary_color': '#000000',
        'secondary_color': '#374151',
        'background_color': '#f9fafb',
        'text_color': '#111827',
        'card_shadow': False,
    },
    {
        'name': 'Corporate',
        'slug': 'corporate',
        'description': 'Professional corporate blue theme.',
        'primary_color': '#1d4ed8',
        'secondary_color': '#1e40af',
        'background_color': '#f8fafc',
        'text_color': '#1e293b',
    },
    {
        'name': 'Creative',
        'slug': 'creative',
        'description': 'Bold and colorful creative theme.',
        'primary_color': '#ec4899',
        'secondary_color': '#db2777',
        'background_color': '#fdf2f8',
        'text_color': '#831843',
    },
    {
        'name': 'Nature',
        'slug': 'nature',
        'description': 'Earth-toned nature-inspired theme.',
        'primary_color': '#059669',
        'secondary_color': '#047857',
        'background_color': '#f0fdf4',
        'text_color': '#14532d',
    },
    {
        'name': 'Sunset',
        'slug': 'sunset',
        'description': 'Warm sunset gradient theme.',
        'primary_color': '#f97316',
        'secondary_color': '#ea580c',
        'background_type': 'GRADIENT',
        'background_gradient': 'linear-gradient(135deg, #ff6b6b 0%, #feca57 50%, #ff9ff3 100%)',
    },
    {
        'name': 'Ocean',
        'slug': 'ocean',
        'description': 'Deep ocean blue theme.',
        'primary_color': '#0284c7',
        'secondary_color': '#0369a1',
        'background_type': 'GRADIENT',
        'background_gradient': 'linear-gradient(135deg, #667eea 0%, #00d4ff 100%)',
    },
    {
        'name': 'Elegant',
        'slug': 'elegant',
        'description': 'Sophisticated elegant theme with gold accents.',
        'primary_color': '#d97706',
        'secondary_color': '#b45309',
        'background_color': '#1c1917',
        'text_color': '#fafaf9',
        'dark_mode': True,
    },
]
