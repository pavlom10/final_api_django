from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ShopSerializer
from .models import Shop
from .permissions import IsOwnerOrAdmin, IsShopOrAdmin


class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Shop.objects.filter(state=True)
        return Shop.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsShopOrAdmin()]
        elif self.action in ['destroy', 'update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return []
