from django.shortcuts import render, redirect
from django.db.models import Q
from products.models import Publication, Product
from accounts.models import *
from products.models import *
import uuid
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from base.emails import send_contact_email


from django.conf import settings

# Create your views here.

def index(request):

    publications = Publication.objects.all()
    products = Product.objects.all()

    try : 
        wishlist = WishList.objects.get(user = request.user)
        user_wishlist_product_uids = wishlist.wishlist_items.all().values_list('product', flat=True) 
    except Exception as e:
        user_wishlist_product_uids = []

    
    categories = Category.objects.all()

    context = {
        'publications' : publications, 
        'products' : products, 
        'user_wishlist_product_uids' : user_wishlist_product_uids,
        'categories' : categories,
        }
    return render(request, 'home/index.html', context)

def about(request):
    return render(request, 'home/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if subject and message and email:
            send_contact_email.delay(name=name, email=email, phone=phone, subject=subject, message=message)
            messages.success(request, "Message Sent Succesfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'home/contact.html')

def search(request):
    if request.method == "POST":
        search_query = request.POST.get('search_query')
        return redirect('/search-results/' + search_query)
    return render(request, 'home/search.html')


def get_search_suggestions_ajax(request):
    search = request.GET.get('search')
    payload = []
    if search:

        objs = Product.objects.filter(
            Q(title__icontains = search) |
            Q(author__name__icontains = search) |
            Q(isbn__icontains = search) |
            Q(publication_id__name__icontains = search) |
            Q(categories__name__icontains = search) |
            Q(subcategories__name__icontains = search)
            ).distinct()
        for obj in objs:
            payload.append({'title' : obj.title})

    return JsonResponse({
        'status' : True, 
        'payload' : payload
    })

def search_result(request, search_query):
    objs = Product.objects.filter(
            Q(title__icontains = search_query) |
            Q(author__name__icontains = search_query) |
            Q(isbn__icontains = search_query) |
            Q(publication_id__name__icontains = search_query) |
            Q(categories__name__icontains = search_query) |
            Q(subcategories__name__icontains = search_query)
            ).distinct()
    
    try :
        wishlist = WishList.objects.get(user = request.user)
    except Exception as e:
        wishlist = None
    
    try :
        user_wishlist_product_uids = wishlist.wishlist_items.all().values_list('product', flat=True) 
    except Exception as e:
        user_wishlist_product_uids = None 
    
    context = {
        'books' : objs,
        'user_wishlist_product_uids' : user_wishlist_product_uids
    }
    return render(request, 'home/search_results.html', context)


def get_author_books(request, slug):
    books = Product.objects.filter(author__slug = slug)

    try :
        wishlist = WishList.objects.get(user = request.user)
    except Exception as e:
        wishlist = None
    
    try :
        user_wishlist_product_uids = wishlist.wishlist_items.all().values_list('product', flat=True) 
    except Exception as e:
        user_wishlist_product_uids = None

    context = {
        'books' : books,
        'user_wishlist_product_uids' : user_wishlist_product_uids,
        'heading' : books[0].author
    }
    return render(request, 'home/books.html', context)



def get_category_books(request, slug):
    books = Product.objects.filter(categories__slug = slug)

    try :
        wishlist = WishList.objects.get(user = request.user)
    except Exception as e:
        wishlist = None
    
    try :
        user_wishlist_product_uids = wishlist.wishlist_items.all().values_list('product', flat=True) 
    except Exception as e:
        user_wishlist_product_uids = None

    context = {
        'books' : books,
        'user_wishlist_product_uids' : user_wishlist_product_uids,
        'heading' : books[0].categories.first()
    }
    return render(request, 'home/books.html', context)



def get_subcategory_books(request, slug):
    books = Product.objects.filter(subcategories__slug = slug)

    try :
        wishlist = WishList.objects.get(user = request.user)
    except Exception as e:
        wishlist = None
    
    try :
        user_wishlist_product_uids = wishlist.wishlist_items.all().values_list('product', flat=True) 
    except Exception as e:
        user_wishlist_product_uids = None

    context = {
        'books' : books,
        'user_wishlist_product_uids' : user_wishlist_product_uids,
        'heading' : SubCategory.objects.get(slug = slug).name
    }
    return render(request, 'home/books.html', context)



def get_publication_books(request, slug):
    books = Product.objects.filter(publication_id__slug = slug)

    try :
        wishlist = WishList.objects.get(user = request.user)
    except Exception as e:
        wishlist = None
    
    try :
        user_wishlist_product_uids = wishlist.wishlist_items.all().values_list('product', flat=True) 
    except Exception as e:
        user_wishlist_product_uids = None

    context = {
        'books' : books,
        'user_wishlist_product_uids' : user_wishlist_product_uids
    }
    return render(request, 'home/books.html', context)

# error handling
def page_not_found(request, exception):
    return render(request, 'base/error-404.html')

# policies
def terms_and_conditions(request):
    return render(request, 'policies/terms_and_conditions.html')
def privacy_policy(request):
    return render(request, 'policies/privacy_policy.html')
def refund_policy(request):
    return render(request, 'policies/refund_policy.html')
def shipping_policy(request):
    return render(request, 'policies/shipping_policy.html')



