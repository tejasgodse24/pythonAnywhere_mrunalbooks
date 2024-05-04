from django.shortcuts import render, HttpResponse
from accounts.models import *
from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import render,  redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from custom_admin.decorators import user_in_group
import os
from django.conf import settings
from accounts.models import Order, OrderItems
from dealer.models import *
from custom_admin.models import * 
from base.helpers import *
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from base.emails import *



# Create your views here.


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(username = email)
        if len(user_obj) == 0 :
            messages.warning(request, "Email is not registered")
            return HttpResponseRedirect(request.path_info)
        
        if user_obj[0].profile.is_email_verified == False:
            messages.warning(request, "Email is not verified")
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].groups.filter(name="admin_manager").exists():
            messages.warning(request, "Permission Denied")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username = email, password = password)

        if not user_obj :
            messages.warning(request, "Password is wrong")
            return HttpResponseRedirect(request.path_info)
        
        if user_obj : 
            login(request, user_obj)
            return redirect('/custom-admin-management/dashboard')
    return render(request, 'custom_admin/login.html')



@user_in_group
def logout_page(request):
    logout(request)
    return redirect('/custom-admin-management/dashboard')


@user_in_group
def dashboard(request):
    today = timezone.now().date()
    today_total_orders = Order.objects.filter(order_date__date = today)
    total_pending_orders = Order.objects.filter(is_delivered = False, is_shipped = False)
    total_orders = Order.objects.filter(is_shipped = True)
    total_users = Profile.objects.filter(is_email_verified = True)

    context = {
        'today_total_orders' : today_total_orders.count(),
        'total_pending_orders' : total_pending_orders.count(),
        'total_orders' : total_orders.count(),
        'total_users' : total_users.count()
    }
    return render(request, 'custom_admin/dashboard.html', context)


# users
@user_in_group
def all_active_users(request):
    all_users = Profile.objects.filter(is_email_verified = True)
    if request.method == "POST":
        search = request.POST.get('search').strip()
        objs = Profile.objects.filter(
            Q(is_email_verified = True) & 
            (
                Q(user__email__iexact = search) |
                Q(mobile_number__iexact = search)
            )
        ).distinct()
        context = {
            'all_users' : objs
        }
        return render(request, 'custom_admin/users/all_active_users.html', context)
    context = {
        'all_users' : all_users
    }
    return render(request, 'custom_admin/users/all_active_users.html', context)

@user_in_group
def normal_users(request):
    normal_users = Profile.objects.filter(is_email_verified = True, login_type__name = "normal")
    context = {
        'normal_users' : normal_users
    }
    return render(request, 'custom_admin/users/normal_users.html', context)

@user_in_group
def prime_users(request):
    prime_users = Profile.objects.filter(is_email_verified = True, login_type__name = "prime")
    context = {
        'prime_users' : prime_users
    }
    return render(request, 'custom_admin/users/prime_users.html', context)

@user_in_group
def dealer_users(request):
    dealer_users = Profile.objects.filter(is_email_verified = True, login_type__name = "dealer")
    context = {
        'dealer_users' : dealer_users
    }
    return render(request, 'custom_admin/users/dealer_users.html', context)

@user_in_group
def not_verified_users(request):
    not_verified_users = Profile.objects.filter(is_email_verified = False, user__is_superuser = False)
    context = {
        'not_verified_users' : not_verified_users
    }
    return render(request, 'custom_admin/users/not_verified_users.html', context)



# membership
@user_in_group
def membership_prices(request):
    prime_prices = Membership_Plan_Prices.objects.get(membership_name__name = "prime")
    dealer_prices = Membership_Plan_Prices.objects.get(membership_name__name = "dealer")
    context = {
        'prime_prices' : prime_prices,
        'dealer_prices' : dealer_prices
    }
    return render(request, 'custom_admin/membership/membership_prices.html', context)


# orders
@user_in_group
def all_orders(request):
    all_orders = Order.objects.filter(is_delivered = False, is_accepted = None).order_by('-created_at')
    context = {'all_orders' : all_orders}
    return render(request, 'custom_admin/order/all_orders.html', context)



@user_in_group
def order_details(request, order_uid):
    order = Order.objects.get(uid = order_uid, is_delivered = False, is_shipped = False)
    all_items = OrderItems.objects.filter(order = order)

    if request.method == "POST":

        if 'confirm' in request.POST:
            print("confirm")
            order.is_delivered = True
            order.is_accepted = True
            if order.delivery_type == 'home':
                c = request.POST.get('couriers-radio')
                email = request.POST.get('email').strip()
                order.courier = Courier.objects.get(uid = c)
                send_order_dispatched_email.delay(email)
            order.save()
            messages.success(request, "Order Delivered Succesfully")
        else:
            order.is_accepted = False
            order.save()
            messages.warning(request, "Order Cancelled Succesfully")
        
        return redirect('/custom-admin-management/orders/all-orders')

    ship_a = None
    login_type = order.membership_type
    ship_a = order.shipping_address

    items_subtotal = order.get_items_subtotal(login_type)
    discount_price = 0
    if order.coupon:
        discount_price = order.coupon.discount_price
    
    shipping_charge = order.shipping_charge
    tax_amount = 0

    total_amount = items_subtotal + shipping_charge + tax_amount - discount_price
    
    context = {
        'all_items' : all_items,
        'user_name' : order.user.first_name + " " + order.user.last_name,
        'order' : order,
        'ship_a' : ship_a,
        'delivery_type' : order.delivery_type,
        'items_subtotal' : items_subtotal,
        'discount_price' : discount_price,
        'shipping_charge' : shipping_charge,
        'tax_amount' : tax_amount,
        'total_amount' : total_amount,
        'couriers' : Courier.objects.filter(is_active = True),
    }
    return render(request, 'custom_admin/order/order_details.html', context)

@user_in_group
def cancelled_orders(request):
    cancelled_orders = Order.objects.filter(is_accepted = False).order_by('-updated_at')
    context = {'all_orders' : cancelled_orders}
    return render(request, 'custom_admin/order/cancelled_orders.html', context)


@user_in_group
def cancelled_oreder_item(request, order_uid):

    order = Order.objects.get(uid = order_uid, is_accepted = False)
    all_items = OrderItems.objects.filter(order = order)
    login_type = order.membership_type

    ship_a = order.shipping_address

    items_subtotal = order.get_items_subtotal(login_type)

    discount_price = 0
    if order.coupon:
        discount_price = order.coupon.discount_price
    
    shipping_charge = order.shipping_charge

    tax_amount = 0

    total_amount = items_subtotal + shipping_charge + tax_amount - discount_price
      
    context = {
        'all_items' : all_items,
        'user_name' : order.user.first_name + " " + order.user.last_name,
        'order' : order,
        'ship_a' : ship_a,
        'delivery_type' : order.delivery_type,
        'items_subtotal' : items_subtotal,
        'discount_price' : discount_price,
        'shipping_charge' : shipping_charge,
        'tax_amount' : tax_amount,
        'total_amount' : total_amount,
        # 'page_type' : "shipped_orders"
    }
    return render(request, 'custom_admin/order/cancelled_order_details.html', context)


@user_in_group
def dispatched_orders(request):
    dispatched_orders = Order.objects.filter(is_delivered = True, is_shipped = False).order_by('-updated_at')
    context = {'all_orders' : dispatched_orders}
    return render(request, 'custom_admin/order/dispatched_orders.html', context)

@user_in_group
def shipped_orders(request):
    shipped_orders = Order.objects.filter(is_delivered = True, is_shipped = True).order_by('-updated_at')
    context = {'all_orders' : shipped_orders}
    return render(request, 'custom_admin/order/shipped_orders.html', context)


@user_in_group
def delivered_oreder_item(request, order_uid):
    order = Order.objects.get(uid = order_uid, is_delivered = True, is_shipped = False)
    all_items = OrderItems.objects.filter(order = order)
    login_type = order.membership_type

    if request.method == "POST":
        email = request.POST.get('email')
        order.is_shipped = True
        order.save()
        messages.success(request, "Order Shipped Succesfully")
        send_order_shipped_email.delay(email)
        return redirect('/custom-admin-management/orders/pending-orders')

    ship_a = order.shipping_address

    items_subtotal = order.get_items_subtotal(login_type)

    discount_price = 0
    if order.coupon:
        discount_price = order.coupon.discount_price
    
    shipping_charge = order.shipping_charge

    tax_amount = 0

    total_amount = items_subtotal + shipping_charge + tax_amount - discount_price
      
    context = {
        'all_items' : all_items,
        'user_name' : order.user.first_name + " " + order.user.last_name,
        'order' : order,
        'ship_a' : ship_a,
        'delivery_type' : order.delivery_type,
        'items_subtotal' : items_subtotal,
        'discount_price' : discount_price,
        'shipping_charge' : shipping_charge,
        'tax_amount' : tax_amount,
        'total_amount' : total_amount,
        'page_type' : "delivered_orders"
    }
    return render(request, 'custom_admin/order/dispatched_order_details.html', context)



@user_in_group
def shipped_oreder_item(request, order_uid):

    order = Order.objects.get(uid = order_uid, is_delivered = True, is_shipped = True)
    all_items = OrderItems.objects.filter(order = order)
    login_type = order.membership_type

    ship_a = order.shipping_address

    items_subtotal = order.get_items_subtotal(login_type)

    discount_price = 0
    if order.coupon:
        discount_price = order.coupon.discount_price
    
    shipping_charge = order.shipping_charge

    tax_amount = 0

    total_amount = items_subtotal + shipping_charge + tax_amount - discount_price
      
    context = {
        'all_items' : all_items,
        'user_name' : order.user.first_name + " " + order.user.last_name,
        'order' : order,
        'ship_a' : ship_a,
        'delivery_type' : order.delivery_type,
        'items_subtotal' : items_subtotal,
        'discount_price' : discount_price,
        'shipping_charge' : shipping_charge,
        'tax_amount' : tax_amount,
        'total_amount' : total_amount,
        'page_type' : "shipped_orders"
    }
    return render(request, 'custom_admin/order/shipped_order_details.html', context)

@user_in_group
def generate_download_courier_script(request, order_uid):
        # Construct the full path to the PDF file
    order = Order.objects.get(uid = order_uid)
    folder_path = settings.MEDIA_ROOT + '/courier_scripts/'
    pdf_filename = order.invoive_no  + '_courier_script.pdf'

    # Construct the full path to the PDF file
    pdf_path = os.path.join(folder_path, pdf_filename)

    # Check if the file exists
    if os.path.exists(pdf_path):
        try : 
            file_path = pdf_path
            response = FileResponse(open(file_path, "rb"), as_attachment=True)
            return response
        except Exception as e:
            print(e)
    else:
        params = {
            'order' : order
        }
        file_name , status = save_courier_script_pdf(params, order.invoive_no)
        try : 
            file_path = pdf_path
            response = FileResponse(open(file_path, "rb"), as_attachment=True)
            return response
        except Exception as e:
            return redirect('/error')



# dealer
@user_in_group
def show_dealers(request):
    all_dealers = Dealer.objects.all()
    context = {
        'all_dealers' : all_dealers,
    }
    return render(request, 'custom_admin/dealer/dealers.html', context)

# courier
@user_in_group
def show_couriers(request):
    all_couriers = Courier.objects.all()
    context = {
        'all_couriers' : all_couriers,
    }
    return render(request, 'custom_admin/courier/couriers.html', context)

# coupon
@user_in_group
def show_coupons(request):
    all_coupons = Coupon.objects.all()
    context = {
        'all_coupons' : all_coupons,
    }
    return render(request, 'custom_admin/coupon/coupons.html', context)
