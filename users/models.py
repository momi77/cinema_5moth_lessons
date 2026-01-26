from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.is_superuser and not self.phone_number:
            raise ValueError("Суперпользователь обязан иметь номер телефона")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.email
