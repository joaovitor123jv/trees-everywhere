from django.urls import path

from .views import PlantedTreesView, PlantedTreeDetailView, PlantedTreeAddView

urlpatterns = [
        path('', PlantedTreesView.as_view(), name='planted_trees'),
        path('planted-tree/<int:id>', PlantedTreeDetailView.as_view(), name='planted-tree-detail'),
        path('planted-tree/add', PlantedTreeAddView.as_view(), name='add-planted-tree'),
]
