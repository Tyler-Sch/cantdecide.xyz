from django.test import TestCase
from django.http import HttpRequest, QueryDict
from youdecide.models import Recipes
from youdecide.scripts.setupSearch import ConstructSearchDict
from youdecide.menu_programs import find_recipes, searchHelp
import pickle
from youdecide.menu_programs1.search import RecipeSearchAndReturn
import json
import random


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

        #CHANGE TO NEW FILES
        #NEED TO CONSTRUCT SEARCH OBJECT AND PICKLE IT
        x = searchHelp('arctic char',testFile)

        #CHANGE TO NEW FILES
        for i in ['arctic char fillets','chicken','chicken,onion']:
            x = random.sample(searchHelp(i,testFile),1)
            recipe = Recipes.objects.get(pk=x[0])
            ingredients = " ".join(i.item for i in recipe.ingredients())
            for item in i.split(","):
                self.assertIn(item, ingredients)

        recipePKSet = set()
        request = HttpRequest()
        #CHANGE TO NEW FIND_RECIPES
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
            #NEW SEARCH HELP NEEDS TESTING
            x = searchHelp(ingredient, 'youdecide/searches/searchFiles/TestSearch3.json')
            for pKey in x:
                recipe = Recipes.objects.get(pk=pKey)
                ingredients = ' '.join(_.item for _ in recipe.ingredients())
                for ingredient_ in ingredients.split(','):
                    self.assertIn(ingredient_, ingredients)


    def test_find_recipe_function(self):
        #YEP, THIS ONE IS USELESS TOO
        request = HttpRequest()
        find_recipes_result = find_recipes(request)
        assert(len(find_recipes_result) > 1)




