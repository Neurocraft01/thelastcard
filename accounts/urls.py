"""
URL patterns for accounts app.
Handles authentication and user management.
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Email verification
    path('verify-email/<uuid:token>/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('resend-verification/', views.ResendVerificationView.as_view(), name='resend_verification'),
    
    # Password management
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uuid:token>/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    
    # Onboarding flow
    path('onboarding/profile/', views.ProfileSetupView.as_view(), name='onboarding_profile'),
    path('onboarding/theme/', views.ThemeSelectionView.as_view(), name='onboarding_theme'),
    path('onboarding/complete/', views.OnboardingCompleteView.as_view(), name='onboarding_complete'),
    
    # Dashboard routes
    path('dashboard/', views.DashboardRedirectView.as_view(), name='dashboard_redirect'),
    
    # Super Admin Dashboard
    path('superadmin/dashboard/', views.SuperAdminDashboardView.as_view(), name='superadmin_dashboard'),
    path('superadmin/admins/', views.SuperAdminAdminsView.as_view(), name='superadmin_admins'),
    path('superadmin/admins/create/', views.SuperAdminCreateAdminView.as_view(), name='superadmin_create_admin'),
    path('superadmin/admins/<uuid:user_id>/update/', views.SuperAdminUpdateAdminView.as_view(), name='superadmin_update_admin'),
    path('superadmin/admins/<uuid:user_id>/delete/', views.SuperAdminDeleteAdminView.as_view(), name='superadmin_delete_admin'),
    path('superadmin/users/', views.SuperAdminUsersView.as_view(), name='superadmin_users'),
    path('superadmin/analytics/', views.SuperAdminAnalyticsView.as_view(), name='superadmin_analytics'),
    path('superadmin/settings/', views.SuperAdminSettingsView.as_view(), name='superadmin_settings'),
    
    # Admin Dashboard
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin-dashboard/users/', views.AdminUsersView.as_view(), name='admin_users'),
    path('admin-dashboard/users/create/', views.AdminCreateUserView.as_view(), name='admin_create_user'),
    path('admin-dashboard/users/<uuid:user_id>/', views.AdminUserDetailView.as_view(), name='admin_user_detail'),
    path('admin-dashboard/users/<uuid:user_id>/update/', views.AdminUpdateUserView.as_view(), name='admin_update_user'),
    path('admin-dashboard/users/<uuid:user_id>/delete/', views.AdminDeleteUserView.as_view(), name='admin_delete_user'),
    path('admin-dashboard/users/<uuid:user_id>/reset-password/', views.AdminResetUserPasswordView.as_view(), name='admin_reset_password'),
    path('admin-dashboard/cards/', views.AdminCardsView.as_view(), name='admin_cards'),
    path('admin-dashboard/cards/create/', views.AdminCreateCardView.as_view(), name='admin_create_card'),
    path('admin-dashboard/cards/<uuid:card_id>/', views.AdminCardDetailView.as_view(), name='admin_card_detail'),
    path('admin-dashboard/cards/<uuid:card_id>/update/', views.AdminUpdateCardView.as_view(), name='admin_update_card'),
    path('admin-dashboard/cards/<uuid:card_id>/delete/', views.AdminDeleteCardView.as_view(), name='admin_delete_card'),
    path('admin-dashboard/cards/<uuid:card_id>/export/', views.AdminExportCardView.as_view(), name='admin_export_card'),
    path('admin-dashboard/cards/export-all/', views.AdminExportAllCardsView.as_view(), name='admin_export_all_cards'),
    path('admin-dashboard/cards/print/', views.AdminPrintCardsView.as_view(), name='admin_print_cards'),
    path('admin-dashboard/analytics/', views.AdminAnalyticsView.as_view(), name='admin_analytics'),
    path('admin-dashboard/settings/', views.AdminSettingsView.as_view(), name='admin_settings'),
    
    # User Dashboard
    path('user/dashboard/', views.UserDashboardView.as_view(), name='user_dashboard'),
    path('user/profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('user/card/', views.UserCardView.as_view(), name='user_card'),
    path('user/analytics/', views.UserAnalyticsView.as_view(), name='user_analytics'),
    path('user/settings/', views.UserSettingsView.as_view(), name='user_settings'),
]
