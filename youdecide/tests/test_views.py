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



class test_views(TestCase):
    fixtures = ['testRecipes']
    requests = {}
    for i in range(3):
        requests['request{}'.format(i)] = HttpRequest()
    randomNumber = random.randint(1,25)
    randomNumber2 = random.randint(1,25)
    requests['request2'].GET = QueryDict(
        'PK={}&PK={}'.format(randomNumber, randomNumber2))
    requests['request1'].GET = QueryDict(
        'PK={}'.format(randomNumber))

    def test_meals(self):
        assert(len(Recipes.objects.all()) > 20)
        response = meals(self.requests['request1'])
        self.assertIn("thechosenfew", str(response.content))
        self.assertIn('grocery_list', str(response.content))
        self.assertIn("yep", str(response.content))
        response = meals(self.requests['request2'])
        self.assertIn(
            'PKeyArray=[{},{}]'.format(
                self.randomNumber, self.randomNumber2),
                str(response.content))
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
        response = str(
            recipeAjax(
                self.requests['request1']).content)
        ingredients1 = (
            [i.item for i in Recipes.objects.all()[self.randomNumber - 1].ingredients()])
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
 
class test_filters(TestCase):

    fixtures = ['testRecipes']
    def test_writeAFile_and_vegan_vegetarian_restrictions(self):
                #test restrictions
        from youdecide import menu_programs
        from youdecide.searches.queryWrapper import writeAFile

        writeAFile(
            menu_programs.restrictions,'vegan','vegan1', Recipes.objects.all())
        writeAFile(
            menu_programs.restrictions,'vegetarian','vegetarian1',Recipes.objects.all())
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






