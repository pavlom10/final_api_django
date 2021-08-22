from django_filters import rest_framework as filters
from products.models import ProductInfo


class ProductInfoFilter(filters.FilterSet):
    shop_id = filters.NumberFilter(field_name='shop')
    category_id = filters.NumberFilter(field_name='category')

    class Meta:
        model = ProductInfo
        fields = ('shop', 'category')
