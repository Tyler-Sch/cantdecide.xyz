from .models import Recipes, Instructions, Ingredient
from .menu_programs import extractIngredient
import re

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
        t = recipe['title']
        u = recipe['url']
        y = recipe['yiel'] if recipe['yiel']  != 99 else 'error'
        at = recipe['active_time'] if recipe['active_time']  != 999 else 'Please see recipe'
        tt = recipe['total_time'] if recipe['total_time']  != 999 else 'Please see recipe'
        try:
            imageUrl = recipe['picture_url']
        except TypeError:
            imageUrl = ''
        #plus = '+' if 'plus' in recipe['active_time'] else ''

        try:
            new_item=Recipes.objects.create(title=t, url=u, yiel=y, active_time=at, total_time=tt, time_plus='',imgUrl=imageUrl)
        except AttributeError:
            f = open('errorrecipelog.json','a')
            f.write(json.dumps(recipe))
            f.close()
            continue

        for st in recipe['instructions']:
            new_item.instructions_set.create(step=st)
        assert(len(recipe['instructions']) == new_item.instructions_set.count())

        #ingredient_lis = new_item.ingredient_list_set.create()

        converted_list = extractIngredient(recipe['ingredients'])
        assert(len(converted_list)==len(recipe['ingredients']))

        for i in range(len(recipe['ingredients'])):
            new_ingredient = new_item.ingredient_set.create(item = converted_list[i][1], amount = converted_list[i][0],
                original_txt = recipe['ingredients'][i])

        









   


