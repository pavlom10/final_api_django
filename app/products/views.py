from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.core.validators import URLValidator
from django.db.models import Q, Sum, F
from requests import get
from distutils.util import strtobool
from shops.permissions import IsOwnerOrAdmin, IsShopOrAdmin
from shops.models import Shop
from shops.serializers import ShopSerializer
from orders.models import Order
from orders.serializers import OrderSerializer
from yaml import load as load_yaml, Loader
from .models import Category, Product, ProductParameter, ProductInfo, Parameter
from .serializers import CategorySerializer


# from rest_framework import generics
# from django.core.validators import URLValidator
# from .serializers import ShopSerializer
# from .models import Product
# from django.shortcuts import render
# from django.http import JsonResponse
# from requests import get
# from rest_framework.authtoken.models import Token
# from rest_framework.generics import ListAPIView


class PartnerUpdate(APIView):

    permission_classes = [permissions.IsAuthenticated, IsShopOrAdmin]

    def post(self, request, *args, **kwargs):
        url = request.data.get('url')

        if not url:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        validate_url = URLValidator()
        try:
            validate_url(url)
        except Exception as e:
            return Response({'Status': False, 'Error': str(e)})

        stream = get(url).content
        data = load_yaml(stream, Loader=Loader)

        shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)

        for category in data['categories']:
            category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
            category_object.shops.add(shop.id)
            category_object.save()
        ProductInfo.objects.filter(shop_id=shop.id).delete()
        for item in data['goods']:
            product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

            product_info = ProductInfo.objects.create(product_id=product.id,
                                                      external_id=item['id'],
                                                      model=item['model'],
                                                      price=item['price'],
                                                      price_rrc=item['price_rrc'],
                                                      quantity=item['quantity'],
                                                      shop_id=shop.id)
            for name, value in item['parameters'].items():
                parameter_object, _ = Parameter.objects.get_or_create(name=name)
                ProductParameter.objects.create(product_info_id=product_info.id,
                                                parameter_id=parameter_object.id,
                                                value=value)

        return Response(status=status.HTTP_200_OK)


class PartnerState(APIView):
    permission_classes = [permissions.IsAuthenticated, IsShopOrAdmin]

    def get(self, request, *args, **kwargs):
        shop = request.user.shop
        serializer = ShopSerializer(shop)
        return Response({'state': 'on' if serializer.data['state'] else 'off'})

    def post(self, request, *args, **kwargs):
        state = request.data.get('state')
        if not state:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        Shop.objects.filter(user_id=request.user.id).update(state=strtobool(state))
        return Response(status=status.HTTP_200_OK)


class PartnerOrders(APIView):
    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(
            ordered_items__product_info__shop__user_id=request.user.id).exclude(state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
