from django.urls import include, path
# from djoser import views
from rest_framework.routers import SimpleRouter
from .views import (
    RecipesViewSet,
    TagsViewSet,
    IngredientsViewSet,)

app_name = 'api'

router = SimpleRouter()

router.register('recipes', RecipesViewSet)
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("", include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
]
