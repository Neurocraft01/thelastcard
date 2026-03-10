"""
URL patterns for cards app.
"""

from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('', views.CardListView.as_view(), name='list'),
    path('create/', views.CardCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.CardDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', views.CardEditView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.CardDeleteView.as_view(), name='delete'),
    path('<uuid:pk>/activate/', views.CardActivateView.as_view(), name='activate'),
    path('<uuid:pk>/deactivate/', views.CardDeactivateView.as_view(), name='deactivate'),
    path('<uuid:pk>/assign/', views.CardAssignView.as_view(), name='assign'),
]
