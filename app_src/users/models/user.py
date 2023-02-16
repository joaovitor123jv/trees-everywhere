from decimal import Decimal
from typing import TYPE_CHECKING

# Extending Django's User model directly is not good, there are several
# limitations, like not being able to customize the model fields.
# from django.contrib.auth.models import User as DjangoUser

# This is a better way to extend Django's User model. This provides the abliity
# to customize the model fields, some field behaviors, set custom admins and more.
from django.contrib.auth.models import AbstractUser as DjangoUser
from django.db import models

if TYPE_CHECKING:
    from app_src.trees.models import Tree

class User(DjangoUser):
    accounts = models.ManyToManyField('users.Account', through='users.UserAccount')

    def plant_tree(self, tree: 'Tree', location: tuple[Decimal, Decimal]):
        return 'I planted a tree!'

    def plant_trees(self):
        return 'I planted a lot of trees!'
    
    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'auth_user'
