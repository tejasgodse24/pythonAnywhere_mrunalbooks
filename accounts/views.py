from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, FileResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.models import *
from base.emails import *
from products.models import Product, Coupon
from dealer.models import Dealer, Dealer_Address
from accounts.forms import *
from django.urls import resolve
from base.helpers import *
from datetime import datetime, timedelta
from accounts.decorators import is_user_normal
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
import uuid
# Create your views here.



def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not User.objects.filter(username=email).first():
                messages.warning(request, 'Not user found with this username.')
                return redirect('/accounts/forgot-password/')
        
        user_obj = User.objects.get(username = email)
        token = uuid.uuid4()
        profile_obj= Profile.objects.get(user = user_obj)
        profile_obj.forgot_password_token = str(token)
        profile_obj.save()
        send_forget_password_email.delay(user_obj.email , token)
        messages.success(request, 'An email is sent.')
        return redirect('/accounts/forgot-password/')
    return render(request, 'accounts/forgot_password.html')



def reset_forgot_password(request, token):
    context={}
    try : 
        profile_obj = Profile.objects.get(forgot_password_token = token)
        context = {'user_id' : profile_obj.user.id}
        if request.method == "POST":
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            if user_id is None:
                messages.warning(request, 'No user id found.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if  new_password != confirm_password:
                messages.warning(request, 'Both must  be equal.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'Password has been reset Successfully')
            return redirect('/accounts/login')

        return render(request, 'accounts/reset_forgot_password.html', context)
    except Exception as e:
        messages.success(request, 'Invalid Link')
        return redirect('/accounts/forgot-password/')



@login_required
def change_password(request):
    if request.POST:
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password is Changed Succesfuly")
            return redirect('/accounts/user-profile')
        else:
            context = {
                'form' : form
            }
            return render(request, 'accounts/change_password.html', context)
            
    form = PasswordChangeForm(user = request.user)
    context = {
        'form' : form
    }
    return render(request, 'accounts/change_password.html', context)



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
        
        user_obj = authenticate(username = email, password = password)

        if not user_obj :
            messages.warning(request, "Password is wrong")
            return HttpResponseRedirect(request.path_info)
        
        if user_obj : 
            login(request, user_obj)
            if request.GET.get('next'):
                next = request.GET.get('next')
                return redirect(next)
            return redirect('/')
    return render(request, 'accounts/login.html')



import re
def register_page(request):

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, "Email is already registered")
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(first_name = fname, last_name = lname, email= email, username = email)
        user_obj.set_password(password)
        user_obj.save()
        email_token = str(uuid.uuid4())
        Profile.objects.create(user = user_obj, email_token = email_token, mobile_number = phone)
        email = user_obj.email
        send_account_activation_email.delay(email, email_token)

        messages.success(request, "An Verification email has been sent on your mail to Verify your Account")
        return HttpResponseRedirect(request.path_info)


    return render(request, 'accounts/register.html')


@login_required
def logout_page(request):
    logout(request)
    return redirect('/')



def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verified = True
        login_type = MembershipType.objects.get(name = 'normal')
        user.login_type = login_type
        user.save()
        return render(request, 'accounts/email_verified.html')
    except Exception as e:
        return HttpResponse('Invalid Email token')

    


def not_login_page(request):
    return render(request, 'accounts/not_login.html', {'type':"Wishlist"})


def cart(request):

    if request.user.is_authenticated : 
        cart , _ = Cart.objects.get_or_create(user = request.user)

        login_type = request.user.profile.login_type.name
        item_subtotal = cart.get_cart_books_total(login_type)
        total_pay = cart.get_cart_total(login_type)


        context = {
            'cart' : cart.cart_items.order_by('product'),
            'total_pay' : total_pay,
            'user_cart' : cart,
            'item_subtotal' : item_subtotal
            }
        return render(request, 'accounts/cart.html', context)
    else:
        return render(request, 'accounts/not_login.html', {'type': "Cart"})


def wishlist(request):
    if request.user.is_authenticated : 
        wishlist , _  = WishList.objects.get_or_create(user = request.user)
        context = {'wishlist' : wishlist.wishlist_items.all()}
        return render(request, 'accounts/wishlist.html', context)
    else:
        return render(request, 'accounts/not_login.html', {'type': "Wishlist"})



@login_required
def add_to_cart_ajax(request):

    if request.method == "GET":
        product_uid = request.GET.get('book_uid')
        product = Product.objects.get(uid = product_uid)
        user = request.user
        cart , _ = Cart.objects.get_or_create(user = user)

        cart_item = CartItems.objects.filter(cart = cart, product = product)

        if cart_item :
            cart_item = CartItems.objects.get(cart = cart, product = product)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        else : 
            cart_item = CartItems.objects.create(cart = cart, product = product)

        total_cart_count = request.user.profile.get_cart_count()

        coupon_discount_price = 0
        if cart.coupon:
            coupon_discount_price = cart.coupon.discount_price

        
        if request.user.profile.login_type.name == 'normal':
            cart_item_quantity_price = cart_item.quantity*cart_item.product.normal_price
        elif request.user.profile.login_type.name == 'prime':
            cart_item_quantity_price = cart_item.quantity*cart_item.product.prime_price
        else :
            cart_item_quantity_price = cart_item.quantity*cart_item.product.dealer_price
        
        login_type = request.user.profile.login_type.name
        cart_total_price = cart.get_cart_total(login_type)
        get_cart_books_total = cart.get_cart_books_total(login_type)

        data = {
            'total_cart_count' : total_cart_count,
            'cart_item_quantity' : cart_item.quantity,
            'cart_item_quantity_price' : cart_item_quantity_price,
            'cart_total_price' : cart_total_price,
            'coupon_discount_price' : coupon_discount_price,
            'get_cart_books_total' : get_cart_books_total
            }
        return JsonResponse(data)


@login_required
def remove_cart_item_ajax(request):
    product_uid = request.GET.get('book_uid')

    product = Product.objects.get(uid = product_uid)
    user = request.user

    cart = Cart.objects.get(user = user)

    cart_item = CartItems.objects.get(cart = cart, product = product)
    cart_item.delete()

    cart = user.carts.get()
    isCouponDismissed = False
    if cart.coupon : 
        try : 
            if cart.get_cart_total() < cart.coupon.minimum_amount:
                messages.warning(request, f'Total amount should be grater than {cart.coupon.minimum_amount}')
                remove_coupon(request, cart.uid)
                isCouponDismissed = True
        except Exception as e:
            ...

    total_cart_count = request.user.profile.get_cart_count()

    coupon_discount_price = 0
    if cart.coupon:
        coupon_discount_price = cart.coupon.discount_price
    
    login_type = request.user.profile.login_type.name
    cart_total_price = cart.get_cart_total(login_type)
    get_cart_books_total = cart.get_cart_books_total(login_type)

  
    data = {
        'total_cart_count' : total_cart_count,
        'cart_total_price' : cart_total_price,
        'isCouponDismissed' : isCouponDismissed,
        'coupon_discount_price' : coupon_discount_price,
        'get_cart_books_total' : get_cart_books_total
    }
    return JsonResponse(data)



@login_required
def reduce_quantity_cart_item_ajax(request):

    product_uid = request.GET.get('book_uid')

    product = Product.objects.get(uid = product_uid)
    user = request.user

    cart = Cart.objects.get(user = user)

    cart_item = CartItems.objects.filter(cart = cart, product = product)[0]

    cart_item.quantity = max(0, cart_item.quantity - 1)
    cart_item.save()

    cart_item_quantity = cart_item.quantity

    if cart_item.quantity == 0:
        cart_item.delete()
        cart_item_quantity = 0

    cart = user.carts.get()
    isCouponDismissed = False
    if cart.coupon : 
        try : 
            if cart.get_cart_total() < cart.coupon.minimum_amount:
                messages.warning(request, f'Total amount should be grater than {cart.coupon.minimum_amount}')
                remove_coupon(request, cart.uid)
                isCouponDismissed = True
        except Exception as e:
            ...
    
    total_cart_count = request.user.profile.get_cart_count()

    coupon_discount_price = 0
    if cart.coupon:
        coupon_discount_price = cart.coupon.discount_price
    
        
    if request.user.profile.login_type.name == 'normal':
        cart_item_quantity_price = cart_item.quantity*cart_item.product.normal_price
    elif request.user.profile.login_type.name == 'prime':
        cart_item_quantity_price = cart_item.quantity*cart_item.product.prime_price
    else :
        cart_item_quantity_price = cart_item.quantity*cart_item.product.dealer_price
    
    login_type = request.user.profile.login_type.name
    cart_total_price = cart.get_cart_total(login_type)
    get_cart_books_total = cart.get_cart_books_total(login_type)

    data = { 
        'cart_item_quantity' : cart_item_quantity ,
        'total_cart_count' : total_cart_count,
        'cart_item_quantity_price' : cart_item_quantity_price,
        'cart_total_price' : cart_total_price,
        'isCouponDismissed' : isCouponDismissed,
        'coupon_discount_price' : coupon_discount_price,
        'get_cart_books_total' : get_cart_books_total
        }
    return JsonResponse(data)
    

@login_required
def add_to_wishlist_ajax(request):
    
    product_uid = request.GET.get('book_uid')
    product = Product.objects.get(uid=product_uid)
    user = request.user

    wishlist , _ = WishList.objects.get_or_create(user = user)

    wishlist_item = WishListItems.objects.filter(wishlist = wishlist, product = product)

    if wishlist_item :
        ...
    else:
        wishlist_item = WishListItems.objects.create(wishlist = wishlist, product = product)

    total_wishlist_count = request.user.profile.get_wishlist_count()
    data = {'total_wishlist_count' : total_wishlist_count}
    return JsonResponse(data)




@login_required
def remove_wishlist_item_ajax(request):

    product_uid = request.GET.get('book_uid')

    product = Product.objects.get(uid = product_uid)
    wishlist = WishList.objects.get(user = request.user)

    wishlist_item = WishListItems.objects.get(wishlist = wishlist, product = product)
    wishlist_item.delete()

    total_wishlist_count = request.user.profile.get_wishlist_count()
    data = {'total_wishlist_count' : total_wishlist_count}
   
    return JsonResponse(data)

@login_required
def get_quantity_item_Incart(request):
    product_uid = request.GET.get('book_uid')
    product = Product.objects.get(uid = product_uid)
    cart = Cart.objects.get_or_create(user = request.user)
    cart_item = CartItems.objects.get(cart = cart, product = product)
    data = {
        'cart_item_quantity' : cart_item.quantity
    }
    return JsonResponse(data)


def user_profile_page(request) :
    if request.user.is_authenticated : 
        if request.method == "POST":
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            user_obj = request.user
            user_obj.first_name = fname
            user_obj.last_name = lname
            user_obj.save()

        return render(request, 'accounts/profile.html')
    else:
        return redirect('/accounts/login/')
    
@login_required
def user_address_page(request):
    addrss = request.user.addressess.all() 
    if not addrss:
        return redirect('/accounts/user-address/add-new-address')
    context = {
        'addrss' : addrss,
    }
    return render(request, 'accounts/show_address.html', context)

@login_required
def add_new_address(request):
    if request.method == 'POST':

        details = AddressForm(request.POST)
        if details.is_valid():  
            ads_form = details.save(commit = False)
            ads_form.user = request.user

            if not request.user.addressess.all() :
                ads_form.is_default = True
            
            ads_form.save()  
            messages.success(request, 'Address Added Successfully')
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('/accounts/user-address/')
        else:
            context = {
                'form' : details
            }
            return render(request, 'accounts/add_address.html', context)
    context = {
        'form' : AddressForm(None)
    }
    return render(request, 'accounts/add_address.html', context)



def final_purchase(request):
    cart , _ = Cart.objects.get_or_create(user = request.user)

    # if request.method == 'POST':
       
    #     if 'address-submit' in request.POST:
    #         details = AddressForm(request.POST)
    
    #         if details.is_valid():  
    #             ads_form = details.save(commit = False)
    #             ads_form.user = request.user
    
    #             if not request.user.addressess.all() :
    #                 ads_form.is_default = True
                
    #             ads_form.save()  
    #             messages.success(request, "Address Saved Successfully")
    #             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #         else:
    #             cart = Cart.objects.get(user = request.user)
    #             login_type = request.user.profile.login_type.name
    #             cart_total_price = cart.get_cart_total(login_type)

    #             context = {
    #                 'cart': cart,
    #                 'total_pay' : cart_total_price,
    #                 'form' : details
    #             }
    #             return render(request, "accounts/final_purchase.html", context) 
    cart = Cart.objects.get(user = request.user)
    addrss = request.user.addressess.all()

    login_type = request.user.profile.login_type.name
    cart_total_price = cart.get_cart_total(login_type)
    item_subtotal = cart.get_cart_books_total(login_type)

    context = {
        'cart': cart,
        'total_pay' : cart_total_price,
        'item_subtotal' : item_subtotal,
        'form' : AddressForm(None),
        'addrss' : addrss,
        'cart_items' : cart.cart_items.order_by('product'),
        'payment_mode' : False
    }
    return render(request, 'accounts/final_purchase.html', context)


def make_final_payment_ajax(request):
    
    cart = Cart.objects.get(user = request.user)
    selected_adrss_uid = request.GET.get('selected_adress_option')
    tax_amount = 0
    shipping_charge = 0
    try:
        # home delivery
        ship_a = Address.objects.get(uid = selected_adrss_uid)
        shipping_charge = request.user.profile.login_type.home_delivery_price
    except Exception as e:
        # pickup point 
        ship_a = Dealer_Address.objects.get(uid = selected_adrss_uid)
        shipping_charge = 0

    login_type = request.user.profile.login_type.name
    cart_total_price = cart.get_cart_total(login_type) + shipping_charge + tax_amount
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
    payment = client.order.create({'amount' : cart_total_price*100, 'currency' : 'INR', 'payment_capture' : 1  })
    context = {
        'payment_mode' : True,
        'payment' : payment,
        'selected_adrss_uid' : selected_adrss_uid
    }
    return JsonResponse(context)



def edit_address(request, addrss_uid):

    address = Address.objects.get(uid = addrss_uid)
    form = AddressForm(instance = address)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        resolved_url = resolve(request.path_info)
        url_name = resolved_url.url_name
        if form.is_valid():
            form.save()
            if url_name == 'edit_addrss_purchase':
                messages.success(request, "Address Edited Successfully")
                return redirect('/accounts/final-purchase/')
            elif url_name == 'edit_address_profile':
                messages.success(request, "Address Edited Successfully")
                return redirect('/accounts/user-address/')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            context = {
                'form' : form
            }
            return render(request, 'accounts/edit_address.html', context)


    
    context = {'form':form}
    return render(request, 'accounts/edit_address.html', context)
   


def add_coupon_ajax(request):

    if request.method == "POST":
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__iexact = coupon)
        cart = Cart.objects.get(user = request.user)
        login_type = request.user.profile.login_type.name

        if not coupon_obj.exists():
            return JsonResponse({'status' : False, 'messages': 'Invalid Coupon'})
        
        if cart.coupon :
            return JsonResponse({'status' : False, 'messages': 'Coupon Already Exists'})

        if cart.get_cart_total(login_type) < coupon_obj[0].minimum_amount:
            return JsonResponse({'status' : False, 'messages': f'Total amount should be grater than {coupon_obj[0].minimum_amount}'})
        
        if coupon_obj[0].is_expired:
            return JsonResponse({'status' : False, 'messages': 'Your coupon is expired'})

        cart.coupon = coupon_obj[0]
        cart.save()
    
   
        cart_total_price = cart.get_cart_total(login_type)

        return JsonResponse({
            'status': True, 
            'coupon_name': coupon,
            'coupon_discount_price' : cart.coupon.discount_price,
            'cart_total_price' : cart_total_price,
            'home_delivery_charge' : request.user.profile.login_type.home_delivery_price,
            'messages': 'Coupon Applied Successfully'
            })
    
        



@login_required
def remove_coupon_ajax(request):
    cart_uid = request.GET.get('cart_uid')
    cart = Cart.objects.get(uid = cart_uid)
    cart.coupon = None
    cart.save()
    login_type = request.user.profile.login_type.name
    cart_total_price = cart.get_cart_total(login_type)
   
    return JsonResponse({
        'status' : True, 
        'messages' : 'Coupon Removed Successfully' ,
        'cart_total_price' : cart_total_price,
        'home_delivery_charge' : request.user.profile.login_type.home_delivery_price,
        })

def remove_coupon(request, cart_uid):
    cart = Cart.objects.get(uid = cart_uid)
    cart.coupon = None
    cart.save()
    messages.warning(request, "Coupon Removed Succesfully")
    return HttpResponseRedirect(request.path_info)

def get_all_prices_ajax(request):
    cart = Cart.objects.get(user = request.user)
    login_type = request.user.profile.login_type.name
    return JsonResponse({
        'status' : True,
        'cart_total_price' : cart.get_cart_total(login_type),
        'home_delivery_charge' : request.user.profile.login_type.home_delivery_price,
    })


def place_order(request):
    selected_adrss_uid = request.GET.get('selected_adrss_uid')
    login_type = request.user.profile.login_type.name
    cart = Cart.objects.get(user = request.user)
    cart_items = CartItems.objects.filter(cart = cart)

    items_subtotal = cart.get_cart_books_total(login_type)
    discount_price = 0
    if cart.coupon:
        discount_price = cart.coupon.discount_price
    tax_amount = 0
 
    shipping_charge = 0
    delivery_type = ''
    login_type = request.user.profile.login_type.name
    try:
        # home delivery
        ship_a = Address.objects.get(uid = selected_adrss_uid)
        shipping_charge = request.user.profile.login_type.home_delivery_price
        delivery_type = 'home'
    except Exception as e:
        # pickup point 
        ship_a = Dealer_Address.objects.get(uid = selected_adrss_uid)
        shipping_charge = 0
        delivery_type = 'pickup'

    try:
        bill_a = Address.objects.get(user = request.user, is_default = True)
    except Exception as e:
        bill_a = None

    total_amount = cart.get_cart_total(login_type) + shipping_charge + tax_amount

    order = Order.objects.create(user = request.user)
    
    
    if cart.coupon:
        order_coupon, _ = Order_Coupon.objects.get_or_create(
            coupon_code = cart.coupon.coupon_code,
            is_expired = cart.coupon.is_expired,
            discount_price = cart.coupon.discount_price,
            minimum_amount = cart.coupon.minimum_amount
        )
        order.coupon = order_coupon
    
    # for payment details
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    razorpay_order_id = request.GET.get('razorpay_order_id')
    razorpay_signature = request.GET.get('razorpay_signature')
    order.razorpay_payment_id = razorpay_payment_id
    order.razorpay_order_id = razorpay_order_id
    order.razorpay_signature = razorpay_signature

    order.delivery_type = delivery_type
    order.membership_type = request.user.profile.login_type.name

    order.shipping_charge = shipping_charge
    order.cart_uid = cart.uid

    if delivery_type == 'home':
        order.shipping_address = ship_a.adss2 +", "+ ship_a.adss1 +", "+ ship_a.area +", "+ ship_a.city +", "+ ship_a.state +", "+ ship_a.pincode
    elif(delivery_type == 'pickup'):
        order.shipping_address = ship_a.adss2 +", "+ ship_a.adss1 +", "+ ship_a.area +", "+ ship_a.city +", "+ ship_a.state +", "+ ship_a.pincode
        dealer_addrss = Dealer_Address.objects.get(uid = selected_adrss_uid)
        order.dealer = dealer_addrss.dealer

    order.save()
    
    for item in cart_items:
        order_product = Order_Product.objects.get(uid = item.product.secondery_uid)
        OrderItems.objects.create(order = order, product = order_product, quantity = item.quantity)

    
    cart_items.delete()
    cart.delete()

    messages.success(request, "Order Placed Succesfully")
    return redirect('/accounts/show-orders/')


def payment_failure(request):
    description = request.GET.get('description')
    source = request.GET.get('source')
    reason = request.GET.get('reason')
    context = {
        'description' : description,
        'source' : source,
        'reason' : reason
    }
    return render(request, 'accounts/payment_failure.html', context)



def download_invoice(request, order_uid):
    try : 
        order = Order.objects.get(uid = order_uid)
        file_path = settings.MEDIA_ROOT + "/invoices/" + order.invoive_no + ".pdf"
        response = FileResponse(open(file_path, "rb"), as_attachment=True)
        return response
    except Exception as e:
        return redirect('/error')



def show_orders(request):
    all_orders = Order.objects.filter(user = request.user).order_by('-order_date')
    context = {'all_orders' : all_orders}
    return render(request, 'accounts/show_orders.html', context)

def show_order_items(request, order_uid):
    order = Order.objects.get(uid = order_uid)
    all_items = OrderItems.objects.filter(order = order)
    login_type = request.user.profile.login_type.name

    ship_a = None

    if order.delivery_type == 'home':
        ship_a = order.shipping_address
    elif(order.delivery_type == 'pickup') :
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
        'bill_a' : order.billing_address,
        'delivery_type' : order.delivery_type,
        'items_subtotal' : items_subtotal,
        'discount_price' : discount_price,
        'shipping_charge' : shipping_charge,
        'tax_amount' : tax_amount,
        'total_amount' : total_amount,
    }

    return render(request, 'accounts/show_order_items.html', context)

@is_user_normal() 
def membershipPlans(request):

    if request.method == "POST":
        if not request.user.is_authenticated:
            current_url = request.build_absolute_uri()
            messages.warning(request, "You need to Login Here to buy membership")
            return redirect(f'/accounts/login?next={current_url}')
        radio_value = request.POST.get('membership-radio-group') 
        substring_list = radio_value.split("-")
        membership = MembershipType.objects.get(name = substring_list[0])

        try:
            membership_prices_obj = Membership_Plan_Prices.objects.get(membership_name = membership)
            if substring_list[1] == 'year':
                end_date = datetime.now() + timedelta(days=365)
                fees = membership_prices_obj.yearly
            elif substring_list[1] == 'six_months':
                end_date = datetime.now() + timedelta(days=183)
                fees = membership_prices_obj.six_months
            elif substring_list[1] == 'three_months':
                end_date = datetime.now() + timedelta(days=92)
                fees = membership_prices_obj.three_months
            else:
                messages.warning(request, "Select Valid Option")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Exception as e:
            messages.warning(request, "Select Valid Option")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
        payment = client.order.create({'amount' : fees*100, 'currency' : 'INR', 'payment_capture' : 1  })
            
        prime_plan = MembershipType.objects.get(name = 'prime')
        prime_plan_prices = Membership_Plan_Prices.objects.get(membership_name = prime_plan)
        dealer_plan = MembershipType.objects.get(name = 'dealer')
        dealer_plan_prices = Membership_Plan_Prices.objects.get(membership_name = dealer_plan)
        context = {
            'prime_plan_prices' : prime_plan_prices,
            'dealer_plan_prices' : dealer_plan_prices,
            'payment_mode' : True,
            'membership_name' : membership.name,
            'membership_time' : substring_list[1],
            'payment' : payment
        }
        return render(request, 'accounts/membership_plans.html', context)
 
    prime_plan = MembershipType.objects.get(name = 'prime')
    prime_plan_prices = Membership_Plan_Prices.objects.get(membership_name = prime_plan)

    dealer_plan = MembershipType.objects.get(name = 'dealer')
    dealer_plan_prices = None
    if dealer_plan.is_active:
        dealer_plan_prices = Membership_Plan_Prices.objects.get(membership_name = dealer_plan)

    context = {
        'prime_plan_prices' : prime_plan_prices,
        'dealer_plan_prices' : dealer_plan_prices,
        'payment_mode' : False
    }

    return render(request, 'accounts/membership_plans.html', context)




def payment_prime_membership(request):

    membership_name = request.GET.get('membership_name')
    membership_time = request.GET.get('membership_time')
    

    membership = MembershipType.objects.get(name = membership_name)

    user_obj = request.user
    profile_obj = user_obj.profile
    profile_obj.login_type = membership
    profile_obj.save()

    membership_prices_obj = Membership_Plan_Prices.objects.get(membership_name = membership)
    if membership_time == 'year':
        end_date = datetime.now() + timedelta(days=365)
        fees = membership_prices_obj.yearly
    elif membership_time == 'six_months':
        end_date = datetime.now() + timedelta(days=183)
        fees = membership_prices_obj.six_months
    elif membership_time == 'three_months':
        end_date = datetime.now() + timedelta(days=92)
        fees = membership_prices_obj.three_months

    membership_details = Membership_Details.objects.create(membership = membership, user = user_obj, end_date = end_date, fees = fees, duration = membership_time)
    # for payment details
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    razorpay_order_id = request.GET.get('razorpay_order_id')
    razorpay_signature = request.GET.get('razorpay_signature')
    membership_details.razorpay_payment_id = razorpay_payment_id
    membership_details.razorpay_order_id = razorpay_order_id
    membership_details.razorpay_signature = razorpay_signature
    membership_details.save()

    messages.success(request, f"You are {membership_name} member now")
    messages.success(request, "Search for books youn want to buy")
    return redirect('/search/')


