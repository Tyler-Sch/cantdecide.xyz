from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .menu_programs import find_recipes, grocery_list
from .models import Recipes


def home(request):
    return render(request, 'youdecide/home.html')

def meals(request,days=0):
    list_ = request.GET.getlist('PK')
    if list_:
        pk1=",".join(str(x) for x in request.GET.getlist('PK'))

    return render(request, 'youdecide/table.html',{'pk':pk1 }) if list_ else render(request,'youdecide/table.html')
    

def newRecipeAjax(request):
    return JsonResponse(Recipes.objects.get(pk=find_recipes(request)).returnJson())

def recipeAjax(request):
    
    return JsonResponse(helperGlist(request))

def lookUpByPk(request):
    return JsonResponse({str(i):Recipes.objects.get(pk=i).returnJson() for i in request.GET.getlist('PK')})

def helperGlist(request):
    xpk = request.GET.getlist('PK')
    ingredients = {}
    discard = set(['&nbsp','kosher salt and ground black pepper','kosher salt and freshly ground black pepper','ground pepper','ground black pepper','kosher salt', 'water','salt','pepper', 'salt and pepper', 'salt and black pepper'])
    for i in xpk:
        recipe = Recipes.objects.get(pk=i).ingredients()
        for it in recipe:
            if it.item.lower() not in discard:
                try:
                    ingredients[it.item.lower()].append(it.amount)
                except KeyError:
                    ingredients[it.item.lower()] = [it.amount]
    return ingredients


