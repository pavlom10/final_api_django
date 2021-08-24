"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from shops.views import ShopViewSet
from users.views import RegisterView
from products.views import PartnerUpdate, PartnerState, PartnerOrders
from orders.views import ProductInfoView, CartView, ContactViewSet

router = routers.DefaultRouter()
router.register(r'shops', ShopViewSet, basename='shops')
router.register(r'user/contacts', ContactViewSet, basename='contacts')

urlpatterns = [
    path('api/v1/register', RegisterView.as_view(), name='auth_register'),
    path('api/v1/', include(router.urls)),
    path('api/v1/partner/update', PartnerUpdate.as_view(), name='partner_update'),
    path('api/v1/products', ProductInfoView.as_view(), name='products'),
    path('api/v1/cart', CartView.as_view(), name='cart'),
    path('api/v1/partner/orders', PartnerOrders.as_view(), name='partner_orders'),
    path('admin', admin.site.urls),
]
