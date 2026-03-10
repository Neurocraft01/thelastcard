"""
Admin configuration for accounts app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, LoginHistory, AuthSettings
from profiles.models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Information'
    fk_name = 'user'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model."""
    
    list_display = (
        'email', 'full_name', 'role',
        'is_verified', 'is_active', 'created_at'
    )
    list_filter = ('role', 'is_verified', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    inlines = (UserProfileInline,)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Role'), {'fields': ('role',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Security'), {
            'fields': ('two_factor_enabled', 'failed_login_attempts', 'locked_until'),
            'classes': ('collapse',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'created_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
    )
    
    readonly_fields = ('created_at', 'last_login')
    
    def full_name(self, obj):
        """Display full name from profile if available."""
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.full_name
        return f"{obj.first_name} {obj.last_name}".strip() or '-'
    full_name.short_description = 'Name'


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    """Admin for login history tracking."""
    
    list_display = ('email_attempted', 'status', 'ip_address', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('email_attempted', 'ip_address')
    readonly_fields = ('id', 'user', 'email_attempted', 'status', 'ip_address', 'user_agent', 'location', 'timestamp')
    ordering = ('-timestamp',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(AuthSettings)
class AuthSettingsAdmin(admin.ModelAdmin):
    """Admin for global auth settings."""
    def has_add_permission(self, request):
        # Allow adding only if no instance exists
        return not AuthSettings.objects.exists()
