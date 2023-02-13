from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from trees.models import PlantedTree
from users.models import Account

class PlantedTreesView(LoginRequiredMixin, View):
    def get(self, request):
        user_trees = PlantedTree.get_user_trees(request.user)
        account_trees = PlantedTree.get_account_trees(Account.from_user(request.user))
        page_context = { 'user': request.user, 'user_trees': user_trees, 'account_trees': account_trees }
        return render(request, 'trees/planted_trees.html', page_context)
