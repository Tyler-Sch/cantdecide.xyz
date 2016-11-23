from selenium import webdriver
import unittest
from selenium .webdriver.common.keys import Keys
from django.test import TestCase
from youdecide.models import Recipes, Ingredient
from youdecide.scripts.load_db import load_database
import json


class NewVisitor(TestCase):
    @classmethod
    def setUpTestData(cls):
        f = open('recipes/mains/testRecipes.json','r')
        x = json.loads(f.read())
        f.close()
        load_database(x)
        

    def setUp(self):
        self.browser = webdriver.Firefox()

        self.browser.implicitly_wait(3)
       
    def tearDown(self):
        self.browser.quit()

    def test_is_you_decide_in_title(self):
        self.browser.get('http://localhost:8000/youdecide/meals')

        self.assertIn('You Decide', self.browser.title)

        #test next recipe button loads another recipe.
        recipeTargets =[]
        for i in range(3):
            self.clickNope()
            recipeTargets.append(self.browser.find_element_by_id('mainDisplay').text)

        assert(recipeTargets[0] != recipeTargets[1])
        assert(recipeTargets[1] != recipeTargets[2])

        #test yep button adds recipe titles, groceries, and changes html
        previousUrl = self.browser.current_url
        self.clickYep()
        newUrl = self.browser.current_url

        assert(previousUrl != newUrl)

        self.clickNope()
        self.clickYep()
        assert(newUrl != self.browser.current_url)

        ingredients = self.browser.find_element_by_id('grocery_list').text
        assert(len(ingredients.split()) > 1)

    def test_grocery_list_different(self):
        self.browser.get('http://localhost:8000/youdecide/meals')
        ingredients = []
        for i in range(2):
            self.clickNope()
            self.clickYep()
            ingredients.append(self.browser.find_element_by_id('grocery_list').text)
        assert(len(ingredients[0]) != len(ingredients[1]))
        




    def clickNope(self):
        self.browser.find_element_by_id('nope').click()

    def clickYep(self):
        self.browser.find_element_by_id('yep').click()
