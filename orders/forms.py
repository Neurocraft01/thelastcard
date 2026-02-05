from django import forms
from django.core.exceptions import ValidationError
from .models import CardOrder


class OrderForm(forms.ModelForm):
    """Form for creating NFC card orders."""
    
    class Meta:
        model = CardOrder
        fields = ['card_type', 'quantity', 'custom_design', 'custom_text', 'shipping_address', 'notes']
        widgets = {
            'card_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all',
                'min': '1',
                'max': '100',
                'value': '1'
            }),
            'custom_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all placeholder:text-slate-400',
                'placeholder': 'e.g. John Doe - CEO'
            }),
            'shipping_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all placeholder:text-slate-400',
                'rows': '4',
                'placeholder': 'Full shipping address including name, street, city, state, pincode...'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-700 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all placeholder:text-slate-400',
                'rows': '3',
                'placeholder': 'Any specific instructions or special requests...'
            }),
            'custom_design': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            }),
        }
        labels = {
            'card_type': 'Card Material',
            'quantity': 'Quantity',
            'custom_design': 'Upload Logo/Design',
            'custom_text': 'Name/Text on Card',
            'shipping_address': 'Delivery Address',
            'notes': 'Order Notes'
        }
    
    def clean_quantity(self):
        """Validate quantity is within acceptable range."""
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise ValidationError('Quantity must be at least 1.')
        if quantity > 100:
            raise ValidationError('Maximum order quantity is 100 cards. For larger orders, please contact support.')
        return quantity
    
    def clean_custom_design(self):
        """Validate custom design file."""
        design = self.cleaned_data.get('custom_design')
        if design:
            # Check file size (max 5MB)
            if design.size > 5 * 1024 * 1024:
                raise ValidationError('Design file must be smaller than 5MB.')
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/svg+xml']
            if hasattr(design, 'content_type') and design.content_type not in allowed_types:
                raise ValidationError('Please upload a valid image file (JPG, PNG, or SVG).')
        
        return design
    
    def clean_shipping_address(self):
        """Validate shipping address is not empty."""
        address = self.cleaned_data.get('shipping_address')
        if not address or len(address.strip()) < 20:
            raise ValidationError('Please provide a complete shipping address with at least 20 characters.')
        return address.strip()
