from django.contrib import admin
from custom_admin.models import *

# Register your models here.

class CourierAdminArea(admin.AdminSite):
    site_header = "Courier Admin Area"

courier_site = CourierAdminArea(name = "Courier_Admin")

# Register your models here.
admin.site.register(Courier)
courier_site.register(Courier)
