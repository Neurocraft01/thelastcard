"""
Forms for accounts app.
Handles user registration, login, and password management.
"""

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


class LoginForm(forms.Form):
    """User login form."""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email',
            'autocomplete': 'email',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox',
        })
    )


class RegisterForm(forms.ModelForm):
    """User registration form."""
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Create a password',
            'autocomplete': 'new-password',
        }),
        help_text='Minimum 8 characters with letters, numbers, and special characters.'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password',
        })
    )
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox',
        }),
        error_messages={
            'required': 'You must accept the terms and conditions.'
        }
    )
    
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your email',
                'autocomplete': 'email',
            })
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Validate password strength
        validate_password(password)
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError({'password_confirm': 'Passwords do not match.'})
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.email = user.email.lower()
        if commit:
            user.save()
        return user


class ForgotPasswordForm(forms.Form):
    """Password reset request form."""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email',
            'autocomplete': 'email',
        })
    )


class ResetPasswordForm(forms.Form):
    """Password reset form."""
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter new password',
            'autocomplete': 'new-password',
        })
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm new password',
            'autocomplete': 'new-password',
        })
    )
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError({'password_confirm': 'Passwords do not match.'})
        
        return cleaned_data


class ChangePasswordForm(forms.Form):
    """Password change form for logged-in users."""
    
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter current password',
            'autocomplete': 'current-password',
        })
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter new password',
            'autocomplete': 'new-password',
        })
    )
    new_password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm new password',
            'autocomplete': 'new-password',
        })
    )
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if self.user and not self.user.check_password(current_password):
            raise ValidationError('Current password is incorrect.')
        return current_password
    
    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        validate_password(new_password)
        return new_password
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password_confirm = cleaned_data.get('new_password_confirm')
        current_password = cleaned_data.get('current_password')
        
        if new_password and new_password_confirm and new_password != new_password_confirm:
            raise ValidationError({'new_password_confirm': 'Passwords do not match.'})
        
        if new_password and current_password and new_password == current_password:
            raise ValidationError({'new_password': 'New password must be different from current password.'})
        
        return cleaned_data
