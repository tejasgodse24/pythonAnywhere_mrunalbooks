from django.shortcuts import render
from products.models import Product
from accounts.models import Cart, CartItems, WishListItems
from django.db.models import Q


# Create your views here.

def get_product(request, slug):
    product = Product.objects.get(slug=slug)
    try : 
        cart_item = CartItems.objects.filter(cart__user = request.user, product = product)[0]

    except Exception as e:
        cart_item  = None
        
    try : 
        wishlist_item = WishListItems.objects.filter(wishlist__user = request.user, product = product)[0]
    except Exception as e:
        wishlist_item  = None


    reccomended_books = Product.objects.filter(
            Q(categories__in  = product.categories.all())|
            Q(subcategories__in = product.subcategories.all())
            ).exclude(uid = product.uid).distinct()
 
        
    
    context = {
        'book' : product, 
        'cart_item' : cart_item, 
        'wishlist_item' : wishlist_item,
        'reccomended_books' : reccomended_books}
    
    return render(request, 'products/product.html', context)

