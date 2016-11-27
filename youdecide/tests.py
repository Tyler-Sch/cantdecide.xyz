from django.test import TestCase,LiveServerTestCase
from django.core.urlresolvers import resolve
from youdecide.views import home, meals,newRecipeAjax, lookUpByPk
from django.http import HttpRequest, QueryDict
from django.template.loader import render_to_string
from youdecide.models import Recipes, Ingredient, Instructions 
from youdecide.scripts.load_db import load_database
from youdecide.menu_programs import find_recipes
import json
import os
import random


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


class test_outside_helper_functions(TestCase):
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

class test_main_recipe_page(TestCase):

    def test_main_recipe_page_loads(self):
        test_chicken = Recipes.objects.create(title='test chicken', yiel ='3', active_time='60', total_time='100')
        request = HttpRequest()
        request.GET = QueryDict('PK='+ str(test_chicken.pk))
        response = meals(request)

        #self.assertIn('test chicken', response.content.decode())

        test_beef=Recipes.objects.create(title='test beef', yiel = '3',active_time='60', total_time='100')
        request = HttpRequest()
        request.GET=QueryDict('PK=' + str(test_beef.pk))

        response = meals(request)

        #self.assertNotIn('test_chicken', response.content.decode())
        #self.assertIn('test beef', response.content.decode())

        request = HttpRequest()
        request.GET=QueryDict('PK='+str(test_beef.pk) + "&PK=" + str(test_chicken.pk))
        response = lookUpByPk(request)
        print(response)

        #self.assertIn('test chicken', response.content.decode())
        #self.assertIn('test beef', response.content.decode())


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




class Test_fiture(TestCase):
    fixtures=['testRecipes.json']

    def test_fixture(self):
        print(len(Recipes.objects.all()))
        assert(len(Recipes.objects.all()) > 10)
        




