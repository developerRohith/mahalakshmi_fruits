from django.urls import path
from . import views


urlpatterns = [

    # Customer Orders
    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),

    path(
        "my-orders/<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),


    # Admin Dashboard
    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),


    # Admin Orders
    path(
        "admin-orders/",
        views.admin_orders,
        name="admin_orders"
    ),

    # Admin Order Detail
    path(
        "admin-orders/<int:order_id>/",
        views.admin_order_detail,
        name="admin_order_detail"
    ),

    # Admin Order Status Update
    path(
        "admin-orders/<int:order_id>/status/",
        views.admin_order_status_update,
        name="admin_order_status_update"
    ),
]
