"""
URL configuration.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import ( 
    home, 
    login, 
    register, 
    otp, 
    create_product
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    # TEMPLATE URL
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('otp/', otp, name='otp'),
    path('create_product/', create_product, name='create_product'),

    # API URLS
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/wallet/', include('wallet.urls')),
    path('api/chat/', include('chat.urls'))   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)