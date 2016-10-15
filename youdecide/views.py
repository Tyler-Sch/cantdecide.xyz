from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .menu_programs import find_recipes, grocery_list
from .models import Recipes


def home(request):
    return render(request, 'youdecide/home.html')

def meals(request, days,**kwargs):
    recipes = days.split('&')
    names = [Recipes.objects.get(pk=i) for i in recipes]
    g_list = grocery_list(set(x.item.lower() for y in names for x in y.ingredient_set.all()))
    return render(request, 'youdecide/table.html',{'names':names, 'g_list':g_list})
    
def new(request):
    return redirect('meals',days=str(find_recipes(request)))

def new_recipe(request, current):
    pass
    '''
    param = request.GET.dict()
    recipes = current.split('&')
    if 'nope' in param:
        recipes[-1] = str(find_recipes(request))
    else:
        recipes.append(str(find_recipes(request)))
    return redirect('meals', days="&".join(recipes))
    '''

def nah(request, current):
    pass
    '''
    recipes = current.split('&')
    recipes[-1] = str(find_recipes(request))
    return redirect('meals', days="&".join(recipes))
    '''
def newRecipeAjax(request):
    return JsonResponse(Recipes.objects.get(pk=find_recipes(request)).returnJson())

def recipeAjax(request):
    xpk = request.GET.getlist('PK')
    ingredients = {}
    discard = set(['&nbsp','kosher salt and ground black pepper','kosher salt and freshly ground black pepper','ground pepper','ground black pepper','kosher salt', 'water','salt','pepper', 'salt and pepper', 'salt and black pepper'])
    for i in xpk:
        recipe = Recipes.objects.get(pk=i).ingredients()
        for it in recipe:
            if it.item not in discard:
                try:
                    ingredients[it.item].append(it.amount)
                except KeyError:
                    ingredients[it.item] = [it.amount]

    return JsonResponse(ingredients)
