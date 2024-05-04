from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from products.models import *
from .models import Publication, Category, SubCategory, Author, Product, Coupon


class ProductAdminArea(admin.AdminSite):
    site_header = "Product Admin Area"
product_site = ProductAdminArea(name = "productAdmin")


class CouponAdminArea(admin.AdminSite):
    site_header = "Coupon Admin Area"
coupon_site = CouponAdminArea(name = "Coupon_Admin")


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class Media:
        js = ['/media/admin/product.js']

    list_display = ['title', 'author', 'publication_id']
    # list_filter = ['publication_id', 'author']
    fieldsets = [
        ('Main Information', {
            'fields': ('title', 'author', 'isbn', 'publication_year', 'publication_id', 'categories', 'subcategories', 'image', 'weight', 'language', 'prod_code_1', 'prod_code_2')
        }),
        ('Prices Information', {
            'fields': ('mrp',
                       ( 'normal_price', 'normal_discount_percenatage'),
                       ( 'prime_price', 'prime_discount_percenatage'),
                       ( 'dealer_price', 'dealer_discount_percenatage'),
                       )
        }),
    ]

    filter_horizontal = ['categories', 'subcategories',]
    exclude = ['slug']

    # this is to display search bar to select publications
    autocomplete_fields = ['publication_id', 'author']
    # this is to display search bar to select products in product table
    search_fields = ['title', 'language', 'prod_code_1', 'prod_code_2']

class PublicationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    # this is to display search bar to select publications in product table
    search_fields = ['name']
    exclude = ['slug']
    def has_delete_permission(self, request, obj = None):
        return False

class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['name']
    exclude = ['slug']

class SubCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['name']
    exclude = ['slug']

class AuthorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['name']
    exclude = ['slug']
    def has_delete_permission(self, request, obj = None):
        return False



class CouponAdminPermissions(admin.ModelAdmin):
    def has_delete_permission(self, request, obj = None):
        return False
    


# Register your models here.
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Coupon, CouponAdminPermissions)


# product site
product_site.register(Publication, PublicationAdmin)
product_site.register(Product, ProductAdmin)
product_site.register(Category, CategoryAdmin)
product_site.register(SubCategory, SubCategoryAdmin)
product_site.register(Author, AuthorAdmin)

coupon_site.register(Coupon, CouponAdminPermissions)



