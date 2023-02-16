from django.db import transaction
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from .forms import PlantedTreeForm
from trees.models import PlantedTree


class PlantedTreesView(LoginRequiredMixin, View):
    def get(self, request):
        planted_trees = PlantedTree.get_all_visible_for_user(request.user)
        page_context = { 'user': request.user, 'planted_trees': planted_trees }
        return render(request, 'trees/planted_trees.html', page_context)


class PlantedTreeDetailView(LoginRequiredMixin, View):
    def get(self, request, id: int):
        planted_tree = get_object_or_404(PlantedTree, id=id)
        if not planted_tree.can_show_to_user(request.user):
            raise PermissionDenied("You don't have permission to view this tree")
        return render(request, 'trees/planted_tree_detail.html', { 'user': request.user, 'planted_tree': planted_tree })


class PlantedTreeAddView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'trees/planted_tree_add.html', { 'user': request.user, 'form': PlantedTreeForm() })

    @transaction.atomic
    def post(self, request):
        form = PlantedTreeForm(request.POST)

        if not form.is_valid():
            return render(request, 'trees/planted_tree_add.html', { 'user': request.user, 'form': form })
        
        planted_tree = form.save(commit=False)
        planted_tree.user = request.user
        planted_tree.save()
        return render(request, 'trees/planted_tree_detail.html', { 'user': request.user, 'planted_tree': planted_tree })
