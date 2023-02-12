from django.urls import path

from .views import PlantedTreesView

urlpatterns = [
        path('', PlantedTreesView.as_view(), name='planted_trees')
]
