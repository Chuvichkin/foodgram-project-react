# Generated by Django 4.1 on 2022-09-07 16:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'Корзина покупок', 'verbose_name_plural': 'Корзины покупок'},
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, unique=True, validators=[django.core.validators.RegexValidator(message='Введите значение в формате HEX!', regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')], verbose_name='Цветовой HEX-код'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='Слаг рецепта'),
        ),
    ]
