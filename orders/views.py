from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils import timezone

from .models import Order
from products.models import Product


def is_admin_user(user):
    return user.is_authenticated and user.is_staff


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "orders/my_orders.html",
        {"orders": orders}
    )


@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order.objects.prefetch_related("items__product"),
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        "orders/order_detail.html",
        {"order": order}
    )


@login_required
@user_passes_test(is_admin_user)
def admin_dashboard(request):

    today = timezone.localdate()

    today_orders = Order.objects.filter(
        created_at__date=today
    )

    today_sales = today_orders.exclude(
        order_status="cancelled"
    ).aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    pending_orders = Order.objects.filter(
        order_status="pending"
    ).count()

    delivered_orders = Order.objects.filter(
        order_status="delivered"
    ).count()

    total_products = Product.objects.count()

    # TOTAL ORDERS
    total_orders = Order.objects.exclude(
        order_status="cancelled"
    ).count()

    # TOTAL SALES
    total_sales = Order.objects.exclude(
        order_status="cancelled"
    ).aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    recent_orders = Order.objects.select_related(
        "user"
    ).order_by("-created_at")[:10]

    context = {
        "today_orders": today_orders.exclude(
            order_status="cancelled"
        ).count(),

        "today_sales": today_sales,

        "pending_orders": pending_orders,

        "delivered_orders": delivered_orders,

        "total_products": total_products,

        "total_orders": total_orders,

        "total_sales": total_sales,

        "recent_orders": recent_orders,
    }

    return render(
        request,
        "orders/admin_dashboard.html",
        context
    )


@login_required
@user_passes_test(is_admin_user)
def admin_orders(request):

    orders = Order.objects.prefetch_related(
        "items__product"
    ).order_by("-created_at")

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "")
    delivery_type = request.GET.get("delivery_type", "")
    payment_method = request.GET.get("payment_method", "")

    if search:
        orders = orders.filter(
            customer_name__icontains=search
        ) | orders.filter(
            mobile__icontains=search
        ) | orders.filter(
            id__icontains=search
        )

    if status:
        orders = orders.filter(
            order_status=status
        )

    if delivery_type:
        orders = orders.filter(
            delivery_type=delivery_type
        )

    if payment_method:
        orders = orders.filter(
            payment_method=payment_method
        )

    context = {
        "orders": orders,
        "search": search,
        "selected_status": status,
        "selected_delivery": delivery_type,
        "selected_payment": payment_method,
        "status_choices": Order.STATUS_CHOICES,
        "delivery_choices": Order.DELIVERY_CHOICES,
        "payment_choices": Order.PAYMENT_CHOICES,
    }

    return render(
        request,
        "orders/admin_orders.html",
        context
    )

@login_required
@user_passes_test(is_admin_user)
def admin_order_detail(request, order_id):

    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items__product"
        ),
        id=order_id
    )

    return render(
        request,
        "orders/admin_order_detail.html",
        {
            "order": order,
        }
    )



@login_required
@user_passes_test(is_admin_user)
def admin_order_status_update(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        new_status = request.POST.get("order_status")

        valid_statuses = dict(Order.STATUS_CHOICES)

        if new_status in valid_statuses:
            order.order_status = new_status
            order.save(update_fields=["order_status", "updated_at"])

    return redirect("admin_orders")

