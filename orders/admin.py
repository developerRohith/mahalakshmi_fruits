from django.contrib import admin
from django.contrib import messages
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    readonly_fields = (
        "product",
        "quantity",
        "price",
        "total",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer_name",
        "mobile",
        "delivery_type",
        "payment_method",
        "payment_status",
        "order_status",
        "total_amount",
        "created_at",
    )

    list_filter = (
        "order_status",
        "delivery_type",
        "payment_method",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "customer_name",
        "mobile",
        "email",
        "city",
        "pincode",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "subtotal",
        "delivery_charge",
        "total_amount",
    )

    fieldsets = (
        (
            "Customer Details",
            {
                "fields": (
                    "customer_name",
                    "mobile",
                    "email",
                )
            },
        ),

        (
            "Delivery Details",
            {
                "fields": (
                    "delivery_type",
                    "address",
                    "city",
                    "pincode",
                )
            },
        ),

        (
            "Payment",
            {
                "fields": (
                    "payment_method",
                    "payment_status",
                )
            },
        ),

        (
            "Order Status",
            {
                "fields": (
                    "order_status",
                )
            },
        ),

        (
            "Amount",
            {
                "fields": (
                    "subtotal",
                    "delivery_charge",
                    "total_amount",
                )
            },
        ),

        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    inlines = [
        OrderItemInline
    ]

    # =====================================================
    # BULK ORDER STATUS ACTIONS
    # =====================================================

    @admin.action(description="Mark selected orders as Confirmed")
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(
            order_status="confirmed"
        )

        self.message_user(
            request,
            f"{updated} order(s) marked as Confirmed.",
            messages.SUCCESS,
        )

    @admin.action(description="Mark selected orders as Preparing")
    def mark_preparing(self, request, queryset):
        updated = queryset.update(
            order_status="preparing"
        )

        self.message_user(
            request,
            f"{updated} order(s) marked as Preparing.",
            messages.SUCCESS,
        )

    @admin.action(description="Mark selected orders as Out for Delivery")
    def mark_out_for_delivery(self, request, queryset):
        updated = queryset.update(
            order_status="out_for_delivery"
        )

        self.message_user(
            request,
            f"{updated} order(s) marked as Out for Delivery.",
            messages.SUCCESS,
        )

    @admin.action(description="Mark selected orders as Ready for Pickup")
    def mark_ready_pickup(self, request, queryset):
        updated = queryset.update(
            order_status="ready_pickup"
        )

        self.message_user(
            request,
            f"{updated} order(s) marked as Ready for Pickup.",
            messages.SUCCESS,
        )

    @admin.action(description="Mark selected orders as Delivered")
    def mark_delivered(self, request, queryset):
        updated = queryset.update(
            order_status="delivered"
        )

        self.message_user(
            request,
            f"{updated} order(s) marked as Delivered.",
            messages.SUCCESS,
        )

    @admin.action(description="Cancel selected orders")
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(
            order_status="cancelled"
        )

        self.message_user(
            request,
            f"{updated} order(s) cancelled.",
            messages.WARNING,
        )

    actions = [
        "mark_confirmed",
        "mark_preparing",
        "mark_out_for_delivery",
        "mark_ready_pickup",
        "mark_delivered",
        "mark_cancelled",
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product",
        "quantity",
        "price",
        "total",
    )

    search_fields = (
        "product__name",
        "order__customer_name",
        "order__mobile",
    )

    ordering = (
        "-order__created_at",
    )