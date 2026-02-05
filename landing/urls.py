"""
URL patterns for landing pages.
"""

from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('features/', views.FeaturesView.as_view(), name='features'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
]
