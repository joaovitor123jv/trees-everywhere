from django.urls import path

from .apis import PlantedTreeApi, TreeApi

urlpatterns = [
        path('planted-tree/', PlantedTreeApi.as_view(), name='apis.planted_trees'),
        path('planted-tree/<int:id>', PlantedTreeApi.as_view(), name='apis.planted_trees.details'),
        path('tree/', TreeApi.as_view(), name='apis.trees'),
]
