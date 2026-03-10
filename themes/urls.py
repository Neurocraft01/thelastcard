"""
URL patterns for themes app.
"""

from django.urls import path
from . import views

app_name = 'themes'

urlpatterns = [
    path('', views.ThemeListView.as_view(), name='list'),
    path('<slug:slug>/', views.ThemeDetailView.as_view(), name='detail'),
    path('<slug:slug>/preview/', views.ThemePreviewView.as_view(), name='preview'),
]
