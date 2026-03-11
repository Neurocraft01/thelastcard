from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('new/', views.OrderCreateView.as_view(), name='create'),
    path('my-orders/', views.OrderListView.as_view(), name='list'),
    path('<uuid:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<uuid:pk>/cancel/', views.OrderCancelView.as_view(), name='cancel'),
    path('<uuid:pk>/payment/', views.OrderPaymentView.as_view(), name='payment'),
    path('<uuid:pk>/payment/callback/', views.OrderPaymentCallbackView.as_view(), name='payment_callback'),
    path('<uuid:pk>/apply-coupon/', views.ApplyCouponView.as_view(), name='apply_coupon'),
    path('<uuid:pk>/remove-coupon/', views.RemoveCouponView.as_view(), name='remove_coupon'),
]
