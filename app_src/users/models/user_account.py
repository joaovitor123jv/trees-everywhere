from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey('users.Account', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_accounts'