from rest_framework import serializers

from .models import Tree
from .models import PlantedTree


class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = ['name', 'scientific_name']


class PlantedTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantedTree
        fields = ['tree', 'user', 'account', 'planted_at']
