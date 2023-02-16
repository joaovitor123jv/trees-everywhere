from datetime import datetime
from django.test import TestCase

# from django.db import models
from trees.models import PlantedTree, Tree
from users.models import User

class PlantedTreeTestCase(TestCase):
    def setUp(self):
        tree_1 = Tree.objects.create(name="Árvore-do-viajante", scientific_name="Ravenala madagascariensis")
        tree_2 = Tree.objects.create(name="Some-other-tree", scientific_name="Another scientificus namus")
        user = User.objects.create(username="testuser", email="testuser@email.com", password="testpassword")
        PlantedTree.objects.create(tree=tree_1, planted_at=datetime.now(), user=user)
        PlantedTree.objects.create(tree=tree_2, planted_at=datetime.now(), user=user)

    def test_default_creation(self):
        planted_tree_1 = PlantedTree.objects.get(tree__name="Árvore-do-viajante")
        self.assertEqual(planted_tree_1.tree.name, "Árvore-do-viajante")
        self.assertEqual(planted_tree_1.tree.scientific_name, "Ravenala madagascariensis")

