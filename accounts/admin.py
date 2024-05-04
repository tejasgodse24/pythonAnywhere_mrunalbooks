from django.contrib import admin
from .models import *


class memberShipAdminArea(admin.AdminSite):
    site_header = "Membership Admin Area"
membership_site = memberShipAdminArea(name = "memberShipAdmin")


# function to don't allow to change or delete normal membership type
class MembershipAdminPermissions(admin.ModelAdmin):
    readonly_fields = ('name',)
    def has_delete_permission(self, request, obj = None):
        # return obj is None or obj.name != 'normal'
        return False

    def has_change_permission(self, request, obj = None):
        return obj is None or obj.name != 'normal'
    


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_email_verified']

class Membership_Plan_Prices_Admin(admin.ModelAdmin):
    readonly_fields = ('membership_name',)
    def has_delete_permission(self, request, obj = None):
        # return obj is None or obj.name != 'normal'
        return False


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CartItems)
admin.site.register(Cart)
admin.site.register(WishListItems)
admin.site.register(WishList)
admin.site.register(MembershipType, MembershipAdminPermissions)

admin.site.register(Address)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems)
admin.site.register(Membership_Plan_Prices, Membership_Plan_Prices_Admin)

admin.site.register(Order_Product)
admin.site.register(Membership_Details)
admin.site.register(Order_Coupon)


membership_site.register(MembershipType, MembershipAdminPermissions)
membership_site.register(Membership_Plan_Prices, Membership_Plan_Prices_Admin)



