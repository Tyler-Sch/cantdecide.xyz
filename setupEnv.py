'''
Script to load database, load common filters
Needs the NYtimes ingredient parser ../NYTimesRecipeTK/ingredient-phrase-tagger-master

./manage.py shell < setupEnv.py
'''

import os
import json
from youdecide.scripts import load_db, setupSearch
from youdecide.models import Recipes
from youdecide.menu_programs1.search import RecipeSearchAndReturn
from youdecide import menu_programs
from youdecide import config
import pickle




searchDictPath = config.PATHS['SEARCHDICTPATH']
quantity = 5  #how long of list of recipes does find_recipes return
pickleFile = config.PATHS['PICKLEDSEARCH']

#uncomment out if you build from scratch
#Recipes.objects.create(title='Sorry, no recipe could be found')
#
#for item in os.listdir('recipes/mains/'):
#    with open('recipes/mains/'+item, 'r') as f:
#        recipeDict = json.loads(f.read())
#        load_db.load_database(recipeDict)

ingredients = Ingredient.obejects.all()
recipes = Recipes.objects.all()

setupSearch_ = setupSearch.ConstructSearchDict(
    ingredients=ingredients,recipes=recipes)

setupSearch.setupAll(searchDictPath)

#create Pickle

search = RecipeSearchAndReturn(searchDictPath,quantity)
with open(pickleFile, 'wb') as f:
    f.write(pickle.dumps(search))
