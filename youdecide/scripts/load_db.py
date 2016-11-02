from youdecide.models import Recipes, Instructions, Ingredient
import re
from youdecide.scripts.helpload import translateIngredients
import json

def convert_time_to_min(time_string):
    '''
    takes string of time and converts it to integer minutes
    ie '60 min' -> 60
    1 hour 30 min -> 90
    1 1/2 hours -> 90
    should work for days, min, and hours
    Wont work for 1/2 day at the moment.
    '''
    extract_time = re.search(r'((([\d\. /]+) (hours?|mins?|minutes?|day?))+)', time_string, re.I)
    extract_hour = re.search(r'([\d\. /]+) hours?',time_string, re.I)
    extract_min = re.search(r'([\d\. /]+) min',time_string, re.I)
    extract_day = re.search(r'(\d\. /]+) days?',time_string, re.I)
    
    if extract_time:
        total_time = 0
        if extract_hour:
            if '/' in extract_hour.group() or '.' in extract_hour.group():
                x = extract_hour.group().split()
                for i in x:
                    try:
                        if '/' not in i and '.' not in i:
                            total_time += int(i) *60
                        elif i=='1/2' or '.5' in i:
                            total_time += 30
                    except ValueError:
                        continue
            else:
                total_time += int(extract_hour.group(1)) * 60
        if extract_min:
            total_time += int(extract_min.group(1))
        if extract_day:
            total_time += int(extract_day.group(1))*60*24
        return total_time
    else:
        return 99
def extract_yield(y_string):
    '''
        returns simplified yield for recipes.
        dumbly chooses the first value if 'serves 4 or 5'
        needs work.
        returns 99 if an error
        Also has trouble with makes
    '''
    y = re.search(r'((?:ser?ves?|serving) +(\d+))|((\d+) (?:servings))',y_string, re.I)
    if not y:
        if 'makes' in y_string or 'Makes' in y_string:
            serves = re.search(r'(?:makes).+(\d+)', y_string, re.I)
            return serves.group(1)
        return 99
    else:
        try:
            serves = [x for x in y.groups() if x and x.isdigit()]
        except AttributeError:
            return 99
            
        return serves[0]
    


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
    takes a list of recipes organized as dictionaries and loads them into the database. 
    The dictionary should have the parameters:
        'title'
        'url',
        yield as 'yiel'
        'active_time'
        'total_time'
        list of ingredients. Use helper function to extract the import parts
        #TODO Add image url
        list of instructions
    '''
    
    for recipe in recipeList:
        if len(recipe['ingredients']) == 0: continue
        t = recipe['title']
        u = recipe['url']
        y = recipe['yiel'] if recipe['yiel']  != 99 else 'error'
        #at = recipe['active_time'] if recipe['active_time']  != 999 else 'Please see recipe'
        tt = recipe['total_time'] if recipe['total_time']  != 999 else 'Please see recipe'
        try:
            imageUrl = recipe['picture_url'] if recipe['picture_url']  else ''
        except KeyError:
            imageUrl = ''
        #plus = '+' if 'plus' in recipe['active_time'] else ''

        try:
            new_item=Recipes.objects.create(title=t, url=u, yiel=y,total_time=tt, time_plus='',imgUrl=imageUrl)
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
            f = open('recipes/apps/{}errorLog.txt'.format(recipe['title'][:50]),'w')
            f.write(json.dumps(converted_list))
            f.close()
            continue
            

        for i in converted_list:
            name = i['name'] 
            qty = i['qty'] 
            unit = i['unit'] 
            comment = i['comment'] 
            other = i['other'] 

            new_ingredient = new_item.ingredient_set.create(item =name,qty=qty,unit=unit,original_txt=i['input'],display=i['display'], comment=comment, other=other) 

