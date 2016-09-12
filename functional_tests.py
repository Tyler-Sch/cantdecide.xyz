from selenium import webdriver
import unittest
from selenium .webdriver.common.keys import Keys

class NewVisitor(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

        self.browser.implicitly_wait(3)
       
    def tearDown(self):
        self.browser.quit()

    def test_is_you_decide_in_title(self):
        self.browser.get('http://localhost:8000/youdecide')
        self.assertIn('You Decide', self.browser.title)

        self.browser.find_element_by_css_selector('#days').click()

        self.assertIn('Meal Plan', self.browser.title)
        table = self.browser.find_elements_by_css_selector('table')
        assert(len(table)>1)

        currentItem=self.browser.find_element_by_id('id_meal_table').text
        self.browser.find_element_by_id('nope').click()
        new_item = self.browser.find_element_by_id('id_meal_table').text

        self.browser.find_element_by_id('yep').click()

        self.assertNotEqual(currentItem, new_item)
        assert(len(self.browser.find_elements_by_class_name('recipe'))>1)



        
    


if __name__ == '__main__': unittest.main(warnings='ignore')
