from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Account(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    users = models.ManyToManyField(User, through='users.UserAccount')

    def __str__(self):
        return f"[{self.id}] {self.name}"

    class Meta:
        db_table = 'account'
