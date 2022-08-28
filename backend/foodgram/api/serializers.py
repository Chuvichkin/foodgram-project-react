# from djoser.serializers import UserCreateSerializer
# # from rest_framework import serializers
# from users.models import User


# class RegistrationSerializer(UserCreateSerializer):
#     """
#     Сериализатор для регистрации пользователя.
#     """
#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'password'
#         )
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create(
#             email=validated_data['email'],
#             username=validated_data['username'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user





# from rest_framework import serializers
# from users.models import CustomUser, Subscription


# class ListDetailUserSerializer(serializers.ModelSerializer):
#     """Сериализатор модели Юзер GET запрос."""
#     is_subscribed = serializers.SerializerMethodField()

#     class Meta:
#         model = CustomUser
#         fields = (
#             "email",
#             "id",
#             "username",
#             "first_name",
#             "last_name",
#             "is_subscribed"
#         )

#     def get_is_subscribed(self, obj):
#         """Проверка 'subscribed' на наличие подписок"""
#         request = self.context.get('request')
#         if request is None or request.user.is_anonymous:
#             return False
#         return Subscription.objects.filter(
#             author=request.user,
#             follower=obj.id
#         ).exists()


from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=(
            'email',
            'username',
            'first_name',
            'last_name',
            'id'
        )

