"""
URL patterns for profiles app.
"""

from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('<slug:slug>/', views.PublicProfileView.as_view(), name='public_profile'),
    path('<slug:slug>/vcard/', views.DownloadVCardView.as_view(), name='download_vcard'),
    path('<slug:slug>/qr/', views.QRCodeView.as_view(), name='qr_code'),
    path('<slug:slug>/mobile/', views.MobilePreviewView.as_view(), name='mobile_preview'),
]
