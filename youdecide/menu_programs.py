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
    ####!!!! MODIFY THAT RANDOM RANGE BEFORE PRODUCTION !!!!#####
    filterDict = request.GET.getlist('restrictions')
    if not filterDict: 
        return random.randint(1,15)
    else:
        option_set = set(i for i in range(1,15))
        options = os.listdir('youdecide/searches/searchFiles')
        for i in filterDict:
            if ''.join([i,'.json']) in options:
                f = open('youdecide/searches/searchFiles/'+ i +'.json', 'r')
                recipe_pk = json.loads(f.read())
                f.close()
                option_set = option_set.intersection(recipe_pk)
        return random.sample(option_set,1)[0] if option_set else 0


def helperGlist(request):
    xpk = request.GET.getlist('PK')
    ingredients = {}
    discard = set(['&nbsp','kosher salt and ground black pepper','kosher salt and freshly ground black pepper','ground pepper','ground black pepper','kosher salt', 'water','salt','pepper', 'salt and pepper', 'salt and black pepper'])
    for i in xpk:
        recipe = Recipes.objects.get(pk=i).ingredients()
        for it in recipe:
            display = it.original_txt
            if it.item:
                item = it.item
            else:
                item = it.original_txt

            if item.lower() not in discard:
                try:
                    ingredients[item.lower()] += '<br>'+ display
                except KeyError:
                    ingredients[item.lower()] = display
    return ingredients

def restrictions(recipe, restriction):
    '''
        take a recipe object
        checks the title for any non-vegan items
        then checks each ingredient

        restriction variable can be vegan or vegetarian 
        
        WILL HAVE PROBLEMS WITH VEGAN FOOD WITH NON-VEGAN NAMES UNLESS 'VEGAN' IS SAID IN THE INGREDIENTS OR TITLE
        ie: un-turkey, faux chicken
    '''
    title = recipe.title.lower()
    if restriction in title.lower(): return True
    restrictDict = {'vegan':set(['pancetta','mussels','butter','bass','turbot','flounder','oxtail','veal','porterhouse','grouper','snapper','tuna','cod','trout','prawns','branzino','sole','anchovy','anchovies','sardines','calamari','halibut','prime rib','lobster','lobsters','foie gras','quail','rabbit','venison','crabs','crab','goat','proscuitto','fontina','chedder','ricotta','yogurt','cream','marscapone','mascarpone','guanciale','squid','ribs','spareribs','rib','bacon','bratwurst','turkey','steak','steaks','mozzarella','scallops','meat','pig','chicken','goose', 'beef','pork','bison','filet', 'egg ','eggs','huevos','cheese','milk','fish','sardine','haddock','shrimp','duck','lamb','ham','carne','clams','salmon','herring','chorizo','mackeral','catfish']),'vegetarian':set(['pancetta','mussels','bass','turbot','flounder','oxtail','veal','porterhouse','grouper','snapper','tuna','cod','trout','prawns','branzino','sole','anchovy','anchovies','sardines','calamari','halibut','prime rib','lobster','lobsters','foie gras','quail','rabbit','venison','crabs','crab','proscuitto','guanciale','squid','ribs','spareribs','rib','bacon','bratwurst','turkey','steak','steaks','scallops','meat','pig','chicken','goose', 'beef','pork','bison','fish','sardine','haddock','shrimp','duck','lamb','ham','carne','clams','salmon'])}

    if restriction not in restrictDict: raise KeyError ('restriction not in restrictDict')
    #check title
    result = True if not len(set(re.split(r'\W+', title)).intersection(restrictDict[restriction])) else False
    
    if result:
        ingredients = (x.original_txt.lower() for x in recipe.ingredient_set.all())
        joinedSet = set(re.split(r'\W+'," ".join(ingredients)))
        if restriction in joinedSet: return True
        if len(joinedSet.intersection(restrictDict[restriction])):
            return False
    
    return result 



