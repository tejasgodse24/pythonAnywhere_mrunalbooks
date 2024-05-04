from django.contrib import admin
from dealer.models import *


class DealerAdminArea(admin.AdminSite):
    site_header = "Dealer Admin Area"

dealer_site = DealerAdminArea(name = "dealerAdmin")


class Dealer_Address_Admin(admin.ModelAdmin):
    list_display = ['shop_name', 'dealer', 'area', 'city', 'pincode']

class DealerAdmin(admin.ModelAdmin):
    list_display = ['fname', 'lname', 'phone']
    search_fields = ['fname', 'lname']


# Register your models here.
admin.site.register(Dealer, DealerAdmin)
admin.site.register(Dealer_Address, Dealer_Address_Admin)


dealer_site.register(Dealer, DealerAdmin)
dealer_site.register(Dealer_Address, Dealer_Address_Admin)

