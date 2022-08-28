from django.contrib import admin

from .models import User

from recipes.models import (Tag,
                            Ingredient,
                            Recipe,
                            #IngredientInRecipe,
                            #TagsInRecipe,
                            FavoriteRecipe,
                            Cart)


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email")
    search_fields = ("first_name", "last_name", "username")
    list_filter = ("first_name", "email")
    empty_value_display = "-пусто-"

class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "slug")
    list_filter = ("name", "slug")

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "units")
    list_filter = ("name",)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "favorite_recipe")
    list_filter = (
        "name",
        "author",
        "tags",
    )

    def favorite_recipe(self, obj):
        return obj.favorite_recipe.all().count()

""" class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ("ingredient", "recipe", "amount")
    list_filter = (
        "ingredient",
        "recipe",
    ) """

class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    list_filter = ("user", "recipe")

class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    list_filter = ("user", "recipe")


admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
#admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(Cart, CartAdmin)