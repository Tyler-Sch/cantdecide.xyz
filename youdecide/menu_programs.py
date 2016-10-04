# -*- coding: utf-8 -*-
import random
import  os
import json
import re
from .models import Recipes

def find_recipes(request):
    '''
        applys filters and 
        returns a random recipe that matches the parameters
        
    '''
    filterDict = request.GET.dict()
    if not filterDict: 
        x = random.choice(Recipes.objects.all())
    else:
        option_set = set((i.pk for i in Recipes.objects.all()))
        options = os.listdir('youdecide/searches/searchFiles')
        for i in filterDict:
            if ''.join([i,'.json']) in options:
                f = open('youdecide/searches/searchFiles/'+ i +'.json', 'r')
                recipe_pk = json.loads(f.read())
                f.close()
                option_set = option_set.intersection(recipe_pk)
        return random.sample(option_set,1)[0]
                
        
    return x.pk


def grocery_list(listOfItems):
    '''
    take a list of items and delete duplicates
    and silly things you dont need to buy
    '''

    discard = set(['&nbsp','kosher salt and ground black pepper','ground pepper','ground black pepper','kosher salt', 'water','salt','pepper', 'salt and pepper', 'salt and black pepper'])

    return listOfItems.difference(discard)





'''
def extractIngredient(ingredient_list):
        #Takes a list of strings that have groceries in them. Hopefully the main ingredient
        #follows a measurement and a comma seperates the imporant ingredient from the others
        #ideal format = quanity measurement of item, blah blah blah
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
'''

def extractIngredient(ingredientList):
    '''
    takes recipe dictionary, extracts the measurement amount and a simplified ingredient
    returns a tuple (measurement, simpleIngredient)
    '''
    
    import re
    ingredients = []
    dead_parrot = re.compile(r'\(.*?\)')
    measurement = re.compile(r'(^([\d/.⁄ ]|to|\bone\-?|\btwo|\bthree|\bfour|five)+( |-g)+((jar|sprig|tablepoon|tbsp|tsp|serving|chunk|stalk|head|piece|peice|ounce|oz|pinch|tablespoon|whole dried|whole|\bg\b|gram|small bunch|bunch[e]?|cup|heaping cup|medium|medium-size|teaspoon|pound|lb|can|sprig|small|knob|ear|quart|large|slice|pint|gallon)[s]?\b\.?)?)',re.I)    
    slashthing = re.compile('⁄')
    addIng = ingredients.append
    for i in ingredientList:
        if 'bone-in,' in i or 'skin-on' in i or 'boneless,' in i or 'double-cut' in i:i= re.sub(',','',i,1)            
        if re.search(r'\bcut\b|inches',i,re.I) and not re.search(r'center-cut', i,re.I):i = i[:re.search(r'cut|inches',i).start()]
        i = ' '.join(re.sub(dead_parrot,' ',i).lower().split())
        i = i.split(',')[0]
        i = re.sub(slashthing, '/',i)
        measure = re.match(measurement, i)
        rest = re.sub(measurement, '', i)
        if measure:
            addIng(tuple([measure.group().strip(), rest.strip()]))
        else:
            addIng(tuple(['',rest]))
    
   
    return ingredients

def isVegan(recipe):
    '''
        take a recipe object
        checks the title for any non-vegan items
        then checks each ingredient
        
        WILL HAVE PROBLEMS WITH VEGAN FOOD WITH NON-VEGAN NAMES ie: un-turkey, faux chicken
    '''
    title = recipe.title.lower()
    if 'vegan' in title.lower(): return True
    notVegan = set(['mussels','butter','bass','turbot','flounder','oxtail','veal','porterhouse','grouper','snapper','tuna','cod','trout','prawns','branzino','sole','anchovy','anchovies','sardines','calamari','halibut','prime rib','lobster','lobsters','foie gras','quail','rabbit','venison','crabs','crab','goat','proscuitto','fontina','chedder','ricotta','yogurt','cream','marscapone','mascarpone','guanciale','squid','ribs','spareribs','rib','bacon','bratwurst','turkey','steak','steaks','mozzarella','scallops','meat','pig','chicken','goose', 'beef','pork','bison','filet', 'egg ','eggs','huevos','cheese','milk','fish','sardine','haddock','shrimp','duck','lamb','ham','carne','clams','salmon','herring','chorizo','mackeral','catfish'])
    vegan = True if not len(set(re.split(r'\W+', title)).intersection(notVegan)) else False
    
    if vegan:
        ingredients = (x.original_txt.lower() for x in recipe.ingredient_set.all())
        joinedSet = set(re.split(r'\W+'," ".join(ingredients)))
        if 'vegan' in joinedSet: return True
        if len(joinedSet.intersection(notVegan)):
            return False
    
    return vegan
    
            
