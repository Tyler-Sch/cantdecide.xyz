from django.test import TestCase,LiveServerTestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest, QueryDict
from django.template.loader import render_to_string
from youdecide.views import home, meals,newRecipeAjax, lookUpByPk,recipeAjax
from youdecide.models import Recipes, Ingredient, Instructions
from youdecide.scripts.load_db import load_database
from youdecide.scripts.setupSearch import ConstructSearchDict
from youdecide.menu_programs import find_recipes, searchHelp
import json
import os
import random
import time


class Test_find_functions(TestCase):
    fixtures = ['testRecipes']

    def test_loadSearchFiles(self):
        d = ConstructSearchDict(
            test=True,
            recipes=Recipes.objects.all(),
            )
        d.setupAll('youdecide/searches/searchFiles/TestSearch3.json')
        assert(len(Recipes.objects.all()) == 25)

        #test previously searched recipes
        testFile = 'youdecide/searches/searchFiles/TestSearch3.json'
        x = searchHelp('arctic char',testFile)

        for i in ['arctic char fillets','chicken','chicken,onion']:
            x = random.sample(searchHelp(i,testFile),1)
            recipe = Recipes.objects.get(pk=x[0])
            ingredients = " ".join(i.item for i in recipe.ingredients())
            for item in i.split(","):
                self.assertIn(item, ingredients)

        recipePKSet = set()
        request = HttpRequest()
        for _ in range(100):
            recipePKSet.add(find_recipes(request))

        assert(len(recipePKSet) > 15)
        request.GET = QueryDict('restrictions=vegan')
        f = open('youdecide/searches/searchFiles/vegan.json','r')
        restrictions = json.loads(f.read())
        f.close()

        for _ in range(100):
            self.assertIn(find_recipes(request), restrictions)




    def test_helpSearch(self):
        for ingredient in ['onion','beet','beef', 'chicken,onion']:
            x = searchHelp(ingredient, 'youdecide/searches/searchFiles/TestSearch3.json')
            for pKey in x:
                recipe = Recipes.objects.get(pk=pKey)
                ingredients = ' '.join(_.item for _ in recipe.ingredients())
                for ingredient_ in ingredients.split(','):
                    self.assertIn(ingredient_, ingredients)






