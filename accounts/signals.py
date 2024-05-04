# django signals
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from accounts.models import *
from django.db.models.signals import  post_delete, post_save, pre_save
from datetime import datetime
from base.helpers import save_invoice_pdf
from base.emails import send_order_placed_thankyou_email
from copy import deepcopy
import uuid

# @receiver(user_logged_in)
# def check_membership_status(sender, user, **kwargs):
#     if not user.is_superuser:
#         if user.profile.login_type.name != 'normal':
#             mem_details = user.user_membership_details.get(is_active = True)
          
#             if mem_details.end_date < datetime.now().date():
#                 mem_details.is_active = False
#                 profile_obj = user.profile
#                 normal_membership = MembershipType.objects.get(name = 'normal')
#                 profile_obj.login_type = normal_membership
#                 mem_details.save()
#                 profile_obj.save()
    
   
@receiver(post_delete, sender = Cart)
def save_invoice_send_thankyou(sender, instance, using, **kwargs):
    try : 
        order = Order.objects.get(cart_uid = instance.uid)
        order_items = order.order_items.order_by('product')
        login_type = order.membership_type
        discount_price = 0
        if order.coupon:
            discount_price = order.coupon.discount_price
        shipping_charge = order.shipping_charge
        tax_amount = 0
        total_amount = order.get_order_total(login_type) + shipping_charge + tax_amount
        
        params = {
            'user_name' : order.user.first_name + " " + order.user.last_name,
            'order' : order,
            'bil_a' : order.billing_address,
            'ship_a' : order.shipping_address,
            'delivery_type':order.delivery_type,
            'order_items' : order_items,
            'items_subtotal' : order.get_items_subtotal(login_type),
            'discount_price' : discount_price,
            'shipping_charge' : shipping_charge,
            'tax_amount' : tax_amount,
            'total_amount' : total_amount,
            'invoive_no' : order.invoive_no,
            'order_no' : order.order_no,
            'invoice_date' : order.invoice_date.date(),
            'order_date' : order.order_date.date()
        }
    
        file_name , status = save_invoice_pdf(params, order.invoive_no)
        email = order.user.email
        send_order_placed_thankyou_email.delay(email)
    except Exception as e:
        ...                

# If admin changes any product then its before stages also should store in another table for 
# users who had buoght it before change 
@receiver(pre_save, sender=Product)
def product_save_before(sender, instance, **kwargs):
    try:
        Product.objects.get(uid = instance.uid)
        instance.secondery_uid = uuid.uuid4()
    except Exception as e:
        instance.secondery_uid = instance.uid

@receiver(post_save, sender=Product)
def product_save(sender, instance, created, **kwargs):
    order_product_obj = Order_Product.objects.create(
        uid = instance.secondery_uid,
        title = instance.title, 
        slug = instance.slug,
        author = instance.author,
        publication_id = instance.publication_id,
        image = instance.image,
        weight = instance.weight,
        language = instance.language,
        prod_code_1 = instance.prod_code_1,
        prod_code_2 = instance.prod_code_2,
        mrp = instance.mrp,
        normal_price = instance.normal_price,
        normal_discount_percenatage = instance.normal_discount_percenatage,
        prime_price = instance.prime_price,
        prime_discount_percenatage = instance.prime_discount_percenatage,
        dealer_price = instance.dealer_price,
        dealer_discount_percenatage = instance.dealer_discount_percenatage
        )