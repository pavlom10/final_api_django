# TODO:
#  фильтр по магазину / категории
#  добавить продукт в корзину по id
#  удалить продукт из корзины по id
#  получить корзину
#  получить мои заказы

from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import ProductInfo
from products.serializers import ProductInfoSerializer
# from .filters import ProductInfoFilter


class ProductInfoView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = ProductInfo.objects.all().select_related(
            'shop', 'product__category').prefetch_related(
            'product_parameters__parameter').distinct()
        serializer = ProductInfoSerializer(queryset, many=True)

        return Response(serializer.data)


class CardView(APIView):
    pass
