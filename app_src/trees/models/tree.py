from django.db import models


class Tree(models.Model):
    name = models.CharField(max_length=255)
    scientific_name = models.TextField()

    class Meta:
        db_table = 'tree'
