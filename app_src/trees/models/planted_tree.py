from django.db import models
from django.contrib.auth import get_user_model

from .tree import Tree
from users.models import Account

User = get_user_model()


class PlantedTree(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    planted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'planted_tree'
