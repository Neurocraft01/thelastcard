"""
URL configuration for NFC Platform project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from profiles.views import PublicProfileView, DownloadVCardView, QRCodeView, MobilePreviewView
from .views import health_check

urlpatterns = [
    # Health check endpoint for monitoring
    path('healthz', health_check, name='health_check'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),  # Allauth URLs
    
    # Landing pages (home, about, pricing, etc.)
    path('', include('landing.urls', namespace='landing')),
    
    # Profile pages (public NFC card profiles)  
    path('p/', include('profiles.urls', namespace='profiles')),
    # Alias /u/ for username-based URLs
    path('u/<slug:slug>/', PublicProfileView.as_view(), name='public_profile_u'),
    path('u/<slug:slug>/vcard/', DownloadVCardView.as_view(), name='download_vcard_u'),
    path('u/<slug:slug>/qr/', QRCodeView.as_view(), name='qr_code_u'),
    path('u/<slug:slug>/mobile/', MobilePreviewView.as_view(), name='mobile_preview_u'),
    
    # Cards management
    path('cards/', include('cards.urls', namespace='cards')),
    
    # Orders (Physical PVC Cards)
    path('orders/', include('orders.urls', namespace='orders')),
    
    # Organizations
    path('organizations/', include('organizations.urls', namespace='organizations')),
    
    # Analytics
    path('analytics/', include('analytics.urls', namespace='analytics')),
    
    # Themes
    path('themes/', include('themes.urls', namespace='themes')),
    
    # API endpoints
    path('api/', include('api.urls', namespace='api')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Custom error handlers
handler404 = 'nfc_platform.views.handler404'
handler500 = 'nfc_platform.views.handler500'
