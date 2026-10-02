from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Product, Category
from orders.models import Order, OrderItem


# =========================================================
# CUSTOMER HOME
# =========================================================

def home(request):

    categories = Category.objects.filter(
        is_active=True
    )

    products = Product.objects.filter(
        is_available=True
    ).select_related("category")

    # PRODUCT TYPE FILTER
    product_type = request.GET.get(
        "type",
        ""
    )

    if product_type in [
        "fruits",
        "eggs",
        "snacks"
    ]:

        products = products.filter(
            product_type=product_type
        )

    # PRODUCT SEARCH
    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        products = products.filter(
            name__icontains=search
        )

    return render(
        request,
        "products/home.html",
        {
            "categories": categories,
            "products": products,
            "selected_product_type": product_type,
            "search": search,
        }
    )


# =========================================================
# CART
# =========================================================

def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    cart = request.session.get("cart", {})

    product_id = str(product.id)

    # =====================================================
    # WEIGHT PRODUCT
    # =====================================================

    if product.unit_type == "weight":

        quantity = Decimal(
            request.GET.get(
                "quantity",
                "100"
            )
        )

        unit = request.GET.get(
            "unit",
            "g"
        )

        if unit == "kg":
            quantity_kg = quantity
        else:
            quantity_kg = quantity / Decimal("1000")

        cart[product_id] = {
            "quantity": str(quantity_kg),
            "display_quantity": str(quantity),
            "unit": unit,
            "price": str(product.price),
        }


    # =====================================================
    # CUSTOM QUANTITY PRODUCT
    # =====================================================

    elif product.unit_type == "custom":

        try:

            quantity = int(
                request.GET.get(
                    "quantity",
                    "1"
                )
            )

        except (ValueError, TypeError):

            quantity = 1

        if quantity < 1:
            quantity = 1

        if quantity > product.stock:
            quantity = int(product.stock)

        if product_id in cart:

            current_quantity = int(
                cart[product_id]["quantity"]
            )

            new_quantity = (
                current_quantity + quantity
            )

            if new_quantity > product.stock:
                new_quantity = int(
                    product.stock
                )

            cart[product_id]["quantity"] = new_quantity

        else:

            cart[product_id] = {
                "quantity": quantity,
                "price": str(product.price),
            }


    # =====================================================
    # PIECE PRODUCT
    # =====================================================

    else:

        if product_id in cart:

            cart[product_id]["quantity"] += 1

        else:

            cart[product_id] = {
                "quantity": 1,
                "price": str(product.price),
            }

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def cart(request):

    cart_data = request.session.get(
        "cart",
        {}
    )

    cart_items = []

    subtotal = Decimal("0.00")

    for product_id, item in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True
        )

        quantity = Decimal(
            str(item["quantity"])
        )

        price = Decimal(
            str(product.price)
        )

        total = quantity * price

        subtotal += total

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "price": price,
            "total": total,
        })

    return render(
        request,
        "products/cart.html",
        {
            "cart_items": cart_items,
            "subtotal": subtotal,
        }
    )


def increase_cart(request, product_id):

    cart_data = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    if product_id in cart_data:

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True
        )

        current_quantity = Decimal(
            str(
                cart_data[product_id]["quantity"]
            )
        )

        if product.unit_type == "weight":

            current_quantity += Decimal("0.1")

        else:

            current_quantity += Decimal("1")

        cart_data[product_id]["quantity"] = str(
            current_quantity
        )

    request.session["cart"] = cart_data
    request.session.modified = True

    return redirect("cart")


def decrease_cart(request, product_id):

    cart_data = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    if product_id in cart_data:

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True
        )

        current_quantity = Decimal(
            str(
                cart_data[product_id]["quantity"]
            )
        )

        if product.unit_type == "weight":

            current_quantity -= Decimal("0.1")

        else:

            current_quantity -= Decimal("1")

        if current_quantity <= 0:

            del cart_data[product_id]

        else:

            cart_data[product_id]["quantity"] = str(
                current_quantity
            )

    request.session["cart"] = cart_data
    request.session.modified = True

    return redirect("cart")


def remove_from_cart(request, product_id):

    cart_data = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    if product_id in cart_data:

        del cart_data[product_id]

    request.session["cart"] = cart_data
    request.session.modified = True

    return redirect("cart")


# =========================================================
# CHECKOUT
# =========================================================

def checkout(request):

    cart_data = request.session.get(
        "cart",
        {}
    )

    if not cart_data:

        return redirect("cart")

    cart_items = []

    subtotal = Decimal("0.00")

    for product_id, item in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True
        )

        quantity = Decimal(
            str(item["quantity"])
        )

        price = Decimal(
            str(product.price)
        )

        total = quantity * price

        subtotal += total

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "price": price,
            "total": total,
            "unit": item.get(
                "unit",
                ""
            ),
            "display_quantity": item.get(
                "display_quantity",
                quantity
            ),
        })

    # =====================================================
    # PROFILE
    # =====================================================

    profile = None

    if request.user.is_authenticated:

        profile = getattr(
            request.user,
            "profile",
            None
        )

    # =====================================================
    # PLACE ORDER
    # =====================================================

    if request.method == "POST":

        customer_name = request.POST.get(
            "customer_name",
            ""
        ).strip()

        mobile = request.POST.get(
            "mobile",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        address = request.POST.get(
            "address",
            ""
        ).strip()

        city = request.POST.get(
            "city",
            ""
        ).strip()

        pincode = request.POST.get(
            "pincode",
            ""
        ).strip()

        delivery_type = request.POST.get(
            "delivery_type",
            "delivery"
        )

        payment_method = request.POST.get(
            "payment_method",
            "cod"
        )

        # =================================================
        # BASIC VALIDATION
        # =================================================

        if not customer_name or not mobile:

            return render(
                request,
                "products/checkout.html",
                {
                    "cart_items": cart_items,
                    "subtotal": subtotal,
                    "profile": profile,
                    "error": (
                        "Please enter your name "
                        "and mobile number."
                    ),
                }
            )

        # =================================================
        # STOCK VALIDATION
        # =================================================

        for item in cart_items:

            product = item["product"]
            quantity = item["quantity"]

            if quantity > product.stock:

                return render(
                    request,
                    "products/checkout.html",
                    {
                        "cart_items": cart_items,
                        "subtotal": subtotal,
                        "profile": profile,
                        "error": (
                            f"Sorry, only "
                            f"{product.stock} available "
                            f"for {product.name}."
                        ),
                    }
                )

        # =================================================
        # ONLINE PAYMENT
        # =================================================

        if payment_method == "online":

            return render(
                request,
                "products/checkout.html",
                {
                    "cart_items": cart_items,
                    "subtotal": subtotal,
                    "profile": profile,
                    "error": (
                        "Online payment will be "
                        "available soon. Please "
                        "select Cash on Delivery."
                    ),
                }
            )

        # =================================================
        # DELIVERY CHARGE
        # =================================================

        delivery_charge = Decimal("0.00")

        total_amount = (
            subtotal +
            delivery_charge
        )

        # =================================================
        # USER
        # =================================================

        user = (
            request.user
            if request.user.is_authenticated
            else None
        )

        # =================================================
        # CREATE ORDER
        # =================================================

        order = Order.objects.create(

            user=user,

            customer_name=customer_name,

            mobile=mobile,

            email=email,

            address=address,

            city=city,

            pincode=pincode,

            delivery_type=delivery_type,

            payment_method="cod",

            payment_status="pending",

            order_status="pending",

            subtotal=subtotal,

            delivery_charge=delivery_charge,

            total_amount=total_amount,
        )

        # =================================================
        # CREATE ORDER ITEMS + REDUCE STOCK
        # =================================================

        for item in cart_items:

            product = item["product"]
            quantity = item["quantity"]

            # Create order item
            OrderItem.objects.create(

                order=order,

                product=product,

                quantity=quantity,

                price=item["price"],

                total=item["total"],
            )

            # ---------------------------------------------
            # REDUCE PRODUCT STOCK
            # ---------------------------------------------

            product.stock -= quantity

            # Prevent negative stock
            if product.stock < 0:

                product.stock = Decimal("0.00")

            product.save(
                update_fields=[
                    "stock"
                ]
            )

        # =================================================
        # CLEAR CART
        # =================================================

        request.session["cart"] = {}

        request.session.modified = True

        # =================================================
        # ORDER SUCCESS
        # =================================================

        return redirect(
            "order_success",
            order_id=order.id
        )

    # =====================================================
    # CHECKOUT PAGE
    # =====================================================

    return render(
        request,
        "products/checkout.html",
        {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "profile": profile,
        },
    )


# =========================================================
# ORDER SUCCESS
# =========================================================

def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        "products/order_success.html",
        {
            "order": order,
        }
    )


# =========================================================
# ORDER TRACKING
# =========================================================

def track_order(request):

    return render(
        request,
        "products/track_order.html"
    )


def track_order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        "products/track_order_detail.html",
        {
            "order": order,
        }
    )


# =========================================================
# MY ORDERS
# =========================================================

def my_orders(request):

    if not request.user.is_authenticated:

        return redirect("login")

    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        "items"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "products/my_orders.html",
        {
            "orders": orders,
        }
    )


# =========================================================
# ADMIN USER CHECK
# =========================================================

def is_admin_user(user):

    return (
        user.is_authenticated
        and user.is_staff
    )


# =========================================================
# ADMIN PRODUCT MANAGEMENT
# =========================================================

@login_required
@user_passes_test(is_admin_user)
def admin_products(request):

    products = Product.objects.select_related(
        "category"
    ).order_by(
        "name"
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    category_id = request.GET.get(
        "category",
        ""
    )

    availability = request.GET.get(
        "availability",
        ""
    )

    if search:

        products = products.filter(
            name__icontains=search
        )

    if category_id:

        products = products.filter(
            category_id=category_id
        )

    if availability == "available":

        products = products.filter(
            is_available=True
        )

    elif availability == "unavailable":

        products = products.filter(
            is_available=False
        )

    categories = Category.objects.filter(
        is_active=True
    ).order_by(
        "name"
    )

    context = {

        "products": products,

        "categories": categories,

        "search": search,

        "selected_category": category_id,

        "selected_availability": availability,
    }

    return render(
        request,
        "products/admin_products.html",
        context
    )


@login_required
@user_passes_test(is_admin_user)
def admin_product_toggle(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    product.is_available = (
        not product.is_available
    )

    product.save(
        update_fields=[
            "is_available"
        ]
    )

    return redirect(
        "admin_products"
    )


@login_required
@user_passes_test(is_admin_user)
def admin_product_delete(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        product.delete()

    return redirect(
        "admin_products"
    )


# =========================================================
# ADMIN CATEGORY MANAGEMENT
# =========================================================

@login_required
@user_passes_test(is_admin_user)
def admin_categories(request):

    categories = Category.objects.all().order_by(
        "name"
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    status = request.GET.get(
        "status",
        ""
    )

    if search:

        categories = categories.filter(
            name__icontains=search
        )

    if status == "active":

        categories = categories.filter(
            is_active=True
        )

    elif status == "inactive":

        categories = categories.filter(
            is_active=False
        )

    context = {

        "categories": categories,

        "search": search,

        "selected_status": status,
    }

    return render(
        request,
        "products/admin_categories.html",
        context
    )


@login_required
@user_passes_test(is_admin_user)
def admin_category_toggle(
    request,
    category_id
):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    category.is_active = (
        not category.is_active
    )

    category.save(
        update_fields=[
            "is_active"
        ]
    )

    return redirect(
        "admin_categories"
    )


@login_required
@user_passes_test(is_admin_user)
def admin_category_delete(
    request,
    category_id
):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == "POST":

        category.delete()

    return redirect(
        "admin_categories"
    )


# =========================================================
# ADMIN PRODUCT STOCK MANAGEMENT
# =========================================================

@login_required
@user_passes_test(is_admin_user)
def admin_product_stock_update(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        stock = request.POST.get(
            "stock",
            ""
        ).strip()

        try:

            stock = Decimal(stock)

            if stock >= 0:

                product.stock = stock

                product.save(
                    update_fields=[
                        "stock"
                    ]
                )

        except (
            ValueError,
            TypeError,
            InvalidOperation
        ):

            pass

    return redirect(
        "admin_products"
    )