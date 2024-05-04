from django.contrib import admin
from django.urls import path

from home.views import *

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    path('search/', search, name='search'),
    path('get-search-suggestions/', get_search_suggestions_ajax, name='get_search_suggestions_ajax'),
    path('search-results/<str:search_query>', search_result, name='search_result'),

    path('author/<slug>', get_author_books, name='author_books'),
    path('categories/<slug>', get_category_books, name='category_books'),
    path('subcategories/<slug>', get_subcategory_books, name='subcategory_books'),
    path('publication/<slug>', get_publication_books, name='publication_books'),

    path('error', page_not_found, name='page_not_found'),
    # policies
    path('terms-and-conditions', terms_and_conditions, name='terms_and_conditions'),
    path('privacy-policy', privacy_policy, name='privacy_policy'),
    path('refund-policy', refund_policy, name='refund_policy'),
    path('shipping-policy', shipping_policy, name='shipping_policy'),



    





 

]
