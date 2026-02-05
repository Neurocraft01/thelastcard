"""
URL patterns for API endpoints.
"""

from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Profile API
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateAPIView.as_view(), name='profile_update'),
    
    # Card API
    path('cards/', views.CardListAPIView.as_view(), name='cards'),
    path('cards/<uuid:pk>/', views.CardDetailAPIView.as_view(), name='card_detail'),
    
    # Analytics API
    path('analytics/track/', views.TrackEventAPIView.as_view(), name='track'),
    path('analytics/summary/', views.AnalyticsSummaryAPIView.as_view(), name='analytics_summary'),
    
    # Themes API
    path('themes/', views.ThemeListAPIView.as_view(), name='themes'),
]
