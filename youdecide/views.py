from django.shortcuts import render, redirect
from django.http import HttpResponse
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
    param = request.GET.dict()
    recipes = current.split('&')
    if 'nope' in param:
        recipes[-1] = str(find_recipes(request))
    else:
        recipes.append(str(find_recipes(request)))
    return redirect('meals', days="&".join(recipes))

def nah(request, current):
    recipes = current.split('&')
    recipes[-1] = str(find_recipes(request))
    return redirect('meals', days="&".join(recipes))
