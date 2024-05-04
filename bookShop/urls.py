
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin-manager-super/', admin.site.urls),
    
    path('' , include('home.urls') ),
    path('product/' , include('products.urls') ),
    path('accounts/' , include('accounts.urls') ),
    path('dealer/' , include('dealer.urls') ),

    path('custom-admin-management/', include('custom_admin.urls')),


] 


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



