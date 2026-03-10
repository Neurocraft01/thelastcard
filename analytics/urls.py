"""
URL patterns for analytics app.
"""

from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('track/', views.TrackInteractionView.as_view(), name='track'),
    path('dashboard/', views.AnalyticsDashboardView.as_view(), name='dashboard'),
    path('card/<uuid:card_id>/', views.CardAnalyticsView.as_view(), name='card'),
    path('export/', views.ExportAnalyticsView.as_view(), name='export'),
]
