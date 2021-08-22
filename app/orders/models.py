from django.db import models
from users.models import User
from products.models import ProductInfo
from django.utils.translation import gettext_lazy as _

ORDER_ = verbose_name = _('order')


class OrderStatusChoices(models.TextChoices):
    CART = 'CART', _('cart')
    NEW = 'NEW', _('new')
    CONFIRMED = 'CONFIRMED', _('confirmed')
    ASSEMBLED = 'ASSEMBLED', _('assembled')
    SENT = 'SENT', _('sent')
    DELIVERED = 'DELIVERED', _('delivered')
    CANCELED = 'CANCELED', _('canceled')


class Contact(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'),
                             related_name='contacts', blank=True,
                             on_delete=models.CASCADE)

    phone = models.CharField(max_length=20, verbose_name=_('phone number'))
    city = models.CharField(max_length=50, verbose_name=_('city'))
    street = models.CharField(max_length=100, verbose_name=_('street'))
    house = models.CharField(max_length=15, verbose_name=_('house'), blank=True)
    building = models.CharField(max_length=15, verbose_name=_('building'), blank=True)
    apartment = models.CharField(max_length=15, verbose_name=_('apartment'), blank=True)

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')

    def __str__(self):
        return f'{self.phone} {self.city} {self.street} {self.house}'


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'),
                             related_name='orders', blank=True,
                             on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    state = models.CharField(verbose_name=_('state'),
                             choices=OrderStatusChoices.choices,
                             max_length=15,
                             default=OrderStatusChoices.CART)
    contact = models.ForeignKey(Contact, verbose_name=_('contact'),
                                blank=True, null=True,
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ('-dt',)

    def __str__(self):
        return str(self.dt)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('order'), related_name='ordered_items',
                              blank=True, on_delete=models.CASCADE)
    product_info = models.ForeignKey(ProductInfo, verbose_name=_('product info'), related_name='ordered_items',
                                     blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')
        constraints = [
            models.UniqueConstraint(fields=['order_id', 'product_info'], name='unique_order_item'),
        ]
