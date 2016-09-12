import random
import  os
import json
import re
from .models import Recipes

def find_recipes():
    '''
        returns a random recipe
    '''
    x = random.choice(Recipes.objects.all())
    return x.pk


def grocery_list(listOfItems):
    '''
    take a list of items and delete duplicates
    and silly things you dont need to buy
    '''

    discard = set(['&nbsp','kosher salt and ground black pepper','ground pepper','ground black pepper','kosher salt', 'water','salt','pepper', 'salt and pepper', 'salt and black pepper'])

    return listOfItems.difference(discard)






def extractIngredient(ingredient_list):
    '''
        Takes a list of strings that have groceries in them. Hopefully the main ingredient
        follows a measurement and a comma seperates the imporant ingredient from the others
        ideal format = quanity measurement of item, blah blah blah
    '''
    measurement = re.compile(r'(([\d/. ]|\bone|\btwo|\bthree|\bfour|five)+( |-g)+((jar|sprig|tablepoon|serving|chunk|stalk|head|piece|peice|ounce|oz\b|pinch|tablespoon|whole dried|whole|\bg\b|gram|small bunch|bunch[e]?|cup|medium|medium-size|teaspoon|pound|lb|can|sprig|small|knob|ear|quart|large|slice|pint|gallon)[s]?)?)',re.I)
    v_a_p = re.compile(r'(\w+ed\b)|(\w+ly\b)|(\bto\b)|(for serving)|(for garnish)|(\((.)+?\))|(plus)|(\bof)|(from)|(minced)|(\binch)', re.I)
    final_lst = []

    for item in ingredient_list:
        if 'bone-in,' in item or 'skin-on' in item or 'boneless,' in item:item= re.sub(',','',item,1)            
        if re.search(r'cut|inches',item,re.I) and not re.search(r'center-cut', item,re.I):item = item[:re.search(r'cut|inches',item).start()]
        m = re.sub(v_a_p,'', item).split(',') 
        z = re.sub(measurement, '', ' '.join(i.strip() for i in m[0].split()))
        j = ' '.join([i.strip() for i in z.split()])
        if re.match(r'^or\b',j):j=re.sub(r'^or','', j)
        if re.search(r'juicelemon|juicelime',j):j=re.sub(r'juice','juice of ',j)
        if re.search(r'zestlemon|zestlime',j):j=re.sub(r'zest', 'zest of ',j)
        ww = re.search(measurement, item)
        if ww: final_lst.append((ww.group(), j))
        else:final_lst.append(('',j))
    return final_lst        
       
