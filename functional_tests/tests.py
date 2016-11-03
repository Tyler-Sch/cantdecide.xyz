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

        self.browser.find_element_by_id('days').click()

        self.assertIn('You Decide', self.browser.title)
        table = self.browser.find_elements_by_class_name('recipe')
        assert(len(table)>=1)

        currentItem=self.browser.find_element_by_id('id_meal_table').text
        self.browser.find_element_by_id('nah').click()
        new_item = self.browser.find_element_by_id('id_meal_table').text

        self.browser.find_element_by_id('yep').click()

        self.assertNotEqual(currentItem, new_item)
        assert(len(self.browser.find_elements_by_class_name('recipe'))>1)
        print('made it this far')

        self.browser.find_element_by_id('vegan_box').click()
        
    


