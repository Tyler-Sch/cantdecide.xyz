from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from django.test import TestCase


class NewVisitor(TestCase):
    fixtures = ['testRecipes.json']

    def setUp(self):
        self.browser = webdriver.PhantomJS()

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

        ingredients = self.findGroceryList() 
        assert(len(ingredients.split()) > 1)

    def test_grocery_list_different_and_reset(self):
        self.browser.get('http://localhost:8000/youdecide/meals')
        ingredients = []
        for i in range(2):
            for _ in range(2):
                self.clickNope()
                self.clickYep()
            
            ingredients.append(self.findGroceryList())
        assert(len(ingredients[0]) != len(ingredients[1]))
        self.remove()
        ingredients = self.browser.find_element_by_id('grocery_list').text
        assert(not len(ingredients))

    def test_url_loads_recipes(self):
        self.browser.get('http://localhost:8000/youdecide/meals/?PK=5')
        recipeString1 = self.findRecipeTitles() 
        assert(len(self.findGroceryList()) > 1)

        self.browser.get('http://localhost:8000/youdecide/meals/?PK=6')
        recipeString2 = self.findRecipeTitles() 
        assert(recipeString1 != recipeString2)

    def test_reverse_recipe_search(self):
        self.browser.get('http://localhost:8000/youdecide/meals')
        self.browser.find_element_by_name('search').send_keys('Arctic Char')
        self.clickNope()
        assert('Arctic Char' in self.findProposed())


        

    def clickNope(self):
        self.browser.find_element_by_id('nope').click()

    def clickYep(self):
        self.browser.find_element_by_id('yep').click()

    def remove(self):
        self.browser.find_element_by_id('remove').click()

    def findGroceryList(self):
        return self.browser.find_element_by_id('grocery_list').text

    def findRecipeTitles(self):
        return self.browser.find_element_by_id('thechosenfew').text

    def findProposed(self):
        return self.browser.find_element_by_id('mainDisplay').text
