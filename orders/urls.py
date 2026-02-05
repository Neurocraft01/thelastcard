from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('new/', views.OrderCreateView.as_view(), name='create'),
    path('my-orders/', views.OrderListView.as_view(), name='list'),
    path('<uuid:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]
