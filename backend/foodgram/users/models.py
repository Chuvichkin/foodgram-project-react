from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import UniqueConstraint
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique follow',
            )
        ]
