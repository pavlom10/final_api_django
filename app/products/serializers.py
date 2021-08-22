from rest_framework import serializers
from .models import Product, ProductParameter, ProductInfo
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class PartnerUpdateSerializer(serializers.ModelSerializer):
    pass


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'category', )


class ProductParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value', )


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)

    class Meta:
        model = ProductInfo
        fields = ('id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameters', )
        read_only_fields = ('id', )
