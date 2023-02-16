
"""
This module contains the API endpoints for the trees app.

It is equivalent to a `view` someway, but only for the API.

Templates should not be rendered here. Instead, the APIs should return JSON formatted data.
"""

from django.contrib.auth import get_user_model
from rest_framework import views, permissions, status
from django.http import JsonResponse

from .models import Tree, PlantedTree
from .serializers import TreeSerializer, PlantedTreeSerializer

User = get_user_model()


class TreeApi(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        available_trees = Tree.objects.all().order_by('name')
        serializer = TreeSerializer(available_trees, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


class PlantedTreeApi(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        planted_trees = PlantedTree.get_all_visible_for_user(request.user)
        serializer = PlantedTreeSerializer(planted_trees, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
