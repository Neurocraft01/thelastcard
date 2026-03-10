# Generated manually - Add Razorpay payment fields and new order statuses

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_cardorder_card_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardorder',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cardorder',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cardorder',
            name='razorpay_signature',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cardorder',
            name='payment_status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending'),
                    ('created', 'Order Created'),
                    ('authorized', 'Authorized'),
                    ('captured', 'Captured'),
                    ('failed', 'Failed'),
                    ('refunded', 'Refunded'),
                ],
                default='pending',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='cardorder',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='cardorder',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending'),
                    ('payment_pending', 'Payment Pending'),
                    ('paid', 'Paid'),
                    ('processing', 'Processing'),
                    ('shipped', 'Shipped'),
                    ('delivered', 'Delivered'),
                    ('cancelled', 'Cancelled'),
                ],
                default='pending',
                max_length=20,
            ),
        ),
    ]
