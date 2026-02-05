"""
Forms for profiles app.
Handles profile creation and updates.
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import Profile


class ProfileForm(forms.ModelForm):
    """Form for creating and updating user profiles."""
    
    class Meta:
        model = Profile
        fields = [
            'profile_photo', 'full_name', 'designation', 'bio', 'company_name',
            'location', 'phone', 'email', 'website',
            'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country',
            'linkedin_url', 'instagram_url', 'twitter_url', 'facebook_url', 
            'github_url', 'youtube_url', 'whatsapp_number'
        ]
        widgets = {
            'profile_photo': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'John Doe'
            }),
            'designation': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'CEO & Founder'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'A brief description about yourself...',
                'rows': '4',
                'maxlength': '500'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'Your Company Name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'City, Country'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': '+1234567890',
                'type': 'tel'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'contact@example.com'
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'https://yourwebsite.com'
            }),
            'address_line1': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'Street address, building number'
            }),
            'address_line2': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'Apartment, suite, unit (optional)'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'State/Province'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'Postal/ZIP code'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'Country'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'https://linkedin.com/in/yourprofile'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'https://instagram.com/yourhandle'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'https://twitter.com/yourhandle'
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'https://facebook.com/yourprofile'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'https://github.com/yourusername'
            }),
            'youtube_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': 'https://youtube.com/@yourchannel'
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'placeholder': '+1234567890',
                'type': 'tel'
            }),
        }
        labels = {
            'profile_photo': 'Profile Photo',
            'full_name': 'Full Name',
            'designation': 'Job Title/Designation',
            'bio': 'About Me',
            'company_name': 'Company',
            'location': 'Location',
            'phone': 'Phone Number',
            'email': 'Public Email',
            'website': 'Website',
            'address_line1': 'Address Line 1',
            'address_line2': 'Address Line 2',
            'city': 'City',
            'state': 'State/Province',
            'postal_code': 'Postal/ZIP Code',
            'country': 'Country',
            'linkedin_url': 'LinkedIn Profile',
            'instagram_url': 'Instagram',
            'twitter_url': 'Twitter/X',
            'facebook_url': 'Facebook',
            'github_url': 'GitHub',
            'youtube_url': 'YouTube Channel',
            'whatsapp_number': 'WhatsApp Number'
        }
    
    def clean_profile_photo(self):
        """Validate profile photo."""
        photo = self.cleaned_data.get('profile_photo')
        if photo:
            # Only validate if a new file is uploaded
            if hasattr(photo, 'size'):
                # Check file size (max 5MB)
                if photo.size > 5 * 1024 * 1024:
                    raise ValidationError('Profile photo must be smaller than 5MB.')
                
                # Check file type
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
                if hasattr(photo, 'content_type') and photo.content_type not in allowed_types:
                    raise ValidationError('Please upload a valid image file (JPG or PNG).')
        return photo
    
    def clean_phone(self):
        """Validate phone number format."""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove common separators
            cleaned = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if not cleaned.replace('+', '').isdigit():
                raise ValidationError('Phone number must contain only digits, spaces, dashes, and optional + prefix.')
            if len(cleaned.replace('+', '')) < 10:
                raise ValidationError('Phone number must be at least 10 digits.')
        return phone
    
    def clean_whatsapp_number(self):
        """Validate WhatsApp number format."""
        whatsapp = self.cleaned_data.get('whatsapp_number')
        if whatsapp:
            # Remove common separators
            cleaned = whatsapp.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if not cleaned.replace('+', '').isdigit():
                raise ValidationError('WhatsApp number must contain only digits, spaces, dashes, and optional + prefix.')
            if len(cleaned.replace('+', '')) < 10:
                raise ValidationError('WhatsApp number must be at least 10 digits.')
        return whatsapp
    
    def clean_bio(self):
        """Validate bio length."""
        bio = self.cleaned_data.get('bio')
        if bio and len(bio) > 500:
            raise ValidationError('Bio must be 500 characters or less.')
        return bio
    
    def clean_email(self):
        """Validate email format."""
        email = self.cleaned_data.get('email')
        if email:
            # Django's EmailField already validates format
            # Additional custom validation can be added here
            pass
        return email
    
    def clean(self):
        """Cross-field validation."""
        cleaned_data = super().clean()
        
        # Ensure at least one contact method is provided
        phone = cleaned_data.get('phone')
        email = cleaned_data.get('email')
        whatsapp = cleaned_data.get('whatsapp_number')
        
        if not phone and not email and not whatsapp:
            raise ValidationError('Please provide at least one contact method (phone, email, or WhatsApp).')
        
        return cleaned_data
