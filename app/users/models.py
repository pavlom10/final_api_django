from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class UserRoleChoices(models.TextChoices):
    SHOP = 'SHOP', 'Shop'
    BUYER = 'BUYER', 'Buyer'


class User(AbstractUser):
    company = models.CharField(_('company'), max_length=40, blank=True)
    position = models.CharField(_('position'), max_length=40, blank=True)
    role = models.CharField(
        _('user role'),
        choices=UserRoleChoices.choices,
        max_length=5,
        default=UserRoleChoices.BUYER
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('email', )
