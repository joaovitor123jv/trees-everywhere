from django.db import models

from .user import User


class Account(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    users = models.ManyToManyField('users.User', through='users.UserAccount')

    def from_user(user: User):
        return Account.objects.filter(users=user)

    class Meta:
        db_table = 'account'
