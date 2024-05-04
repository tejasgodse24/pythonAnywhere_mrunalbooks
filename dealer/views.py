from django.shortcuts import render
from dealer.models import *
from django.http import JsonResponse
from django.db.models import Q



def dealer_login(request):
    return render(request, 'dealer/dealer.html')


def dealer_register(request):
    return render(request, 'dealer/register.html')

def get_dealer_names_ajax(request):
    search = request.GET.get('search')
    payload = []
    if search:
        objs = Dealer_Address.objects.filter(
            Q(name__icontains = search) |
            Q(shop_name__icontains = search) |
            Q(pincode__icontains = search) |
            Q(area__icontains = search) |
            Q(adss1__icontains = search) |
            Q(city__icontains = search) 
            )

        for obj in objs:
            payload.append({
                'name' : obj.name, 
                'shop_name' : obj.shop_name,
                'pincode' : obj.pincode,
                'area' : obj.area, 
                'adss1' : obj.adss1,
                'adss2' : obj.adss2,
                'adss3' : obj.adss3,
                'city'  : obj.city,
                'state' : obj.state,
                'uid' : obj.uid
                })
    
    return JsonResponse({
        'status' : True, 
        'payload' : payload
    })
