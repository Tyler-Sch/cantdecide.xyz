from django.test import TestCase
from django.core.urlresolvers import resolve
from .views import home, meals, new_recipe, nah
from django.http import HttpRequest
from django.template.loader import render_to_string
from .models import Recipes, Ingredient, Instructions 
from .load_db import convert_time_to_min, load_database
import json
import os


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
        test_chicken = Recipes.objects.create(title='Simple Roast Chicken', url='http://www.example.com',yiel = 2,
            active_time='10', total_time='60')
        self.assertEqual(Recipes.objects.first().title,'Simple Roast Chicken')
        test_instuction1 = Instructions.objects.create(recipe=test_chicken, step = 'Go to store, find the most beautiful chicken you have ever seen, buy it.')
        test_instruction2 = Instructions.objects.create(recipe=Recipes.objects.get(title='Simple Roast Chicken'), step='Take the chicken out of packaging. Preheat the oven to 325. Caress.')
        test_instruction3 = Instructions.objects.create(recipe=Recipes.objects.first(), step='cook that chicken right')
        self.assertEqual(3, Instructions.objects.count())
        self.assertEqual(3, len(test_chicken.instructions_set.all()))
        self.assertEqual(Instructions.objects.last().step, 'cook that chicken right')
        self.assertIn(test_instruction2.step, [i.step for i in test_chicken.instructions_set.all()])
        
        #test_ingredient_list = Ingredient_list.objects.create(recipe=test_chicken)
        #self.assertIn(test_ingredient_list, test_chicken.ingredient_list_set.all())

        test_ingredient1 = Ingredient.objects.create(item='chicken', amount='1 bird', original_txt='1 bird of the most glorious chicken you have ever seen.',recipe= test_chicken)
        test_ingredient2 = Ingredient.objects.create(item='butter', amount='1 stick', original_txt='1 stick of the sickest butter', recipe=test_chicken)

        self.assertEqual(2, Ingredient.objects.count())
        self.assertIn(test_ingredient1, test_chicken.ingredient_set.all())
        self.assertEqual('chicken', test_chicken.ingredient_set.first().item)
        self.assertEqual(len(Ingredient.objects.all()), len(test_chicken.ingredient_set.all()))


    def test_that_two_items_wont_intersect(self):
        self.assertEqual(Recipes.objects.count(),0)

        test_chicken = Recipes.objects.create(title='Chicken', url='http://www.blah.com', yiel='2', active_time='10', total_time='60')
        test_beef = Recipes.objects.create(title='Beef', url='http://www.blahblah.com', yiel='2', active_time='5', total_time='100')

        test_instruction_c1 = test_chicken.instructions_set.create(step='Go to store, find the most beautiful chicken')
        test_instruction_c2 = test_chicken.instructions_set.create(step='Buy it')
        self.assertEqual(Instructions.objects.count(), test_chicken.instructions_set.count())
        self.assertIn('Buy it', test_chicken.instructions_set.last().step)

        test_instruction_b1 = test_beef.instructions_set.create(step='Get the beef')
        test_instruction_b2 = test_beef.instructions_set.create(step='mmm beef')
        test_instruction_b3 = test_beef.instructions_set.create(step='eat da beef')
        self.assertEqual(3, test_beef.instructions_set.count())
        self.assertIn(test_instruction_b2, Instructions.objects.all())

        #test_ingredient_list = test_chicken.ingredient_list_set.create()
        #test_ingredient_list2 = test_beef.ingredient_list_set.create()
        #self.assertNotEqual(Ingredient_list.objects.first(), Ingredient_list.objects.last())

        test_ing1 = test_chicken.ingredient_set.create(item='chicken', amount='1 bird', original_txt='best damn chickn')
        
        test_ing2 = test_chicken.ingredient_set.create(item='butter', amount='1 stick', original_txt='1 stick of butter')
        self.assertEqual(Ingredient.objects.count(), 2)

        test_ing3 = test_beef.ingredient_set.create(item='beef', amount='1 cow', original_txt='1 cow of beef')
        test_ing4 = test_beef.ingredient_set.create(item='butter', amount='1 stick', original_txt='1 stick of butter')
        test_ing5 = test_beef.ingredient_set.create(item='stock', amount='1 quart', original_txt='1 quart of beef stock')
        self.assertEqual(Ingredient.objects.count(),5)


        self.assertNotEqual(Recipes.objects.first(), Recipes.objects.last())
        self.assertEqual(2, Recipes.objects.count())
        self.assertNotEqual(test_chicken.instructions_set.all(), test_beef.instructions_set.all())
        self.assertEqual(5, Instructions.objects.count())
        self.assertNotIn('Buy it', [i.step for i in test_beef.instructions_set.all()])
        self.assertNotEqual(test_chicken.ingredient_set.count(), test_beef.ingredient_set.count())
        self.assertNotIn('chicken', [i.item for i in test_beef.ingredient_set.all()])
        self.assertIn('chicken', [i.item for i in test_chicken.ingredient_set.all()])


class test_outside_database_loader(TestCase):
    def test_convert_time_to_min(self):
        x = convert_time_to_min('1 hour')
        self.assertEqual(x, 60)
        self.assertEqual(0, convert_time_to_min('0 minutes'))
        self.assertEqual(0, convert_time_to_min('0 min'))
        self.assertEqual(30, convert_time_to_min('30 minutes'))
        self.assertEqual(1440, convert_time_to_min('24 hours'))
        self.assertEqual(180, convert_time_to_min('3 hours'))
        self.assertEqual(150, convert_time_to_min('2 hours 30 minutes'))
        self.assertEqual(90, convert_time_to_min('1 1/2 hours'))
        self.assertEqual(15, convert_time_to_min('15 min'))
        self.assertEqual(120, convert_time_to_min('1 to 2 hours'))
    
class test_main_recipe_page(TestCase):

    def test_main_recipe_page_loads(self):
        test_chicken = Recipes.objects.create(title='test chicken', yiel ='3', active_time='60', total_time='100')
        request = HttpRequest()
        response = meals(request,str(test_chicken.pk))

        self.assertIn('test chicken', response.content.decode())

        test_beef=Recipes.objects.create(title='test beef', yiel = '3',active_time='60', total_time='100')
        request = HttpRequest()
        response = meals(request, str(test_beef.pk))

        self.assertNotIn('test_chicken', response.content.decode())
        self.assertIn('test beef', response.content.decode())

        request = HttpRequest()
        response = meals(request, str(test_beef.pk) +'&'+str(test_chicken.pk))

        self.assertIn('test chicken', response.content.decode())
        self.assertIn('test beef', response.content.decode())


class test_add_new_recipes(TestCase):
    def test_page_new_recipe_page_loads(self):
        request = HttpRequest()
        test_chicken = Recipes.objects.create(title='test chicken')
        response = new_recipe(request, '1')


class test_filters(TestCase):
    def test_load_db_and_test_filters(self):
        f=open('recipes/mains/saveurMainCourseRecipesAll.json','r')
        testRecipe = json.loads(f.read())
        f.close()
        load_database(testRecipe)

        self.assertEqual(testRecipe[0]['title'], Recipes.objects.first().title)
        self.assertEqual(len(testRecipe[0]['instructions']), Recipes.objects.first().instructions_set.count())
        self.assertEqual(testRecipe[0]['instructions'][0], Instructions.objects.first().step)
        self.assertEqual(testRecipe[0]['ingredients'][0], Ingredient.objects.first().original_txt)
        self.assertEqual(len(testRecipe[0]['ingredients']), Recipes.objects.first().ingredient_set.count())

        if len(testRecipe) > 1:
            self.assertNotEqual(Recipes.objects.first().ingredient_set.all(), Recipes.objects.last().ingredient_set.all())

        from youdecide import menu_programs
        from youdecide.searches.queryWrapper import writeAFile

        writeAFile(menu_programs.isVegan, 'veganFile', Recipes.objects.all())
        f = open('youdecide/searches/searchFiles/veganFile.json','r')
        dirList = os.listdir('youdecide/searches/searchFiles')
        self.assertIn('veganFile.json',dirList)
        vF = json.loads(f.read())
        f.close()
        assert(len(vF) > 1)
        #make sure you can search for vegan recipes
        x=Recipes.objects.get(pk=vF[0])
        y=Recipes.objects.get(pk=vF[1])
        self.assertNotEqual(x,y)

        #make sure you can call vegan recipes
        





