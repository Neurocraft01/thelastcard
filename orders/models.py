from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Coupon(models.Model):
    """Coupon codes that can be applied to orders for discounts."""

    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    )

    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.CharField(max_length=255, blank=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="Percentage (0-100) or fixed amount in ₹"
    )
    min_order_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Minimum order amount required to use this coupon"
    )
    max_discount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Maximum discount amount (for percentage coupons)"
    )
    usage_limit = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Total number of times this coupon can be used (leave blank for unlimited)"
    )
    used_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.discount_type == 'percentage':
            return f"{self.code} - {self.discount_value}% off"
        return f"{self.code} - ₹{self.discount_value} off"

    @property
    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        if now < self.valid_from:
            return False
        if self.usage_limit is not None and self.used_count >= self.usage_limit:
            return False
        return True

    def get_discount(self, order_total):
        """Calculate discount for the given order total."""
        if not self.is_valid:
            return 0
        if order_total < self.min_order_amount:
            return 0
        if self.discount_type == 'percentage':
            discount = order_total * self.discount_value / 100
            if self.max_discount:
                discount = min(discount, self.max_discount)
        else:
            discount = min(self.discount_value, order_total)
        return round(discount, 2)


class CardOrder(models.Model):
    """Model for physical NFC card orders."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('payment_pending', 'Payment Pending'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('created', 'Order Created'),
        ('authorized', 'Authorized'),
        ('captured', 'Captured'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    CARD_TYPE_CHOICES = (
        ('white_pvc', 'White PVC Card - ₹449'),
        ('pink_pvc', 'Pink PVC Card - ₹449'),
        ('metallic', 'Metallic Premium Card - ₹649'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='card_orders'
    )
    
    # Order Details
    card_type = models.CharField(
        max_length=20,
        choices=CARD_TYPE_CHOICES,
        default='white_pvc'
    )
    quantity = models.PositiveIntegerField(default=1)
    
    # Customization
    custom_design = models.ImageField(
        upload_to='orders/designs/',
        blank=True,
        null=True,
        help_text="Upload your custom design/logo (optional)"
    )
    custom_text = models.CharField(
        max_length=100,
        blank=True,
        help_text="Name or text to print on card"
    )
    
    # Shipping
    shipping_address = models.TextField()
    
    # Status & Tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    tracking_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True, help_text="Special instructions")
    
    # Payment (Razorpay)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Coupon
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders'
    )
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Card Order'
        verbose_name_plural = 'Card Orders'
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.email} - {self.get_status_display()}"
    
    @property
    def order_number(self):
        return f"TLC-{str(self.id)[:8].upper()}"
    
    @property
    def subtotal(self):
        """Calculate subtotal before discount."""
        PRICES = {
            'white_pvc': 449,
            'pink_pvc': 449,
            'metallic': 649,
        }
        base_price = PRICES.get(self.card_type, 449)
        return base_price * self.quantity

    @property
    def total_price(self):
        """Calculate total price after discount."""
        return max(self.subtotal - self.discount_amount, 0)
