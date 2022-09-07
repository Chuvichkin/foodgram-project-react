# Generated by Django 4.1 on 2022-09-07 19:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_alter_shoppingcart_options_alter_tag_color_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Favourite',
            new_name='Favorite',
        ),
        migrations.RemoveConstraint(
            model_name='favorite',
            name='unique_favourite',
        ),
        migrations.RemoveConstraint(
            model_name='shoppingcart',
            name='unique_shopping_cart',
        ),
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=9, unique=True, verbose_name='Цветовой HEX-код'),
        ),
    ]