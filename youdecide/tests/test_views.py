from django.test import TestCase
from django.http import HttpRequest, QueryDict
from youdecide.views import meals,newRecipeAjax, lookUpByPk,recipeAjax
from youdecide.models import Recipes
from youdecide.menu_programs import find_recipes
import json
import os
import random



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
        assert(len(Recipes.objects.all()) == 25)
        response = meals(self.requests['request1'])
        self.assertIn("thechosenfew", str(response.content))
        self.assertIn('grocery_list', str(response.content))
        self.assertIn("yep", str(response.content))
        response = meals(self.requests['request2'])
        self.assertIn(
            'PKeyArray=[{},{}]'.format(
                self.randomNumber, self.randomNumber2),
                str(response.content))


    def test_newRecipeAjax(self):
        attrs = ['pk','yiel','imgUrl','title','url']
        responseSet = set()
        for _ in range(5):
            print(self.requests['request1'])
            response = str(newRecipeAjax(self.requests['request1']).content)
            for i in attrs:
                self.assertIn(i, response)
            responseSet.add(response)
        #yes, 2 is an arbitrary value
        assert(len(responseSet) > 2)

    def test_recipeAjax(self):
        #function gets PK and returns grocery list
        response = str(
            recipeAjax(
                self.requests['request1']).content)
        ingredients1 = (
            [i.item for i in Recipes.objects.all()[
                self.randomNumber - 1].ingredients()])
        count = 0
        #count accounts for ingredients that get filtered out
        #if view by python. ie black pepper/ water 
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









