from django.views import View
from django.shortcuts import render, redirect


class PlantedTreesView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'trees/planted_trees.html', { 'user': request.user })
