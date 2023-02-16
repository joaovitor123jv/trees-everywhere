from django.urls import path

from .apis import UserApi

urlpatterns = [
        path('users/', UserApi.as_view(), name='apis.users'),
]
