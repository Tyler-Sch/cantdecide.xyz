from django.test import TestCase
from django.http import HttpRequest, QueryDict
from youdecide.models import Recipes
from youdecide.scripts.setupSearch import ConstructSearchDict
from youdecide.menu_programs1.search import RecipeSearchAndReturn
import pickle
import json
import random
import os


class Test_find_functions(TestCase):
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

    def test_loadSearchFiles(self):
        self.assertEqual(len(Recipes.objects.all()),25)

        #should only be lower case entries in searchDict
        with open(self.dictionaryLocation,'r') as dict_:
            searchDict = json.loads(dict_.read())
            assert('chicken' in searchDict)
            assert('arctic char fillets' in searchDict)
            assert(len(searchDict['chicken']) > 3)

        with open(self.pickleLocation,'rb') as searchFile:
            search = pickle.loads(searchFile.read())
            listOfSearchMethods = dir(search)
            self.assertIn('find_recipes', listOfSearchMethods)
            self.assertIn('searchHelp',listOfSearchMethods)


    def test_find_recipes(self):
        self.assertEqual(len(Recipes.objects.all()),25)

        #load_search_object and Http Request
        request = HttpRequest()

        with open(self.pickleLocation,'rb') as s:
            search = pickle.loads(s.read())
            assert(len(search.find_recipes(request)) == self.howManyRecipes)


        #searchHelp tests
        for i in [['arctic char fillets'],['chicken'],['chicken','onion']]:
            x = random.sample(search.searchHelp(i),1)
            recipe = Recipes.objects.get(pk=x[0])
            ingredients = " ".join(i.item for i in recipe.ingredients())
            for item in i:
                self.assertIn(item, ingredients)


        request.GET = QueryDict('restrictions=vegan')
        veganList = search.find_recipes(request)
        #assert that if find_recipes doesnt have enough recipes to fill 
        #a quanity, it returns a shorter list ending in a 1
        assert(veganList[-1] == 1)
        assert(len(veganList) > 1)
        assert(len(veganList) < self.howManyRecipes)


        for recipePK in veganList:
            recipe = Recipes.objects.get(pk=recipePK)
            ingredients = " ".join([_.item for _ in recipe.ingredients()])
            for nonVeggie in self.nonVeganFoods:
                self.assertNotIn(nonVeggie, ingredients)

        request.GET = QueryDict('restrictions=vegan&search=chicken')
        nonSensicalFindRecipe = search.find_recipes(request)
        self.assertEqual(nonSensicalFindRecipe[0], 1)
        assert(len(nonSensicalFindRecipe) == 1)









    #def test_find_recipe_function(self):
        #YEP, THIS ONE IS USELESS TOO
        #request = HttpRequest()
        #find_recipes_result = find_recipes(request)
        #assert(len(find_recipes_result) > 1)




