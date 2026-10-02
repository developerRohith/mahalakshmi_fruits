from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "unit_type",
        "price",
        "stock",
        "is_available",
    )

    list_filter = (
        "category",
        "unit_type",
        "is_available",
    )

    search_fields = ("name",)

    list_editable = (
        "price",
        "stock",
        "is_available",
    )