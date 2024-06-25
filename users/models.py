from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name=_("email"), help_text=_("enter your email"))
    phone_number = PhoneNumberField(**NULLABLE, verbose_name=_("phone"))
    city = models.CharField(max_length=64, **NULLABLE, verbose_name=_("city"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return str(self.email)
