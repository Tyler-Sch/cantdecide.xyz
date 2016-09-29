from selenium import webdriver
import unittest
from selenium .webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from youdecide.models import Recipes, Ingredient


class NewVisitor(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        Chicken=Recipes.objects.create(title='chicken')
        Chicken.ingredient_set.create(item='chicken parts')
        Beef = Recipes.objects.create(title='Beef')
        Beef.ingredient_set.create(item='Beef parts')
        stuff = Recipes.objects.create(title='stuff')
        stuff.ingredient_set.create(item='mmm')
        moreStuff = Recipes.objects.create(title='more Stuff')
        moreStuff.ingredient_set.create(item='yuck')
  

        self.browser.implicitly_wait(3)
       
    def tearDown(self):
        self.browser.quit()

    def test_is_you_decide_in_title(self):
        self.browser.get('http://cantdecide.xyz/youdecide')

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


        
    


