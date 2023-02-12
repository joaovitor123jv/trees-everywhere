from django.urls import path
from django.urls.conf import include
from django.contrib.auth import views as auth_views

from .views import LoginView, LogoutView

urlpatterns = [
        path('auth/login/', LoginView.as_view(), name='login'),
        path('auth/logout/', LogoutView.as_view(), name='logout'),
        path('auth/register/', LoginView.as_view(), name='register-acount'),
        path('auth/recover/', LoginView.as_view(), name='recover-password'),
        path('auth/lock/', LoginView.as_view(), name='lock-screen')
]
