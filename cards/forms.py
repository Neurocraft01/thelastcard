"""
Forms for cards app.
Handles NFC card creation and updates.
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import NFCCard


class NFCCardForm(forms.ModelForm):
    """Form for creating and updating NFC cards."""
    
    class Meta:
        model = NFCCard
        fields = ['url_slug', 'theme']
        widgets = {
            'url_slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'your-custom-url',
                'pattern': '[a-z0-9-]+',
            }),
            'theme': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all'
            }),
        }
        labels = {
            'url_slug': 'Custom URL (yourdomain.com/c/your-custom-url)',
            'theme': 'Profile Theme'
        }
        help_texts = {
            'url_slug': 'Choose a unique URL for your NFC card profile. Use only lowercase letters, numbers, and hyphens.',
            'theme': 'Select a theme for your public profile page.'
        }
    
    def clean_url_slug(self):
        """Validate URL slug."""
        slug = self.cleaned_data.get('url_slug')
        if slug:
            slug = slug.lower().strip()
            
            # Check format
            import re
            if not re.match(r'^[a-z0-9-]+$', slug):
                raise ValidationError('URL can only contain lowercase letters, numbers, and hyphens.')
            
            # Check length
            if len(slug) < 3:
                raise ValidationError('URL must be at least 3 characters long.')
            
            if len(slug) > 50:
                raise ValidationError('URL must be 50 characters or less.')
            
            # Check if slug is reserved
            reserved_slugs = [
                'admin', 'api', 'static', 'media', 'login', 'logout', 'register',
                'dashboard', 'profile', 'settings', 'help', 'support', 'contact',
                'about', 'terms', 'privacy', 'pricing', 'features', 'home'
            ]
            if slug in reserved_slugs:
                raise ValidationError(f'The URL "{slug}" is reserved and cannot be used.')
            
            # Check uniqueness (excluding current instance if editing)
            existing = NFCCard.objects.filter(url_slug=slug)
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError('This URL is already taken. Please choose another.')
        
        return slug
