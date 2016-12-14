from django.test import TestCase
from youdecide.models import Recipes, Ingredient, Instructions
from youdecide.scripts.load_db import load_database
import json



class Test_data_base_entries(TestCase):
    def test_can_data_base_items_be_constructed(self):
        test_chicken = Recipes.objects.create(
            title='Simple Roast Chicken',
            url='http://www.example.com',
            yiel = 2,
            active_time='10',
            total_time='60'
            )

        self.assertEqual(Recipes.objects.first().title,'Simple Roast Chicken')
        test_instuction1 = Instructions.objects.create(
            recipe=test_chicken, 
            step = 'Go to store, find the most beautiful chicken you have ever \
            seen, buy it.'
            )
        test_instruction2 = Instructions.objects.create(
            recipe=Recipes.objects.get(
                title='Simple Roast Chicken'), 
                step='Take the chicken out of packaging. Preheat\
                the oven to 325. Caress.')
        test_instruction3 = Instructions.objects.create(
            recipe=Recipes.objects.first(), 
            step='cook that chicken right')

        self.assertEqual(3, Instructions.objects.count())
        self.assertEqual(3, len(test_chicken.instructions_set.all()))
        self.assertEqual(
            Instructions.objects.last().step, 'cook that chicken right')
        self.assertIn(
            test_instruction2.step, 
            [i.step for i in test_chicken.instructions_set.all()])
        
        test_ingredient1 = Ingredient.objects.create(
            item='chicken', 
            comment='1 bird', 
            original_txt='1 bird of the most glorious \
            chicken you have ever seen.',
            recipe= test_chicken)
        test_ingredient2 = Ingredient.objects.create(
            item='butter', 
            comment='1 stick', 
            original_txt='1 stick of the sickest butter', 
            recipe=test_chicken)

        self.assertEqual(2, Ingredient.objects.count())
        self.assertIn(test_ingredient1, test_chicken.ingredient_set.all())
        self.assertEqual('chicken', test_chicken.ingredient_set.first().item)
        self.assertEqual(
            len(Ingredient.objects.all()), 
            len(test_chicken.ingredient_set.all()))


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


