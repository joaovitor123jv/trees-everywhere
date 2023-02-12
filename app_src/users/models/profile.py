from django.db import models


class Profile(models.Model):
    text = models.TextField()
    joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'profile'
