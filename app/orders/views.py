# TODO:
#  фильтр по магазину / категории
#  добавить продукт в корзину по id
#  удалить продукт из корзины по id
#  получить корзину
#  получить мои заказы
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import ProductInfo
from products.serializers import ProductInfoSerializer
from .models import Order, OrderItem, OrderStatusChoices
from .serializers import CartSerializer
# from .filters import ProductInfoFilter


class ProductInfoView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = ProductInfo.objects.all().select_related(
            'shop', 'product__category').prefetch_related(
            'product_parameters__parameter').distinct()
        serializer = ProductInfoSerializer(queryset, many=True)

        return Response(serializer.data)


class CartView(APIView):
    def post(self, request):
        cart, _ = Order.objects.get_or_create(user_id=request.user.id, state=OrderStatusChoices.CART)

        try:
            product = ProductInfo.objects.get(
                pk=request.data['product_id']
            )
            quantity = int(request.data['quantity'])
        except Exception as e:
            # print e
            return Response(status=status.HTTP_400_BAD_REQUEST)

        existing_cart_item = OrderItem.objects.filter(order=cart, product_info=product).first()
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
        else:
            new_cart_item = OrderItem(order=cart, product_info=product, quantity=quantity)
            new_cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)


        #
        # # # Disallow adding to cart if available inventory is not enough
        # # if product.available_inventory <= 0 or product.available_inventory - quantity < 0:
        # #     print "There is no more product available"
        # #     return Response({'status': 'fail'})
        #
        # existing_cart_item = OrderItem.objects.filter(cart=cart, product=product).first()
        # # before creating a new cart item check if it is in the cart already
        # # and if yes increase the quantity of that item
        # if existing_cart_item:
        #     existing_cart_item.quantity += quantity
        #     existing_cart_item.save()
        # else:
        #     new_cart_item = OrderItem(cart=cart, product_info=product, quantity=quantity)
        #     new_cart_item.save()
        #
        # # return the updated cart to indicate success
        # serializer = CartSerializer(cart)
        # return Response(serializer.data)
