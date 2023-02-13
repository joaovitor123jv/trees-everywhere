from django.db import models


class Tree(models.Model):
    name = models.CharField(max_length=255)
    scientific_name = models.TextField()

    def __str__(self) -> str:
        return f"{self.id} | {self.name}"

    class Meta:
        db_table = 'tree'
