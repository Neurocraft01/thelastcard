"""
Views for accounts app.
Handles authentication, registration, and dashboards.
"""

import uuid
import io
import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string

from .models import User, LoginHistory
from .forms import (
    LoginForm, RegisterForm, ForgotPasswordForm,
    ResetPasswordForm, ChangePasswordForm
)
from .mixins import SuperAdminRequiredMixin, AdminRequiredMixin, UserRequiredMixin


class LoginView(View):
    """Handle user login."""
    template_name = 'auth/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard_redirect')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # Get client info
            ip_address = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
            
            try:
                user = User.objects.get(email=email)
                
                # Check if account is locked
                if user.is_account_locked:
                    LoginHistory.objects.create(
                        user=user,
                        email_attempted=email,
                        status=LoginHistory.LoginStatus.LOCKED,
                        ip_address=ip_address,
                        user_agent=user_agent
                    )
                    messages.error(request, 'Your account is temporarily locked. Please try again later.')
                    return render(request, self.template_name, {'form': form})
                
                # Authenticate
                authenticated_user = authenticate(request, email=email, password=password)
                
                if authenticated_user is not None:
                    # Successful login
                    user.record_successful_login(ip_address, user_agent)
                    
                    LoginHistory.objects.create(
                        user=user,
                        email_attempted=email,
                        status=LoginHistory.LoginStatus.SUCCESS,
                        ip_address=ip_address,
                        user_agent=user_agent
                    )
                    
                    login(request, authenticated_user, backend='django.contrib.auth.backends.ModelBackend')
                    
                    # Set session expiry
                    if not remember_me:
                        request.session.set_expiry(0)  # Browser close
                    else:
                        request.session.set_expiry(1209600)  # 14 days
                    
                    messages.success(request, f'Welcome back, {user.email}!')
                    return redirect('accounts:dashboard_redirect')
                else:
                    # Failed login
                    user.increment_failed_login()
                    
                    LoginHistory.objects.create(
                        user=user,
                        email_attempted=email,
                        status=LoginHistory.LoginStatus.FAILED,
                        ip_address=ip_address,
                        user_agent=user_agent
                    )
                    
                    messages.error(request, 'Invalid email or password.')
                    
            except User.DoesNotExist:
                # User doesn't exist - log attempt
                LoginHistory.objects.create(
                    email_attempted=email,
                    status=LoginHistory.LoginStatus.FAILED,
                    ip_address=ip_address,
                    user_agent=user_agent
                )
                messages.error(request, 'Invalid email or password.')
        
        return render(request, self.template_name, {'form': form})
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LogoutView(View):
    """Handle user logout."""
    
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('landing:home')
    
    def post(self, request):
        return self.get(request)


class RegisterView(View):
    """Handle user registration."""
    template_name = 'auth/register.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard_redirect')
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Auto-activate user
            user.is_verified = True  # Auto-verify user (skip email verification)
            user.save()
            
            # Create user profile automatically
            from profiles.models import UserProfile
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'full_name': ''}
            )
            
            # Log in the user automatically with the correct backend
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            messages.success(
                request,
                'Welcome! Let\'s set up your profile.'
            )
            return redirect('accounts:onboarding_profile')
        
        return render(request, self.template_name, {'form': form})
    
    def send_verification_email(self, user, token, request):
        """Send email verification link."""
        verification_url = request.build_absolute_uri(
            reverse('accounts:verify_email', kwargs={'token': token})
        )
        
        subject = f'Verify your email - {settings.SITE_NAME}'
        message = f'''
Hello,

Thank you for registering at {settings.SITE_NAME}!

Please click the link below to verify your email address:

{verification_url}

This link will expire in 24 hours.

If you did not create an account, please ignore this email.

Best regards,
The {settings.SITE_NAME} Team
'''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )


class VerifyEmailView(View):
    """Handle email verification."""
    
    def get(self, request, token):
        try:
            user = User.objects.get(verification_token=token)
            if user.verify_email(token):
                messages.success(request, 'Email verified successfully! You can now log in.')
            else:
                messages.error(request, 'Invalid or expired verification link.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid verification link.')
        
        return redirect('accounts:login')


class ResendVerificationView(LoginRequiredMixin, View):
    """Resend verification email."""
    
    def post(self, request):
        user = request.user
        if user.is_verified:
            messages.info(request, 'Your email is already verified.')
        else:
            token = user.generate_verification_token()
            # Send verification email (reuse RegisterView method)
            RegisterView().send_verification_email(user, token, request)
            messages.success(request, 'Verification email sent! Please check your inbox.')
        
        return redirect('accounts:user_settings')


class ForgotPasswordView(View):
    """Handle password reset request."""
    template_name = 'auth/forgot_password.html'
    
    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = user.generate_verification_token()
                self.send_reset_email(user, token, request)
            except User.DoesNotExist:
                pass  # Don't reveal if email exists
            
            messages.success(
                request,
                'If an account with that email exists, we have sent a password reset link.'
            )
            return redirect('accounts:login')
        
        return render(request, self.template_name, {'form': form})
    
    def send_reset_email(self, user, token, request):
        """Send password reset link."""
        reset_url = request.build_absolute_uri(
            reverse('accounts:reset_password', kwargs={'token': token})
        )
        
        subject = f'Reset your password - {settings.SITE_NAME}'
        message = f'''
Hello,

You have requested to reset your password at {settings.SITE_NAME}.

Please click the link below to set a new password:

{reset_url}

This link will expire in 1 hour.

If you did not request a password reset, please ignore this email.

Best regards,
The {settings.SITE_NAME} Team
'''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )


class ResetPasswordView(View):
    """Handle password reset."""
    template_name = 'auth/reset_password.html'
    
    def get(self, request, token):
        try:
            user = User.objects.get(verification_token=token)
            if user.verification_token_expires and timezone.now() > user.verification_token_expires:
                messages.error(request, 'This password reset link has expired.')
                return redirect('accounts:forgot_password')
            
            form = ResetPasswordForm()
            return render(request, self.template_name, {'form': form, 'token': token})
        except User.DoesNotExist:
            messages.error(request, 'Invalid password reset link.')
            return redirect('accounts:forgot_password')
    
    def post(self, request, token):
        try:
            user = User.objects.get(verification_token=token)
            form = ResetPasswordForm(request.POST)
            
            if form.is_valid():
                user.set_password(form.cleaned_data['password'])
                user.verification_token = None
                user.verification_token_expires = None
                user.password_changed_at = timezone.now()
                user.save()
                
                messages.success(request, 'Password reset successful! You can now log in.')
                return redirect('accounts:login')
            
            return render(request, self.template_name, {'form': form, 'token': token})
            
        except User.DoesNotExist:
            messages.error(request, 'Invalid password reset link.')
            return redirect('accounts:forgot_password')


class ChangePasswordView(LoginRequiredMixin, View):
    """Handle password change for logged-in users."""
    template_name = 'auth/change_password.html'
    
    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.password_changed_at = timezone.now()
            request.user.save()
            
            # Re-authenticate to prevent logout
            login(request, request.user, backend='django.contrib.auth.backends.ModelBackend')
            
            messages.success(request, 'Password changed successfully!')
            return redirect('accounts:dashboard_redirect')
        
        return render(request, self.template_name, {'form': form})


class DashboardRedirectView(LoginRequiredMixin, View):
    """Redirect to appropriate dashboard based on user role."""
    
    def get(self, request):
        user = request.user
        
        # Check if regular user needs onboarding (no cards yet)
        if user.role == User.Role.USER and not user.cards.exists():
            return redirect('accounts:onboarding_profile')
        
        if user.is_super_admin:
            return redirect('accounts:superadmin_dashboard')
        elif user.is_admin:
            return redirect('accounts:admin_dashboard')
        else:
            return redirect('accounts:user_dashboard')


# =============================================================================
# SUPER ADMIN DASHBOARD VIEWS
# =============================================================================

class SuperAdminDashboardView(SuperAdminRequiredMixin, TemplateView):
    """Super Admin main dashboard."""
    template_name = 'dashboard/superadmin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get statistics
        from organizations.models import Organization
        from cards.models import NFCCard
        from analytics.models import ProfileAnalytics
        from django.db.models import Count
        
        context['total_users'] = User.objects.count()
        context['total_admins'] = User.objects.filter(role=User.Role.ADMIN).count()
        context['total_organizations'] = Organization.objects.count()
        context['total_cards'] = NFCCard.objects.count()
        context['active_cards'] = NFCCard.objects.filter(status=NFCCard.Status.ACTIVE).count()
        context['pending_cards'] = NFCCard.objects.filter(status=NFCCard.Status.PENDING).count()
        context['total_views'] = ProfileAnalytics.objects.filter(interaction_type='VIEW').count()
        
        # Recent users with profile data
        context['recent_users'] = User.objects.select_related('profile').order_by('-created_at')[:10]
        
        return context


class SuperAdminAdminsView(SuperAdminRequiredMixin, TemplateView):
    """Super Admin - Manage admins."""
    template_name = 'dashboard/superadmin/admins.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admins'] = User.objects.filter(role=User.Role.ADMIN).order_by('-created_at')
        return context





class SuperAdminUsersView(SuperAdminRequiredMixin, TemplateView):
    """Super Admin - View all users."""
    template_name = 'dashboard/superadmin/users.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.select_related('profile').prefetch_related('cards').order_by('-created_at')
        return context


class SuperAdminAnalyticsView(SuperAdminRequiredMixin, TemplateView):
    """Super Admin - Platform analytics."""
    template_name = 'dashboard/superadmin/analytics.html'


class SuperAdminSettingsView(SuperAdminRequiredMixin, TemplateView):
    """Super Admin - Platform settings."""
    template_name = 'dashboard/superadmin/settings.html'


# =============================================================================
# ADMIN DASHBOARD VIEWS
# =============================================================================

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    """Admin main dashboard."""
    template_name = 'dashboard/admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # All users
        context['users'] = User.objects.filter(role=User.Role.USER).select_related('profile').prefetch_related('cards')
        context['user_count'] = context['users'].count()
        
        from cards.models import NFCCard
        context['cards'] = NFCCard.objects.all()
        context['card_count'] = context['cards'].count()
        context['active_cards'] = context['cards'].filter(status=NFCCard.Status.ACTIVE).count()
        
        return context


class AdminUsersView(AdminRequiredMixin, TemplateView):
    """Admin - Manage all users."""
    template_name = 'dashboard/admin/users.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(role=User.Role.USER).select_related('profile').prefetch_related('cards').order_by('-created_at')
        return context


class AdminCardsView(AdminRequiredMixin, TemplateView):
    """Admin - Manage all cards."""
    template_name = 'dashboard/admin/cards.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from cards.models import NFCCard
        context['cards'] = NFCCard.objects.select_related('user', 'user__profile', 'theme').order_by('-created_at')
        return context


class AdminAnalyticsView(AdminRequiredMixin, TemplateView):
    """Admin - System analytics."""
    template_name = 'dashboard/admin/analytics.html'


class AdminSettingsView(AdminRequiredMixin, TemplateView):
    """Admin - Admin settings."""
    template_name = 'dashboard/admin/settings.html'


class AdminCardDetailView(AdminRequiredMixin, TemplateView):
    """Admin - View card details for printing."""
    template_name = 'dashboard/admin/card_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from cards.models import NFCCard
        
        card_id = self.kwargs.get('card_id')
        card = get_object_or_404(NFCCard, id=card_id)
        
        context['card'] = card
        context['user'] = card.user
        if card.user:
            try:
                context['profile'] = card.user.profile
            except:
                context['profile'] = None
        
        return context


class AdminUserDetailView(AdminRequiredMixin, TemplateView):
    """Admin - View user details with all their cards."""
    template_name = 'dashboard/admin/user_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from cards.models import NFCCard
        from analytics.models import ProfileAnalytics
        from django.db.models import Count
        
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        
        context['member'] = user
        context['cards'] = user.cards.all()
        context['active_cards_count'] = user.cards.filter(status=NFCCard.Status.ACTIVE).count()
        
        # Get total views for user's cards
        context['total_views'] = ProfileAnalytics.objects.filter(
            card__in=user.cards.all(),
            interaction_type='VIEW'
        ).count()
        
        try:
            context['profile'] = user.profile
        except:
            context['profile'] = None
        
        return context


class AdminExportCardView(AdminRequiredMixin, View):
    """Export card data for printing."""
    
    def get(self, request, card_id):
        from cards.models import NFCCard
        from reportlab.lib.pagesizes import LETTER, inch
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        
        card = get_object_or_404(NFCCard, id=card_id)
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=LETTER, topMargin=0.5*inch, bottomMargin=0.5*inch)
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=24,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.HexColor('#D4AF37')
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            textColor=colors.HexColor('#333333')
        )
        
        content = []
        
        # Title
        content.append(Paragraph("Card Printing Data", title_style))
        content.append(Spacer(1, 20))
        
        # Card Info
        content.append(Paragraph("Card Information", heading_style))
        
        card_data = [
            ['Card UID', card.card_uid],
            ['URL Slug', card.url_slug],
            ['Status', card.get_status_display()],
            ['Created', card.created_at.strftime('%Y-%m-%d %H:%M')],
            ['Public URL', f"{settings.SITE_URL}/{card.url_slug}"],
        ]
        
        t = Table(card_data, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f7f7f7')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dddddd')),
        ]))
        content.append(t)
        content.append(Spacer(1, 20))
        
        # User Info
        if card.user:
            content.append(Paragraph("User Information", heading_style))
            
            user = card.user
            profile = getattr(user, 'profile', None)
            
            user_data = [
                ['Email', user.email],
                ['Name', profile.full_name if profile else '-'],
                ['Company', profile.company if profile else '-'],
                ['Designation', profile.designation if profile else '-'],
                ['Phone', profile.phone_primary if profile else '-'],
                ['Website', profile.website if profile else '-'],
                ['Location', profile.location if profile else '-'],
            ]
            
            t2 = Table(user_data, colWidths=[2*inch, 4*inch])
            t2.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f7f7f7')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dddddd')),
            ]))
            content.append(t2)
            content.append(Spacer(1, 20))
        
        # QR Code
        content.append(Paragraph("QR Code for Printing", heading_style))
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"{settings.SITE_URL}/{card.url_slug}")
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="#000000", back_color="white")
        
        # Save QR to buffer
        qr_buffer = io.BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        
        # Add QR to PDF
        qr_image = Image(qr_buffer, width=2*inch, height=2*inch)
        content.append(qr_image)
        
        doc.build(content)
        
        # Get the value of the buffer
        pdf = buffer.getvalue()
        buffer.close()
        
        # Return response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="card_{card.url_slug}.pdf"'
        response.write(pdf)
        
        return response


class AdminExportAllCardsView(AdminRequiredMixin, View):
    """Export all cards data for printing."""
    
    def get(self, request):
        from cards.models import NFCCard
        import csv
        
        user = request.user
        
        # Get organization cards
        if user.organization:
            org_users = user.organization.members.all()
            cards = NFCCard.objects.filter(user__in=org_users).select_related('user')
        else:
            cards = NFCCard.objects.none()
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="cards_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Card UID', 'URL Slug', 'Status', 'Public URL',
            'User Email', 'Full Name', 'Company', 'Designation',
            'Phone', 'Website', 'Created Date'
        ])
        
        for card in cards:
            profile = getattr(card.user, 'profile', None) if card.user else None
            writer.writerow([
                card.card_uid,
                card.url_slug,
                card.get_status_display(),
                f"{settings.SITE_URL}/{card.url_slug}",
                card.user.email if card.user else '',
                profile.full_name if profile else '',
                profile.company if profile else '',
                profile.designation if profile else '',
                profile.phone_primary if profile else '',
                profile.website if profile else '',
                card.created_at.strftime('%Y-%m-%d %H:%M'),
            ])
        
        return response


class AdminPrintCardsView(AdminRequiredMixin, TemplateView):
    """Admin - Print multiple cards."""
    template_name = 'dashboard/admin/print_cards.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from cards.models import NFCCard
        
        user = self.request.user
        
        # Get selected card IDs from query params
        card_ids = self.request.GET.getlist('cards')
        
        if card_ids and user.organization:
            org_users = user.organization.members.all()
            context['cards'] = NFCCard.objects.filter(
                id__in=card_ids,
                user__in=org_users
            ).select_related('user')
        else:
            context['cards'] = []
        
        return context


# =============================================================================
# USER DASHBOARD VIEWS
# =============================================================================

class UserDashboardView(UserRequiredMixin, TemplateView):
    """Regular user dashboard."""
    template_name = 'dashboard/user/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get user's cards
        context['cards'] = user.cards.all()
        context['card_count'] = context['cards'].count()
        
        # Get profile completion
        if hasattr(user, 'profile'):
            context['profile'] = user.profile
            context['completion'] = user.profile.completion_percentage
        else:
            context['completion'] = 0
        
        # Get analytics summary
        from analytics.models import UserAnalyticsSummary
        try:
            context['analytics'] = UserAnalyticsSummary.objects.get(user=user)
        except UserAnalyticsSummary.DoesNotExist:
            context['analytics'] = None
        
        return context


from django.views.generic import UpdateView
from django.urls import reverse_lazy
from profiles.models import UserProfile

class UserProfileView(UserRequiredMixin, UpdateView):
    """User - Edit profile."""
    model = UserProfile
    template_name = 'dashboard/user/profile.html'
    fields = ['first_name', 'last_name', 'bio', 'company', 'designation', 'phone_primary', 'email_public', 'website', 'city', 'profile_photo']
    success_url = reverse_lazy('accounts:user_profile')
    
    def get_object(self, queryset=None):
        profile, created = UserProfile.objects.get_or_create(
            user=self.request.user,
            defaults={'full_name': self.request.user.email.split('@')[0]}
        )
        return profile

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


class UserCardView(UserRequiredMixin, TemplateView):
    """User - Manage NFC card."""
    template_name = 'dashboard/user/card.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = self.request.user.cards.all()
        
        from themes.models import Theme
        context['themes'] = Theme.objects.filter(is_active=True)
        
        return context


class UserAnalyticsView(UserRequiredMixin, TemplateView):
    """User - View card analytics."""
    template_name = 'dashboard/user/analytics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        from analytics.models import DailyAnalyticsSummary
        from django.db.models import Sum
        from datetime import timedelta
        
        user = self.request.user
        cards = user.cards.all()
        
        # Get last 30 days analytics
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        context['daily_stats'] = DailyAnalyticsSummary.objects.filter(
            card__in=cards,
            date__gte=thirty_days_ago.date()
        ).order_by('date')
        
        # Aggregate totals
        totals = context['daily_stats'].aggregate(
            total_views=Sum('total_views'),
            total_unique=Sum('unique_views'),
            total_saves=Sum('contact_saves')
        )
        context['totals'] = totals
        
        return context


class UserSettingsView(UserRequiredMixin, TemplateView):
    """User - Account settings."""
    template_name = 'dashboard/user/settings.html'


# =============================================================================
# SUPER ADMIN CRUD OPERATIONS
# =============================================================================

class SuperAdminCreateAdminView(SuperAdminRequiredMixin, View):
    """Super Admin - Create new Admin."""
    
    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password', 'Admin@123')  # Default password
        
        try:
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, f'User with email {email} already exists.')
                return redirect('accounts:superadmin_admins')
            
            # Create Admin user
            admin = User.objects.create_user(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=User.Role.ADMIN,
                is_verified=True,
                is_active=True
            )
            
            # Create profile
            from profiles.models import UserProfile
            UserProfile.objects.create(
                user=admin,
                first_name=first_name,
                last_name=last_name
            )
            
            messages.success(request, f'Admin {email} created successfully. Default password: {password}')
            return redirect('accounts:superadmin_admins')
            
        except Exception as e:
            messages.error(request, f'Error creating admin: {str(e)}')
            return redirect('accounts:superadmin_admins')


class SuperAdminUpdateAdminView(SuperAdminRequiredMixin, View):
    """Super Admin - Update Admin details."""
    
    def post(self, request, user_id):
        admin = get_object_or_404(User, id=user_id, role=User.Role.ADMIN)
        
        admin.first_name = request.POST.get('first_name', admin.first_name)
        admin.last_name = request.POST.get('last_name', admin.last_name)
        admin.email = request.POST.get('email', admin.email)
        admin.is_active = request.POST.get('is_active') == 'on'
        admin.save()
        
        messages.success(request, f'Admin {admin.email} updated successfully.')
        return redirect('accounts:superadmin_admins')


class SuperAdminDeleteAdminView(SuperAdminRequiredMixin, View):
    """Super Admin - Delete Admin."""
    
    def post(self, request, user_id):
        admin = get_object_or_404(User, id=user_id, role=User.Role.ADMIN)
        email = admin.email
        admin.delete()
        messages.success(request, f'Admin {email} deleted successfully.')
        return redirect('accounts:superadmin_admins')


class AdminCreateUserView(AdminRequiredMixin, View):
    """Admin - Create new User."""
    
    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password', 'User@123')  # Default password
        
        try:
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, f'User with email {email} already exists.')
                return redirect('accounts:admin_users')
            
            # Create User
            user = User.objects.create_user(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=User.Role.USER,
                is_verified=True,
                is_active=True
            )
            
            # Create profile
            from profiles.models import UserProfile
            UserProfile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name
            )
            
            messages.success(request, f'User {email} created successfully. Default password: {password}')
            return redirect('accounts:admin_users')
            
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            return redirect('accounts:admin_users')


class AdminUpdateUserView(AdminRequiredMixin, View):
    """Admin - Update User details."""
    
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id, role=User.Role.USER)
        
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.is_active = request.POST.get('is_active') == 'on'
        user.save()
        
        # Update profile if exists
        try:
            profile = user.profile
            profile.first_name = user.first_name
            profile.last_name = user.last_name
            profile.save()
        except:
            pass
        
        messages.success(request, f'User {user.email} updated successfully.')
        return redirect('accounts:admin_user_detail', user_id=user_id)


class AdminDeleteUserView(AdminRequiredMixin, View):
    """Admin - Delete User."""
    
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id, role=User.Role.USER)
        
        email = user.email
        user.delete()
        messages.success(request, f'User {email} deleted successfully.')
        return redirect('accounts:admin_users')


class AdminResetUserPasswordView(AdminRequiredMixin, View):
    """Admin - Reset User password."""
    
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id, role=User.Role.USER)
        
        new_password = request.POST.get('new_password', 'User@123')
        user.set_password(new_password)
        user.save()
        
        messages.success(request, f'Password reset for {user.email}. New password: {new_password}')
        return redirect('accounts:admin_user_detail', user_id=user_id)


class AdminCreateCardView(AdminRequiredMixin, View):
    """Admin - Create new Card for user."""
    
    def post(self, request):
        from cards.models import NFCCard
        from themes.models import Theme
        
        user_id = request.POST.get('user_id')
        card_name = request.POST.get('card_name', 'Digital Business Card')
        theme_id = request.POST.get('theme_id')
        
        try:
            user = get_object_or_404(User, id=user_id, role=User.Role.USER)
            
            # Get theme
            theme = Theme.objects.filter(id=theme_id).first() if theme_id else Theme.objects.filter(is_default=True).first()
            
            # Create card
            card = NFCCard.objects.create(
                user=user,
                card_name=card_name,
                theme=theme,
                status=NFCCard.Status.ACTIVE
            )
            
            messages.success(request, f'Card "{card_name}" created for {user.email}.')
            return redirect('accounts:admin_user_detail', user_id=user_id)
            
        except Exception as e:
            messages.error(request, f'Error creating card: {str(e)}')
            return redirect('accounts:admin_cards')


class AdminUpdateCardView(AdminRequiredMixin, View):
    """Admin - Update Card details."""
    
    def post(self, request, card_id):
        from cards.models import NFCCard
        card = get_object_or_404(NFCCard, id=card_id)
        
        card.card_name = request.POST.get('card_name', card.card_name)
        card.status = request.POST.get('status', card.status)
        card.save()
        
        messages.success(request, f'Card "{card.card_name}" updated successfully.')
        return redirect('accounts:admin_card_detail', card_id=card_id)


class AdminDeleteCardView(AdminRequiredMixin, View):
    """Admin - Delete Card."""
    
    def post(self, request, card_id):
        from cards.models import NFCCard
        card = get_object_or_404(NFCCard, id=card_id)
        
        card_name = card.card_name
        user_id = card.user.id
        card.delete()
        messages.success(request, f'Card "{card_name}" deleted successfully.')
        return redirect('accounts:admin_user_detail', user_id=user_id)


# =============================================================================
# ONBOARDING VIEWS
# =============================================================================

class OnboardingRequiredMixin(LoginRequiredMixin):
    """Mixin to ensure user hasn't completed onboarding."""
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if user has completed onboarding (has at least one card)
            if request.user.cards.exists():
                return redirect('accounts:dashboard_redirect')
        return super().dispatch(request, *args, **kwargs)


class ProfileSetupView(LoginRequiredMixin, View):
    """Step 1: Profile information setup after registration."""
    template_name = 'onboarding/profile_setup.html'
    
    def get(self, request):
        # If user already has cards, redirect to dashboard
        if request.user.cards.exists():
            return redirect('accounts:dashboard_redirect')
        
        profile, created = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={'full_name': ''}
        )
        return render(request, self.template_name, {'profile': profile})
    
    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={'full_name': ''}
        )
        
        # Update profile with form data
        profile.full_name = request.POST.get('full_name', '').strip()
        profile.first_name = request.POST.get('first_name', '').strip()
        profile.last_name = request.POST.get('last_name', '').strip()
        profile.company = request.POST.get('company', '').strip()
        profile.designation = request.POST.get('designation', '').strip()
        profile.phone_primary = request.POST.get('phone', '').strip()
        profile.email_public = request.POST.get('email_public', '').strip() or request.user.email
        profile.website = request.POST.get('website', '').strip()
        profile.bio = request.POST.get('bio', '').strip()
        
        # Handle profile photo
        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']
        
        profile.save()
        
        messages.success(request, 'Profile saved! Now choose your theme.')
        return redirect('accounts:onboarding_theme')


class ThemeSelectionView(LoginRequiredMixin, View):
    """Step 2: Theme selection for the profile."""
    template_name = 'onboarding/theme_selection.html'
    
    def get(self, request):
        # If user already has cards, redirect to dashboard
        if request.user.cards.exists():
            return redirect('accounts:dashboard_redirect')
        
        from themes.models import Theme
        # Get 3 featured themes for selection
        themes = Theme.objects.filter(
            is_active=True, 
            is_public=True,
            theme_type='SYSTEM'
        ).order_by('?')[:3]  # Random 3 themes
        
        # If not enough themes, get all available
        if themes.count() < 3:
            themes = Theme.objects.filter(is_active=True, is_public=True)[:3]
        
        return render(request, self.template_name, {'themes': themes})
    
    def post(self, request):
        from themes.models import Theme
        from cards.models import NFCCard
        
        theme_id = request.POST.get('theme_id')
        
        # Get or create default theme
        theme = None
        if theme_id:
            try:
                theme = Theme.objects.get(id=theme_id)
            except Theme.DoesNotExist:
                pass
        
        # Create the user's card (without NFC UID - it's optional now)
        card = NFCCard.objects.create(
            user=request.user,
            created_by=request.user,
            theme=theme,
            status=NFCCard.Status.ACTIVE,
            activation_date=timezone.now()
        )
        
        # Generate QR code for the card
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f"{settings.SITE_URL}/{card.url_slug}")
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="#000000", back_color="white")
            
            qr_buffer = io.BytesIO()
            qr_img.save(qr_buffer, format='PNG')
            qr_buffer.seek(0)
            
            from django.core.files.base import ContentFile
            card.qr_code.save(f'qr_{card.url_slug}.png', ContentFile(qr_buffer.getvalue()), save=True)
        except Exception as e:
            pass  # QR generation failed, but card is still created
        
        messages.success(request, 'Your profile is ready!')
        return redirect('accounts:onboarding_complete')


class OnboardingCompleteView(LoginRequiredMixin, TemplateView):
    """Step 3: Onboarding complete - show the profile URL."""
    template_name = 'onboarding/complete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user's latest card
        card = self.request.user.cards.order_by('-created_at').first()
        context['card'] = card
        
        if card:
            context['profile_url'] = f"{settings.SITE_URL}/{card.url_slug}"
        
        try:
            context['profile'] = self.request.user.profile
        except:
            context['profile'] = None
        
        return context
