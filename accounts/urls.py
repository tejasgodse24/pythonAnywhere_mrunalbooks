from django.contrib import admin
from django.urls import path
from accounts.views import *

urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),
    path('activate/<email_token>/', activate_email, name='activate_email'),
    path('logout/', logout_page, name='logout'),
    path('not-login-error/', not_login_page, name='not_login'),

    path('show-membership-plans/', membershipPlans, name='membershipPlans'),

    path('user-profile/', user_profile_page, name='user_profile'),
    path('user-address/', user_address_page, name='user_address'),
    path('user-address/add-new-address', add_new_address, name='add_new_address'),
    path('user-address/edit-address/<addrss_uid>', edit_address, name='edit_address_profile'),
    path('user-change-password/', change_password, name='change_password'),

    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<token>', reset_forgot_password, name='reset_forgot_password'),

    path('show-orders/', show_orders, name='show_orders'),
    path('show-order-items/<order_uid>', show_order_items, name='show_order_items'),
    path('download/<order_uid>', download_invoice, name='download_invoice'),

    path('cart/', cart, name = 'cart'),
    path('wishlist/', wishlist, name='wishlist'),
   
    # ajax paths
    path('add-wishlist', add_to_wishlist_ajax, name='add_to_wishlist_ajax'),
    path('wishlist-items', remove_wishlist_item_ajax, name='remove_wishlist_item_ajax'),
    path('cart-items/', add_to_cart_ajax, name='add_to_cart_ajax'),
    path('remove-cart-item/', remove_cart_item_ajax, name='remove_cart_item_ajax'),
    path('reduce-cart-items/', reduce_quantity_cart_item_ajax, name='reduce_quantity_cart_item_ajax'),
    path('get-quantity-item-Incart/', get_quantity_item_Incart, name='get_quantity_item_Incart'),

    path('add-coupon/', add_coupon_ajax, name='add_coupon_ajax'),
    path('remove-coupon/', remove_coupon_ajax, name='remove_coupon_ajax'),
    path('get-all-prices/', get_all_prices_ajax, name='get_all_prices_ajax'),

    # payment
    path('final-purchase/', final_purchase, name = 'final_purchase'),
    path('make-final-payment', make_final_payment_ajax, name='make_final_payment_ajax'),
    path('final-purchase/edit-addrss/<addrss_uid>/', edit_address, name = 'edit_addrss_purchase'),
   
    path('payment-success/place-final-order/', place_order, name = 'place_order'),
    path('payment-failure/', payment_failure, name = 'payment_failure'),

    path('payment-success/prime-membership/', payment_prime_membership, name = 'payment_prime_membership'),



]
