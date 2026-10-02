from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):

    # PRODUCT TYPE
    PRODUCT_TYPE_CHOICES = [
        ("fruits", "🍎 Fruits"),
        ("eggs", "🥚 Eggs"),
        ("snacks", "🍘 Snacks"),
    ]

    # CUSTOMER QUANTITY TYPE
    UNIT_CHOICES = [
        ("piece", "Piece"),
        ("weight", "Weight"),
        ("custom", "Custom Quantity"),
    ]

    # STOCK UNIT
    STOCK_UNIT_CHOICES = [
        ("piece", "Pieces"),
        ("g", "Grams (g)"),
        ("kg", "Kilograms (kg)"),
    ]

    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES,
        default="fruits"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=150)

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    description = models.TextField(blank=True)

    # CUSTOMER ORDERING TYPE
    unit_type = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default="piece"
    )

    # PRICE
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # STOCK QUANTITY
    stock = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # STOCK UNIT
    stock_unit = models.CharField(
        max_length=10,
        choices=STOCK_UNIT_CHOICES,
        default="piece"
    )

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name