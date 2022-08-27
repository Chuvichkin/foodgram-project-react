from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
#from pkg_resources import _


class CustomUser(AbstractUser):
    """Модель Пользователя"""
    password = CharField(max_length=150)
    email = models.EmailField(blank=True, unique=True)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.email


class Subscription(models.Model):
    """Подписка на других авторов рецепта"""
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author'
    )
    follower = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower'
    )

    def __str__(self):
        return f'Пользователь {self.author}, подписался на {self.follower}'