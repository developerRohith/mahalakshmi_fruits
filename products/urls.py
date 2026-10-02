from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.home,
        name="home"
    ),

    # CART
    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/increase/<int:product_id>/",
        views.increase_cart,
        name="increase_cart"
    ),

    path(
        "cart/decrease/<int:product_id>/",
        views.decrease_cart,
        name="decrease_cart"
    ),

    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    # CHECKOUT
    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "order-success/<int:order_id>/",
        views.order_success,
        name="order_success"
    ),

    # ORDER TRACKING
    path(
        "track-order/",
        views.track_order,
        name="track_order"
    ),

    path(
        "track-order/<int:order_id>/",
        views.track_order_detail,
        name="track_order_detail"
    ),

    # CUSTOMER ORDERS
    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),

    # ADMIN CATEGORY MANAGEMENT

path(
    "admin-categories/",
    views.admin_categories,
    name="admin_categories"
),

path(
    "admin-categories/<int:category_id>/toggle/",
    views.admin_category_toggle,
    name="admin_category_toggle"
),

path(
    "admin-categories/<int:category_id>/delete/",
    views.admin_category_delete,
    name="admin_category_delete"
),

    # ADMIN PRODUCT MANAGEMENT
    path(
        "admin-products/",
        views.admin_products,
        name="admin_products"
    ),

    path(
        "admin-products/<int:product_id>/toggle/",
        views.admin_product_toggle,
        name="admin_product_toggle"
    ),

    path(
        "admin-products/<int:product_id>/delete/",
        views.admin_product_delete,
        name="admin_product_delete"
    ),
    path(
    "admin-products/<int:product_id>/stock/",
    views.admin_product_stock_update,
    name="admin_product_stock_update"
),

]