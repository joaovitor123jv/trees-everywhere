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

    def get_user_trees(user: User):
        return PlantedTree.objects.filter(user=user)
    
    def get_account_trees(account: Account):
        return PlantedTree.objects.filter(account__in=account)
    
    def __str__(self) -> str:
        return f'{self.tree.name} planted by {self.user.username} at {self.planted_at}'

    class Meta:
        db_table = 'planted_tree'
