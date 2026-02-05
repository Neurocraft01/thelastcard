"""
URL patterns for organizations app.
"""

from django.urls import path
from . import views

app_name = 'organizations'

urlpatterns = [
    path('', views.OrganizationListView.as_view(), name='list'),
    path('create/', views.OrganizationCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.OrganizationDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', views.OrganizationEditView.as_view(), name='edit'),
]
