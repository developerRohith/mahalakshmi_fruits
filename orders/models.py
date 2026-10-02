from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):

    DELIVERY_CHOICES = [
        ("delivery", "Home Delivery"),
        ("pickup", "Shop Pickup"),
    ]

    PAYMENT_CHOICES = [
        ("cod", "Cash on Delivery"),
        ("online", "Online Payment"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("preparing", "Preparing"),
        ("out_for_delivery", "Out for Delivery"),
        ("ready_pickup", "Ready for Pickup"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="orders"
)
    customer_name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)

    delivery_type = models.CharField(
        max_length=20,
        choices=DELIVERY_CHOICES,
        default="delivery"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="cod"
    )

    payment_status = models.CharField(
        max_length=20,
        default="pending"
    )

    order_status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending"
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    delivery_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"