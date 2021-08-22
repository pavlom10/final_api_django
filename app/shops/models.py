from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _


class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    url = models.URLField(verbose_name=_('link'), null=True, blank=True)
    user = models.OneToOneField(User, verbose_name=_('user'),
                                blank=True, null=True,
                                on_delete=models.CASCADE)
    state = models.BooleanField(verbose_name=_('on'), default=True)

    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')
        ordering = ('-name',)

    def __str__(self):
        return self.name
