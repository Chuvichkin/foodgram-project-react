from django.db import models
from users.models import CustomUser


class Tag(models.Model):
    name = models.TextField(verbose_name='Название тега', unique=True)
    color = models.TextField(verbose_name='Цвет тега')
    slug = models.SlugField(verbose_name='Слаг тега', unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Ingredient(models.Model):
    name = models.TextField(verbose_name='Название ингредиента')
    # quantity = models.TextField(verbose_name='Количество ингредиента')
    units = models.TextField(verbose_name='Единицы измерения')

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class Recipe(models.Model):
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='recipe',
                               verbose_name='Автор рецепта')
    name = models.CharField(max_length=200,
                            verbose_name='Название рецепта')
    picture = models.ImageField(upload_to='pictures/',
                                default=None,
                                verbose_name='Фото блюда')
    text = models.TextField(verbose_name='Название рецепта')
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag)
    cooking_time = models.IntegerField(verbose_name='Время приготовления')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredient_in_recipe",
        #verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name="ingredient_in_recipe",
        verbose_name="Ингредиент в рецепте",
    )
    amount = models.PositiveIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"


class TagsInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="tag_in_recipe",
        #verbose_name="Рецепт",
    )
    tag = models.ForeignKey(Tag,
                            on_delete=models.PROTECT,
                            related_name="tag_in_recipe",
                            verbose_name="Хештег в рецепте")
    amount = models.PositiveIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Хештег в рецепте"
        verbose_name_plural = "Хештеги в рецепте"


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name="favorite",
                             verbose_name="Пользователь")
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name="favorite_recipe",
                               verbose_name="Рецепт")

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"


class Cart(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name="cart",
                             verbose_name="Пользователь")
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name="cart_recipe",
                               verbose_name="Рецепт")

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
