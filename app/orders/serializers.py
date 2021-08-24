from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Order


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # ordered_items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'dt'
        )