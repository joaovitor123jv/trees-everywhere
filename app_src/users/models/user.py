from decimal import Decimal
from typing import TYPE_CHECKING

from django.contrib.auth.models import User as DjangoUser

if TYPE_CHECKING:
    from app_src.trees.models import Tree

class User(DjangoUser):
    def plant_tree(self, tree: 'Tree', location: tuple[Decimal, Decimal]):
        return 'I planted a tree!'

    def plant_trees(self):
        return 'I planted a lot of trees!'

    class Meta:
        proxy = True
