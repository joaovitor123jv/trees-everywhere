from django.conf import settings
from django.urls import path
from .views import landing_page

urlpatterns = [
        path('', landing_page, name=settings.GUEST_FIRST_PAGE)
]
