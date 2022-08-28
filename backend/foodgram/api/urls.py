from django.urls import path, re_path, include

app_name = 'api'

from django.urls import path, include, re_path

urlpatterns = [
    path("", include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
]