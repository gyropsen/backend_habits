from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """
    Класс модели пользователя
    """

    username = None

    telegram_id = models.CharField(
        unique=True, max_length=128, verbose_name=_("telegram_id"), help_text=_("enter telegram_id")
    )
    chat_id = models.CharField(
        unique=True, max_length=128, verbose_name=_("chat_id"), **NULLABLE, help_text=_("enter chat_id")
    )
    write_message = models.BooleanField(
        default=False, verbose_name=_("write_message"), help_text=_("the user must write")
    )
    phone_number = PhoneNumberField(**NULLABLE, verbose_name=_("phone"))
    city = models.CharField(max_length=64, **NULLABLE, verbose_name=_("city"))

    USERNAME_FIELD = "telegram_id"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return str(self.email)
