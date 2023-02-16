"""
This module contains the API endpoints for the users app.

It is equivalent to a `view` someway, but only for the API.

Templates should not be rendered here. Instead, the APIs should return JSON formatted data.
"""

from django.contrib.auth import get_user_model
from rest_framework import views, permissions, status
from django.http import JsonResponse

from .serializers import UserSerializer

User = get_user_model()


class UserApi(views.APIView):
    """
    Returns the current user's data.

    It is equivalent to the `request.user` object, but in JSON format.

    To use this endpoint, the user must be authenticated.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
