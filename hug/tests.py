from django.test import TestCase
from hug.models import Tree
import unittest


class TestBasic(unittest.TestCase):
    "Basic tests"

    def test_basic(self):
        a = 1
        self.assertEqual(1, a)

    def test_basic_2(self):
        a = 1
        assert a == 1


class TreeTestCase(TestCase):
    def setUp(self):
        Tree.objects.create(treeId=251469, neighbourhood='DOWNTOWN', commonName='NO SUCH THING', diameter=4, streetNumber=509, street='HELLO', lat=4.98, lon=123.64)

    def test_trees_can_save(self):
        tree1 = Tree.objects.get(treeId=251469)
        tree1.save()



