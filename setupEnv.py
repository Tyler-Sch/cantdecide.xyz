'''
Script to load database, load common filters
Needs the NYtimes ingredient parser ../NYTimesRecipeTK/ingredient-phrase-tagger-master

./manage.py shell < setupEnv.py
'''

import os
import json
from youdecide.scripts import load_db
from youdecide.searches.queryWrapper import writeAFile
from youdecide.models import Recipes
from youdecide import menu_programs



for item in os.listdir('youdecide/searches/searchFiles'):
    os.remove('youdecide/searches/searchFiles/'+item)
    
#delete test when running live
#make sure to include the / at the end of directories
for item in os.listdir('recipes/mains/test/'):
    with open('recipes/mains/test/'+item, 'r') as f:
        recipeDict = json.loads(f.read())
        load_db.load_database(recipeDict)


restrictions = set(['vegan','vegetarian'])

for i in restrictions:
    writeAFile(menu_programs.restrictions, i, i, Recipes.objects.all())
        

