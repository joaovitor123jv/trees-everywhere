from django.db import models


class UserAccount(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    account = models.ForeignKey('users.Account', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_accounts'