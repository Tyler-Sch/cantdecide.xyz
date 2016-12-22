from django.test import TestCase
from youdecide.models import Recipes
from youdecide.scripts.setupSearch import ConstructSearchDict
from youdecide.menu_programs1.search import RecipeSearchAndReturn
from youdecide import config
import pickle
import json
import os


class MetaClassForTests(TestCase):
    fixtures = ['testRecipes']
    dictionaryLocation = 'youdecide/searches/searchFiles/TestSearch3.json'
    pickleLocation = 'youdecide/searches/searchFiles/testPickleSearch'
    howManyRecipes = 5
    with open('youdecide/scripts/searchTemplates/veganTemplate.json','r') as f:
        nonVeganFoods = json.loads(f.read())

    def setUp(self):
        d = ConstructSearchDict(
            test=True,
            recipes=Recipes.objects.all())
        d.setupAll(self.dictionaryLocation)
        search = RecipeSearchAndReturn(self.dictionaryLocation,self.howManyRecipes)
        with open(self.pickleLocation,'wb') as f:
            f.write(pickle.dumps(search))

    def tearDown(self):
        for file_ in [self.dictionaryLocation, self.pickleLocation]:
            os.remove(file_)


