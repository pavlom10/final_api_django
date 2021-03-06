from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from django.db.models import Q, Sum, F
from products.models import ProductInfo
from products.serializers import ProductInfoSerializer
from users.mailing import mailing_new_order
from .models import Order, OrderItem, OrderStatusChoices, Contact
from .serializers import CartSerializer, OrderSerializer, ContactSerializer
from .permissions import IsBuyerOrAdmin
# from .filters import ProductInfoFilter


class ProductInfoView(APIView):
    """
    An endpoint for product listing.
    """
    serializer_class = None
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs):

        query = Q(shop__state=True)
        shop_id = request.query_params.get('shop_id')
        category_id = request.query_params.get('category_id')

        if shop_id:
            query = query & Q(shop_id=shop_id)

        if category_id:
            query = query & Q(product__category_id=category_id)

        queryset = ProductInfo.objects.filter(
            query).select_related(
            'shop', 'product__category').prefetch_related(
            'product_parameters__parameter').distinct()
        serializer = ProductInfoSerializer(queryset, many=True)

        return Response(serializer.data)


class CartView(APIView):
    """
    An endpoint for adding position to cart.
    """
    permission_classes = [IsBuyerOrAdmin]
    serializer_class = CartSerializer
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        cart, _ = Order.objects.get_or_create(user_id=request.user.id, state=OrderStatusChoices.CART)

        try:
            product = ProductInfo.objects.get(
                pk=request.data['product_id']
            )
            quantity = int(request.data['quantity'])
        except Exception as e:
            return Response({'Status': False, 'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        existing_cart_item = OrderItem.objects.filter(order=cart, product_info=product).first()
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
        else:
            new_cart_item = OrderItem(order=cart, product_info=product, quantity=quantity)
            new_cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)


class ContactViewSet(viewsets.ModelViewSet):
    """
    An endpoint for user contacts.
    """
    serializer_class = ContactSerializer
    permission_classes = [IsBuyerOrAdmin]

    def get_queryset(self):
        if self.action == 'list':
            return Contact.objects.filter(user=self.request.user)
        return Contact.objects.all()


class OrderView(APIView):
    """
    An endpoint for orders listing and posting.
    """
    permission_classes = [IsBuyerOrAdmin]
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(
            user_id=request.user.id).exclude(state=OrderStatusChoices.CART).prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if {'id', 'contact'}.issubset(request.data):
            if request.data['id'].isdigit():
                try:
                    is_updated = Order.objects.filter(
                        user_id=request.user.id, id=request.data['id']).update(
                        contact_id=request.data['contact'],
                        state=OrderStatusChoices.NEW)
                except Exception as e:
                    return Response({'Status': False, 'Error': str(e)})
                else:
                    if is_updated:
                        # mailing_new_order(user_id=request.user.id)
                        return Response({'Status': 'Ok'})

        return Response(status=status.HTTP_400_BAD_REQUEST)
