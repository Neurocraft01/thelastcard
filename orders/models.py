from django.db import models
from django.conf import settings
import uuid


class CardOrder(models.Model):
    """Model for physical NFC card orders."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    CARD_TYPE_CHOICES = (
        ('standard', 'Standard PVC - ₹449'),
        ('premium', 'Metallic Premium - ₹649'),
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
        default='standard'
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
    def total_price(self):
        """Calculate total price based on card type and quantity."""
        PRICES = {
            'standard': 449,
            'premium': 649,
        }
        base_price = PRICES.get(self.card_type, 449)
        return base_price * self.quantity
