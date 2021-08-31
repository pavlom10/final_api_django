from django.conf import settings
from django.core import mail
from django_rest_passwordreset.signals import reset_password_token_created
from .models import User, ConfirmEmailToken


def mailing_new_order(user_id, **kwargs):
    """
    Отправяем письмо при изменении статуса заказа
    """
    user = User.objects.get(id=user_id)

    emails = (
        (
            # title:
            f"Обновление статуса заказа",
            # message:
            'Заказ сформирован',
            # from:
            settings.EMAIL_HOST_USER,
            # to:
            [user.email]
        ),
    )
    result = mail.send_mass_mail(emails)
    return result


def mailing_password_reset_token_created(reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    """
    emails = (
        (
            # title:
            f"Password Reset Token for {reset_password_token.user}",
            # message:
            reset_password_token.key,
            # from:
            settings.EMAIL_HOST_USER,
            # to:
            [reset_password_token.user.email]
        ),
    )
    result = mail.send_mass_mail(emails)
    return result


def mailing_new_user_registered_signal(user_id, **kwargs):
    """
    Отправляем письмо с подтрердждением почты
    """
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    emails = (
        (
            # title:
            f"Password Reset Token for {token.user.email}",
            # message:
            token.key,
            # from:
            settings.EMAIL_HOST_USER,
            # to:
            [token.user.email]
        ),
    )

    result = mail.send_mass_mail(emails)
    return result
