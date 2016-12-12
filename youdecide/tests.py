from django.test import TestCase,LiveServerTestCase
from django.core.urlresolvers import resolve
from youdecide.views import home, meals,newRecipeAjax, lookUpByPk,recipeAjax
from django.http import HttpRequest, QueryDict
from django.template.loader import render_to_string
from youdecide.models import Recipes, Ingredient, Instructions
from youdecide.scripts.load_db import load_database
from youdecide.scripts.setupSearch import ConstructSearchDict
from youdecide.menu_programs import find_recipes, searchHelp, reverseIngredients
import json
import os
import random
import time


class home_page_test(TestCase):
    def test_root(self):
        #is the root there?
        found = resolve('/youdecide/')
        assert(found.func == home)

    def test_home_page_returns_html(self):
        request = HttpRequest()
        response = home(request)

        expected_html = render_to_string('youdecide/home.html')
        assert(expected_html == response.content.decode())

class Test_data_base_entries(TestCase):
    
    def test_can_data_base_items_be_constructed(self):
        test_chicken = Recipes.objects.create(title='Simple Roast Chicken', 
            url='http://www.example.com',yiel = 2,
            active_time='10', total_time='60'
            )
        self.assertEqual(Recipes.objects.first().title,'Simple Roast Chicken')
        test_instuction1 = Instructions.objects.create(recipe=test_chicken, 
            step = 'Go to store, find the most beautiful chicken you have ever \
            seen, buy it.'
            )
        test_instruction2 = Instructions.objects.create(recipe=Recipes.objects.get(title='Simple Roast Chicken'), step='Take the chicken out of packaging. Preheat the oven to 325. Caress.')
        test_instruction3 = Instructions.objects.create(recipe=Recipes.objects.first(), step='cook that chicken right')
        self.assertEqual(3, Instructions.objects.count())
        self.assertEqual(3, len(test_chicken.instructions_set.all()))
        self.assertEqual(Instructions.objects.last().step, 'cook that chicken right')
        self.assertIn(test_instruction2.step, [i.step for i in test_chicken.instructions_set.all()])
        
        test_ingredient1 = Ingredient.objects.create(item='chicken', comment='1 bird', original_txt='1 bird of the most glorious chicken you have ever seen.',recipe= test_chicken)
        test_ingredient2 = Ingredient.objects.create(item='butter', comment='1 stick', original_txt='1 stick of the sickest butter', recipe=test_chicken)

        self.assertEqual(2, Ingredient.objects.count())
        self.assertIn(test_ingredient1, test_chicken.ingredient_set.all())
        self.assertEqual('chicken', test_chicken.ingredient_set.first().item)
        self.assertEqual(len(Ingredient.objects.all()), len(test_chicken.ingredient_set.all()))


class test_loadDatabase(TestCase):


    def test_load_database(self):
        f=open('recipes/mains/test/testRecipes.json','r')
        testRecipe = json.loads(f.read())
        f.close()
        load_database(testRecipe)

        self.assertEqual(testRecipe[0]['title'], Recipes.objects.first().title)
        self.assertEqual(len(testRecipe[0]['instructions']), 
            Recipes.objects.first().instructions_set.count())
        self.assertEqual(testRecipe[0]['instructions'][0], 
            Instructions.objects.first().step)
        self.assertEqual(testRecipe[0]['ingredients'][0], 
            Ingredient.objects.first().original_txt)
        self.assertEqual(len(testRecipe[0]['ingredients']), 
            Recipes.objects.first().ingredient_set.count())

        if len(testRecipe) > 1:
            self.assertNotEqual(Recipes.objects.first().ingredient_set.all(), 
                Recipes.objects.last().ingredient_set.all())

class test_find_functions(TestCase):
    fixtures = ['testRecipes']

    def loadSearchFiles(self):
        d = ConstructSearchDict(test=True, recipes=Recipes.objects.all())
        d.buildPopularIngredients()
        d.reverseIngredient()
        d.writeDictionaryToFile('youdecide/searches/searchFiles/TestSearch3.json')
        assert(d.recipes == 25)

        #test previously searched recipes
        testFile = 'youdecide/searches/searchFiles/TestSearch3.json'
        x = searchHelp('arctic char',testFile)

        for i in [['arctic char'],['chicken'],['chicken','onion']]:
            x = random.sample(searchHelp(i,testFile),1)
            recipe = Recipes.objects.get(pk=x)
            ingredients = " ".join(i.item for i in recipe.ingredients())
            for item in i:
                self.assertIn(item, ingredients)


    def helpSearch(self):
        for ingredient in ['onion','beet','beef', 'chicken,onion']:
            x = searchHelp(ingredient)
            for pKey in x:
                recipe = Recipes.objects.get(pk=pKey)
                ingredients = ' '.join(_.item for _ in recipe.ingredients())
                for ingredient_ in ingredient.split(','):
                    self.assertIn(ingredient_, ingredients)


    def test_find_recipes_function(self):
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

        #test search function
        
        request = HttpRequest()
        request.GET = QueryDict('search=Arctic+char')
        x = Recipes.objects.get(pk=find_recipes(request)).ingredients()
        self.assertIn('arctic char', " ".join(i.item for i in x))
        print('TESTING@@@@@!!!!!!!$$$$$$')
            



class test_views(TestCase):
    fixtures = ['testRecipes']
    requests = {}
    for i in range(3):
        requests['request{}'.format(i)] = HttpRequest()
    randomNumber = random.randint(1,25)
    randomNumber2 = random.randint(1,25)
    requests['request2'].GET = QueryDict('PK={}&PK={}'.format(randomNumber, randomNumber2))
    requests['request1'].GET = QueryDict('PK={}'.format(randomNumber))

    def test_meals(self):
        assert(len(Recipes.objects.all()) > 20)
        response = meals(self.requests['request1'])
        self.assertIn("thechosenfew", str(response.content))
        self.assertIn('grocery_list', str(response.content))
        self.assertIn("yep", str(response.content))
        response = meals(self.requests['request2'])
        self.assertIn('PKeyArray=[{},{}]'.format(self.randomNumber, self.randomNumber2), str(response.content))
    '''
    for this tests to work the find_recipes function needs to be altered
    def test_newRecipeAjax(self):
        attrs = ['pk','yiel','imgUrl','title','url']
        responseSet = set()
        for _ in range(5):
            response = str(newRecipeAjax(self.requests['request1']).content)
            for i in attrs:
                self.assertIn(i, response)
            responseSet.add(response)
        #yes, 2 is an arbitrary value
        assert(len(responseSet) > 2)
    '''
    def test_recipeAjax(self):
        #function gets PK and returns grocery list
        response = str(recipeAjax(self.requests['request1']).content)
        ingredients1 = [i.item for i in Recipes.objects.all()[self.randomNumber - 1].ingredients()]
        count = 0
        #count accounts for ingredients that get filtered out of view by python. ie black pepper/ water 
        # dont need to be seen on the view
        for i in ingredients1:
            try:
                self.assertIn(i, response)
            except AssertionError:
                count +=1
                continue
        if count > 2:
            raise AssertionError('Check test_recipeAjax test')

        response = str(recipeAjax(self.requests['request2']).content)
        ingredients2 = [i.item for i in Recipes.objects.all()[self.randomNumber2-1].ingredients()]
        count = 0
        for i in ingredients1 + ingredients2:
            try:
                self.assertIn(i, response)
            except AssertionError:
                count += 1
                continue
        if count > 3:
            raise AssertionError('check test_recipeAjax')


    def test_lookUpByPk(self):
        lookFor =['url','title','yiel','active_time','total_time']
        for i in self.requests:
            response = str(lookUpByPk(self.requests[i]).content)
            if i != 'request0':
                recipe = Recipes.objects.get(pk=self.requests[i].GET.dict()['PK'])
                for z in lookFor:
                    self.assertIn(z,response)
                self.assertIn(recipe.url, response)
                self.assertIn(recipe.title, response)

class test_filters_and_database_loader(TestCase):

    fixtures = ['testRecipes']
    def test_writeAFile_and_vegan_vegetarian_restrictions(self):
                #test restrictions
        from youdecide import menu_programs
        from youdecide.searches.queryWrapper import writeAFile

        writeAFile(menu_programs.restrictions,'vegan','vegan1', Recipes.objects.all())
        writeAFile(menu_programs.restrictions,'vegetarian','vegetarian1',Recipes.objects.all())
        f = open('youdecide/searches/searchFiles/vegan1.json','r')
        z = open('youdecide/searches/searchFiles/vegetarian1.json')
        dirList = os.listdir('youdecide/searches/searchFiles')
        self.assertIn('vegan1.json',dirList)
        self.assertIn('vegetarian1.json', dirList)
        vF = json.loads(f.read())
        veg = json.loads(z.read())
        z.close()
        f.close()
        assert(len(vF) > 1)
        assert(len(veg) > 1)

        #make sure you can restrict to vegan recipes
        x=Recipes.objects.get(pk=vF[0])
        y=Recipes.objects.get(pk=vF[1])
        self.assertNotEqual(x,y)
        self.assertNotEqual(vF,veg)

        #make sure you can call vegan recipes
        #This block needs to be reworked
        request1 = HttpRequest()
        request1.method = 'GET'
        request1.GET = QueryDict('restrictions=vegan1')
        self.assertEqual(request1.GET['restrictions'], 'vegan1')
        recipe = str(vF[random.choice(range(len(vF)))])

        request2 = HttpRequest()
        request2.GET = QueryDict('restrictions=vegetarian1')

        
        #test Find Recipes

        for i in range(10):
            x = find_recipes(request1)
            self.assertIn(x, vF)

        for i in range(10):
            x = find_recipes(request2)
            self.assertIn(x,veg)

        request3 = HttpRequest()
        request3.GET = QueryDict('restrictions=vegan1&restictions=vegetarian1')
       
        for i in range(10):
            x = find_recipes(request3)
            self.assertIn(x,vF)

        os.remove('youdecide/searches/searchFiles/vegan1.json')
        os.remove('youdecide/searches/searchFiles/vegetarian1.json')






