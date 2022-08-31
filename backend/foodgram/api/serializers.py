from django.forms import ValidationError
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Cart, FavoriteRecipe, Ingredient,
                            IngredientInRecipe, Recipe, Tag)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Follow, User


class UserCreateSerializer(serializers.ModelSerializer):
    """для новых пользователей"""
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'id'
        )


class UserSerializer(serializers.ModelSerializer):
    """для существующих пользователей"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        """прибавляем поле подписки пользователя на автора."""
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        user = request.user
        following = obj.follower.filter(user=obj, following=user)
        return following.exists()


class FollowListSerializer(serializers.ModelSerializer):
    """для списка избранных авторов"""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source="recipes.count", read_only=True
    )

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "recipes",
            "is_subscribed",
            "recipes_count",
        )
        read_only_fields = fields

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        user = request.user
        following = obj.follower.filter(user=obj, following=user)
        return following.exists()

    def get_recipes(self, obj):
        request = self.context.get("request")
        context = {"request": request}
        recipes = obj.recipes.all()
        return FollowRecipeSerializer(
            recipes, context=context, many=True
        ).data


class FollowCreateSerializer(serializers.ModelSerializer):
    """для подписки на пользователя"""
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ("user", "following",)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=("user", "following"),
                message="Подписка уже оформлена.",
            )
        ]

    def validate_self_following(self, value):
        user = self.context.get("request").user
        if user == value:
            raise serializers.ValidationError("Нельзя подписаться на себя.")
        return value


class TagListSerializer(serializers.ModelSerializer):
    """для тегов"""
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientsListSerializer(serializers.ModelSerializer):
    "для списка ингредиентов"
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class RecipeListSerializer(serializers.ModelSerializer):
    """для списка рецептов"""
    tags = TagListSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_ingredients(self, obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return ShowIngredientInRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context["request"]
        if request.user.is_anonymous:
            return False
        user_id = request.user.id
        favorite = FavoriteRecipe.objects.all().filter(user=user_id, recipe=obj)
        return favorite.exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context["request"]
        if request.user.is_anonymous:
            return False
        user_id = request.user.id
        recipe_in_cart = Cart.objects.all().filter(
            user=user_id, recipe=obj
        )
        return recipe_in_cart.exists()


class FollowRecipeSerializer(serializers.ModelSerializer):
    """для добавления рецепта в избранное"""
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class ShowIngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientInRecipe
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ("id", "amount")


class RecipeCreateSerializer(serializers.ModelSerializer):
    """для создания и изменения рецепта."""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientInRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def add_recipe_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient["id"]
            amount = ingredient["amount"]
            IngredientInRecipe.objects.update_or_create(
                recipe=recipe,
                ingredient=ingredient_id,
                defaults={"amount": amount},
            )

    def create(self, validated_data):
        author = self.context.get("request").user
        tag_from_data = validated_data.pop("tags")
        ingredients_from_data = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.add_recipe_ingredients(ingredients_from_data, recipe)
        recipe.tags.set(tag_from_data)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.image = validated_data.get("image", instance.image)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        tag_from_data = validated_data.pop("tags")
        if tag_from_data:
            instance.tags.set(tag_from_data)

        ingredients_from_data = self.validated_data.pop("ingredients")
        instance.ingredients.clear()
        self.add_recipe_ingredients(ingredients_from_data, instance)
        instance.save()
        return instance

    def validate(self, data):
        ingredients = self.initial_data.get("ingredients")
        if ingredients == []:
            raise ValidationError(
                {"Ошибка": "Необходимо выбрать хотя бы один ингредиент"}
            )
        amounts = data.get("ingredients")
        if [item for item in amounts if item["amount"] < 1]:
            raise serializers.ValidationError(
                {"amount": "Минимальное количество ингридиента 1"}
            )
        for ingredient in ingredients:
            if ingredients.count(ingredient) > 1:
                id = ingredient["id"]
                name = Ingredient.objects.all().get(id=id).name
                raise ValidationError({f"{name}": f"{name} уже есть в списке"})
        return data

    def to_representation(self, recipe):
        return RecipeListSerializer(
            recipe, context={"request": self.context.get("request")}
        ).data


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class FavoriteSerializer(serializers.ModelSerializer):
    """Для полей ManyToMany и обратных связей (объектов RelatedManager) создаём поле класса PrimaryKeyRelatedField."""
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = FavoriteRecipe
        fields = ("user", "recipe")

    def validate_recipe(self, data):
        user = self.context.get("request").user
        new_recipe = self.initial_data.get("recipe")
        if (
            FavoriteRecipe.objects.all()
            .filter(user=user, recipe=new_recipe)
            .exists()
        ):
            raise ValidationError("Этот рецепт у вас уже в избранном")
        return data

    def to_representation(self, instance):
        return RecipeSerializer(instance.recipe).data


class CartSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Cart
        fields = ("user", "recipe")

    def validate_recipe(self, data):
        user = self.context.get("request").user
        recipe = self.initial_data.get("recipe")
        if (
            Cart.objects.all()
            .filter(user=user, recipe=recipe)
            .exists()
        ):
            raise ValidationError("Этот рецепт уже в вашей корзине")
        return data

    def to_representation(self, instance):
        return RecipeSerializer(instance.recipe).data
