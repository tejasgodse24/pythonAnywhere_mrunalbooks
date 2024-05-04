from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from products.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product, Coupon
from dealer.models import Dealer
from custom_admin.models import Courier


# Create your models here.

class MembershipType(BaseModel):
    name = models.CharField(max_length=50)
    discount_percent = models.IntegerField()
    home_delivery_price = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default = True, null=True, blank=True)

    def __str__(self):
        return self.name

class Membership_Details(BaseModel):
    membership = models.ForeignKey(MembershipType, on_delete = models.CASCADE, related_name='membership_details')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_membership_details')
    start_date = models.DateField(auto_now_add = True)
    end_date = models.DateField()
    fees = models.IntegerField()
    duration = models.CharField(max_length = 20)
    is_active = models.BooleanField(default = True, null=True, blank=True)
    
    razorpay_order_id = models.CharField(max_length=100, null = True, blank = True)
    razorpay_payment_id = models.CharField(max_length=100, null = True, blank = True)
    razorpay_signature = models.CharField(max_length=100, null = True, blank = True)

    def __str__(self):
        return self.user.username

    

class Membership_Plan_Prices(BaseModel):
    membership_name = models.OneToOneField(MembershipType, on_delete=models.CASCADE, related_name='membership_prices')
    yearly = models.IntegerField()
    six_months = models.IntegerField()
    three_months = models.IntegerField()

    def __str__(self):
        return self.membership_name.name


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    mobile_number = models.CharField(max_length=10, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    login_type = models.ForeignKey(MembershipType, on_delete=models.CASCADE, null=True, blank=True)
    forgot_password_token = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    def get_cart_count(self):
        items_count = []
        all_cart_items = CartItems.objects.filter(cart__user = self.user)
        
        for cart_item in all_cart_items :
            items_count.append(cart_item.quantity)
        return sum(items_count)
    
    def get_wishlist_count(self):
        wishlist_items = WishListItems.objects.filter(wishlist__user = self.user)
        return len(wishlist_items)
    

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_cart_total(self, login_type):
        if login_type == 'prime':
            return self.get_cart_total_prime()
        elif login_type == 'dealer':
            return self.get_cart_total_dealer()
        
        return self.get_cart_total_normal()
    
    def get_cart_total_normal(self): #for normal members
        cart_items = self.cart_items.all()
        price = []
        for item in cart_items:
            price.append(item.product.normal_price * item.quantity)

        total_pay = sum(price)

        if self.coupon:
            if total_pay > self.coupon.minimum_amount:
                total_pay =  total_pay - self.coupon.discount_price
        return total_pay
    
    def get_cart_total_prime(self): #for prime members
        cart_items = self.cart_items.all()
        price = []
        for item in cart_items:
            price.append(item.product.prime_price * item.quantity)

        total_pay = sum(price)

        if self.coupon:
            if total_pay > self.coupon.minimum_amount:
                total_pay =  total_pay - self.coupon.discount_price
        return total_pay
    
    def get_cart_total_dealer(self): #for dealer members
        cart_items = self.cart_items.all()
        price = []
        for item in cart_items:
            price.append(item.product.dealer_price * item.quantity)

        total_pay = sum(price)

        if self.coupon:
            if total_pay > self.coupon.minimum_amount:
                total_pay =  total_pay - self.coupon.discount_price
        return total_pay
    
    def get_cart_books_total(self, login_type):
        if login_type == 'prime':
            return self.get_cart_books_total_prime()
        elif login_type == 'dealer':
            return self.get_cart_books_total_dealer()
        
        return self.get_cart_books_total_normal()
    
    def get_cart_books_total_normal(self):
        cart_items = self.cart_items.all()
        price = []
        for item in cart_items:
            price.append(item.product.normal_price * item.quantity)
        return sum(price)
    
    def get_cart_books_total_prime(self):
        cart_items = self.cart_items.all()
        price = []
        for item in cart_items:
            price.append(item.product.prime_price * item.quantity)
        return sum(price)
    
    def get_cart_books_total_dealer(self):
        cart_items = self.cart_items.all()
        price = []
        for item in cart_items:
            price.append(item.product.dealer_price * item.quantity)
        return sum(price)
    
 


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)





class WishList(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    def __str__(self):
        return self.user.username
    

class WishListItems(BaseModel):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addressess')
    name = models.CharField(max_length = 50)
    pincode = models.CharField(max_length = 6)
    area = models.CharField(max_length = 100)
    adss1 =  models.CharField(max_length = 1000)
    adss2 =  models.CharField(max_length = 1000)
    adss3 =  models.CharField(max_length = 1000, null=True, blank=True)
    city = models.CharField(max_length = 100)
    state =  models.CharField(max_length = 100)
    phone =  models.CharField(max_length=10)
    is_default = models.BooleanField(default = False)





class Order_Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)

    def __str__(self):
        return self.coupon_code




class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    cart_uid = models.UUIDField(null=True, blank=True)
    is_accepted = models.BooleanField(null=True, blank=True, default = None)
    is_delivered = models.BooleanField(default = False)
    is_shipped = models.BooleanField(default = False)
    invoive_no = models.CharField(editable=False, max_length=50)
    order_no = models.CharField(editable=False, max_length=50)
    invoice_date = models.DateTimeField(auto_now_add=True) 
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_type = models.CharField(max_length=20, null=True, blank=True)
    membership_type = models.CharField(max_length=20, null=True, blank=True)
    coupon = models.ForeignKey(Order_Coupon, on_delete=models.SET_NULL, null=True, blank=True)
   
    billing_address = models.CharField(max_length=1000, null=True, blank=True)
    shipping_address = models.CharField(max_length=1000, null=True, blank=True)

    dealer = models.ForeignKey(Dealer, on_delete=models.SET_NULL, related_name='dealer_orders', null=True, blank=True)
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, related_name='courier_orders', null=True, blank=True)

    shipping_charge = models.IntegerField(default=0)

    razorpay_order_id = models.CharField(max_length=100, null = True, blank = True)
    razorpay_payment_id = models.CharField(max_length=100, null = True, blank = True)
    razorpay_signature = models.CharField(max_length=100, null = True, blank = True)


    def get_orderItems_count(self):
        items_count = []
        all_oder_items = OrderItems.objects.filter(order__user = self.user)

        for item in all_oder_items:
            items_count.append(item.quantity)
        return sum(items_count)
    
    
    def get_order_total(self, login_type):
        if login_type == 'prime':
            return self.get_order_total_prime()
        elif login_type == 'dealer':
            return self.get_order_total_dealer()
        
        return self.get_order_total_normal()
    
    def get_order_total_normal(self): #for normal members
        order_items = self.order_items.all()
        price = []
        for item in order_items:
            price.append(item.product.normal_price * item.quantity)

        total_pay = sum(price)

        if self.coupon:
            if total_pay > self.coupon.minimum_amount:
                total_pay =  total_pay - self.coupon.discount_price
        return total_pay
    
    def get_order_total_prime(self): #for prime members
        order_items = self.order_items.all()
        price = []
        for item in order_items:
            price.append(item.product.prime_price * item.quantity)

        total_pay = sum(price)

        if self.coupon:
            if total_pay > self.coupon.minimum_amount:
                total_pay =  total_pay - self.coupon.discount_price
        return total_pay
    
    def get_order_total_dealer(self): #for dealer members
        order_items = self.order_items.all()
        price = []
        for item in order_items:
            price.append(item.product.dealer_price * item.quantity)

        total_pay = sum(price)

        if self.coupon:
            if total_pay > self.coupon.minimum_amount:
                total_pay =  total_pay - self.coupon.discount_price
        return total_pay
    
    def get_items_subtotal(self, login_type):
        if login_type == 'prime':
            return self.get_items_subtotal_prime()
        elif login_type == 'dealer':
            return self.get_items_subtotal_dealer()
        
        return self.get_items_subtotal_normal()

    def get_items_subtotal_normal(self):
        all_order_items = OrderItems.objects.filter(order__uid = self.uid)
        item_subtotal = []
        for item in all_order_items:
            item_subtotal.append(item.product.normal_price * item.quantity)
        total = sum(item_subtotal)
        return total
    
    def get_items_subtotal_prime(self):
        all_order_items = OrderItems.objects.filter(order__uid = self.uid)
        item_subtotal = []
        for item in all_order_items:
            item_subtotal.append(item.product.prime_price * item.quantity)
        total = sum(item_subtotal)
        return total
    
    def get_items_subtotal_dealer(self):
        all_order_items = OrderItems.objects.filter(order__uid = self.uid)
        item_subtotal = []
        for item in all_order_items:
            item_subtotal.append(item.product.dealer_price * item.quantity)
        total = sum(item_subtotal)
        return total

    def generate_order_number(self):
        prefix = "ORD"
        return f"{prefix}-{self.uid}"
    
    def generate_invoice_number(self):
        prefix = "INV"
        return f"{prefix}-{self.uid}"
    
    def save(self, *args, **kwargs):
        self.invoive_no = self.generate_invoice_number()
        self.order_no = self.generate_order_number()
        super().save(*args, **kwargs)



class Order_Product(BaseModel):
    title = models.CharField(max_length=1000)
    slug = models.SlugField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author_order_products',null=True, blank=True)
    publication_id = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='publication_order_products')
    image = models.ImageField()

    weight = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length = 50, null=True, blank=True)

    prod_code_1 = models.CharField(max_length = 50, null=True, blank=True)
    prod_code_2 = models.CharField(max_length = 50, null=True, blank=True)

    # prices 
    mrp = models.IntegerField()

    normal_price = models.IntegerField()
    normal_discount_percenatage = models.IntegerField()

    prime_price = models.IntegerField()
    prime_discount_percenatage = models.IntegerField()

    dealer_price = models.IntegerField()
    dealer_discount_percenatage = models.IntegerField()

    def __str__(self):
        return self.title


    
class OrderItems(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Order_Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)


