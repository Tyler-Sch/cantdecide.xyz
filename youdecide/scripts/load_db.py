from youdecide.models import Recipes, Instructions, Ingredient
import re
from youdecide.scripts.helpload import translateIngredients
import json


def deletePara(ingredients):
    '''
        removes text between parentheises
    '''
    dead_parrot = re.compile(r'\(.*?\)')
    saveurSlash = re.compile(r'⁄')
    ingredients = [re.sub(saveurSlash,'/',i) for i in ingredients]
    return [re.sub(dead_parrot,'',i) for i in ingredients]

def load_database(recipeList):

    '''
    takes a list of recipes organized as dictionaries and loads them
    into the database.
    The dictionary should have the parameters:
        'title'
        'url',
        yield as 'yiel'
        'active_time'
        'total_time'
        list of ingredients. Use helper function to extract the import parts
        image url
        list of instructions
    '''

    for recipe in recipeList:
        if len(recipe['ingredients']) == 0: continue
        t = recipe['title']
        u = recipe['url']
        y = recipe['yiel'] if recipe['yiel']  != 99 else 'error'
        tt = recipe['total_time'] if recipe['total_time']  != 999 else 'Please see recipe'
        try:
            imageUrl = recipe['picture_url'] if recipe['picture_url']  else ''
        except KeyError:
            imageUrl = ''

        try:
            new_item=Recipes.objects.create(
                title=t,
                url=u,
                yiel=y,
                total_time=tt,
                time_plus=''
                ,imgUrl=imageUrl)
        except AttributeError:
            f = open('errorrecipelog.json','a')
            f.write(json.dumps(recipe))
            f.close()
            continue

        for st in recipe['instructions']:
            new_item.instructions_set.create(step=st)
        assert(len(recipe['instructions']) == new_item.instructions_set.count())

        converted_list = translateIngredients(deletePara(recipe['ingredients']))

        try:
            assert(len(converted_list)==len(recipe['ingredients']))

        except AssertionError:
            f = open(
                'recipes/apps/{}errorLog.txt'.format(recipe['title'][:50]),'w'
                )
            f.write(json.dumps(converted_list))
            f.close()
            continue

        for i in converted_list:
            name = i['name']
            qty = i['qty']
            unit = i['unit']
            comment = i['comment']
            other = i['other']

            new_ingredient = new_item.ingredient_set.create(
                item =name,
                qty=qty,
                unit=unit,
                original_txt=i['input'],
                display=i['display'],
                comment=comment,
                other=other,
                )

