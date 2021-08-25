from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_rest_passwordreset.tokens import get_token_generator


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


class ConfirmEmailToken(models.Model):
    class Meta:
        verbose_name = _('Confirm token for email')
        verbose_name_plural = _('Confirm tokens for email')

    @staticmethod
    def generate_key():
        """ generates a pseudo random code using os.urandom and binascii.hexlify """
        return get_token_generator().generate_token()

    user = models.ForeignKey(
        User,
        related_name='confirm_email_tokens',
        on_delete=models.CASCADE,
        verbose_name=_("The User which is associated to this password reset token")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("When was this token generated")
    )

    # Key field, though it is not the primary key of the model
    key = models.CharField(
        _("Key"),
        max_length=64,
        db_index=True,
        unique=True
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ConfirmEmailToken, self).save(*args, **kwargs)

    def __str__(self):
        return "Password reset token for user {user}".format(user=self.user)
