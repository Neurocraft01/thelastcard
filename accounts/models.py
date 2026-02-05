"""
Custom User model with role-based access control.
Supports Super Admin, Admin, and User roles.
"""

import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('role', User.Role.SUPER_ADMIN)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model with UUID primary key and role-based access.
    Uses email for authentication instead of username.
    """
    
    class Role(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', _('Super Admin')
        ADMIN = 'ADMIN', _('Admin')
        USER = 'USER', _('User')
    
    # Primary fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        _('username'),
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        help_text=_('Unique username for profile URL. Letters, numbers, and underscores only.')
    )
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    
    # Role
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        db_index=True
    )
    
    # Verification and status
    is_verified = models.BooleanField(
        default=False,
        help_text=_('Designates whether this user has verified their email.')
    )
    verification_token = models.UUIDField(null=True, blank=True)
    verification_token_expires = models.DateTimeField(null=True, blank=True)
    
    # Two-factor authentication
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=32, blank=True)
    two_factor_backup_codes = models.JSONField(default=list, blank=True)
    
    # Password management
    password_changed_at = models.DateTimeField(null=True, blank=True)
    previous_passwords = models.JSONField(default=list, blank=True)  # Store last 5 hashes
    
    # Session and security
    failed_login_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_user_agent = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    @property
    def is_super_admin(self):
        """Check if user is a Super Admin."""
        return self.role == self.Role.SUPER_ADMIN
    
    @property
    def is_admin(self):
        """Check if user is an Admin."""
        return self.role == self.Role.ADMIN
    
    @property
    def is_regular_user(self):
        """Check if user is a regular User."""
        return self.role == self.Role.USER
    
    @property
    def is_account_locked(self):
        """Check if account is currently locked due to failed login attempts."""
        if self.locked_until:
            return timezone.now() < self.locked_until
        return False
    
    def lock_account(self, duration_minutes=30):
        """Lock the account for specified duration."""
        self.locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
        self.save(update_fields=['locked_until'])
    
    def unlock_account(self):
        """Unlock the account and reset failed attempts."""
        self.locked_until = None
        self.failed_login_attempts = 0
        self.save(update_fields=['locked_until', 'failed_login_attempts'])
    
    def increment_failed_login(self):
        """Increment failed login attempts and lock if threshold reached."""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.lock_account()
        self.save(update_fields=['failed_login_attempts'])
    
    def record_successful_login(self, ip_address=None, user_agent=''):
        """Record successful login and reset failed attempts."""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.last_login = timezone.now()
        self.last_login_ip = ip_address
        self.last_login_user_agent = user_agent[:500] if user_agent else ''  # Truncate
        self.save(update_fields=[
            'failed_login_attempts', 'locked_until', 'last_login',
            'last_login_ip', 'last_login_user_agent'
        ])
    
    def generate_verification_token(self):
        """Generate a new email verification token."""
        self.verification_token = uuid.uuid4()
        self.verification_token_expires = timezone.now() + timezone.timedelta(hours=24)
        self.save(update_fields=['verification_token', 'verification_token_expires'])
        return self.verification_token
    
    def verify_email(self, token):
        """Verify the email with the provided token."""
        if self.verification_token and str(self.verification_token) == str(token):
            if self.verification_token_expires and timezone.now() < self.verification_token_expires:
                self.is_verified = True
                self.is_active = True
                self.verification_token = None
                self.verification_token_expires = None
                self.save(update_fields=[
                    'is_verified', 'is_active', 
                    'verification_token', 'verification_token_expires'
                ])
                return True
        return False


class LoginHistory(models.Model):
    """Track login history for security auditing."""
    
    class LoginStatus(models.TextChoices):
        SUCCESS = 'SUCCESS', _('Success')
        FAILED = 'FAILED', _('Failed')
        LOCKED = 'LOCKED', _('Account Locked')
        BLOCKED = 'BLOCKED', _('IP Blocked')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='login_history',
        null=True,
        blank=True
    )
    email_attempted = models.EmailField()
    status = models.CharField(max_length=20, choices=LoginStatus.choices)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('login history')
        verbose_name_plural = _('login histories')
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.email_attempted} - {self.status} - {self.timestamp}"


class AuthSettings(models.Model):
    """Global authentication settings (Singleton)."""
    enable_google_login = models.BooleanField(
        default=True,
        help_text=_("Enable/Disable Google Login button on login/register pages.")
    )

    class Meta:
        verbose_name = _('Authentication Settings')
        verbose_name_plural = _('Authentication Settings')

    def __str__(self):
        return "Authentication Settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # Singleton
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
