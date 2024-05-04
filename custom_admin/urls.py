
from django.contrib import admin
from django.urls import path
from custom_admin.views import *
from products.admin import product_site, coupon_site
from accounts.admin import membership_site
from dealer.admin import dealer_site
from custom_admin.admin import courier_site

urlpatterns = [

    # admin sites urls
    path('product-entry-tables/', product_site.urls),
    path('memberships-management/', membership_site.urls),
    path('dealership-management/', dealer_site.urls),
    path('coupon-management/', coupon_site.urls),
    path('courier-services-management/', courier_site.urls),

    # custom admin urls
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout'),
    path('dashboard', dashboard, name="admin_dashboard"),
    # users
    path('users/all-active-users', all_active_users, name="all_active_users"),
    path('users/normal-users', normal_users, name="normal_users"),
    path('users/prime-users', prime_users, name="prime_users"),
    path('users/dealer-users', dealer_users, name="dealer_users"),
    path('users/not-verified-users', not_verified_users, name="not_verified_users"),

    # membership
    path('membership/prices', membership_prices, name="membership_prices"),

    # orders
    path('orders/all-orders', all_orders, name="all_orders"),
    path('orders/order-details/<order_uid>', order_details, name="order_details"),

    path('orders/pending-orders', dispatched_orders, name="dispatched_orders"),
    path('orders/pending-order-details/<order_uid>', delivered_oreder_item, name="delivered_oreder_item"),

    path('orders/shipped-orders', shipped_orders, name="shipped_orders"),
    path('orders/shipped-order-details/<order_uid>', shipped_oreder_item, name="shipped_oreder_item"),

    path('orders/cancelled-orders', cancelled_orders, name="cancelled_orders"),
    path('orders/cancelled-order-details/<order_uid>', cancelled_oreder_item, name="cancelled_oreder_item"),

    path('orders/download/<order_uid>', generate_download_courier_script, name='generate_download_courier_script'),

    # dealers
    path('dealer/all-dealers', show_dealers, name="show_dealers"),

    # couriers
    path('couriers/all-couriers', show_couriers, name="show_couriers"),

    # coupon
    path('coupon/all-coupon', show_coupons, name="show_coupons"),

    # search




] 

