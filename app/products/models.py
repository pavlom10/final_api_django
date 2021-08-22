# TODO
#  Endpoints: https://github.com/netology-code/python-final-diplom/blob/master/reference/api.md

from django.db import models
from shops.models import Shop
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name=_('name'))
    shops = models.ManyToManyField(Shop, verbose_name=_('shops'), related_name='categories', blank=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=80, verbose_name=_('name'))
    category = models.ForeignKey(Category, verbose_name=_('category'), related_name='products', blank=True,
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='product_info', blank=True,
                                on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name=_('shop'), related_name='product_info', blank=True,
                             on_delete=models.CASCADE)
    model = models.CharField(max_length=80, verbose_name=_('model'), blank=True)
    external_id = models.PositiveIntegerField(verbose_name=_('external id'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    price = models.PositiveIntegerField(verbose_name=_('price'))
    price_rrc = models.PositiveIntegerField(verbose_name=_('price rrc'))

    class Meta:
        verbose_name = _('product info')
        verbose_name_plural = _('products info')
        constraints = [
            models.UniqueConstraint(fields=['product', 'shop', 'external_id'], name='unique_product_info'),
        ]


class Parameter(models.Model):
    name = models.CharField(max_length=40, verbose_name=_('name'))

    class Meta:
        verbose_name = _('parameter')
        verbose_name_plural = _('parameters')
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, verbose_name=_('product info'),
                                     related_name='product_parameters', blank=True,
                                     on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name=_('parameter'), related_name='product_parameters', blank=True,
                                  on_delete=models.CASCADE)
    value = models.CharField(verbose_name=_('value'), max_length=100)

    class Meta:
        verbose_name = _('parameter')
        verbose_name_plural = _('parameters')
        constraints = [
            models.UniqueConstraint(fields=['product_info', 'parameter'], name='unique_product_parameter'),
        ]
