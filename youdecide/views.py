from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .menu_programs import find_recipes, helperGlist
from .models import Recipes
from youdecide.menu_programs1.searchAndReturn import RecipeSearchAndReturn


def home(request):

    return render(request, 'youdecide/home.html')

def meals(request, days=0):

    list_ = request.GET.getlist('PK')
    if list_:
        pk1=",".join(str(x) for x in request.GET.getlist('PK'))

    return render(
        request, 'youdecide/table.html',{'pk':pk1}
        ) if list_ else render(request,'youdecide/table.html')

def newRecipeAjax(request):
    newSearch = RecipeSearchAndReturn(
        request, 'youdecide/searches/searchFiles/searchDict.json',5)

    return JsonResponse(
        Recipes.objects.get(
            pk=newSearch.find_recipes()[0]).returnJson())

def recipeAjax(request):

    return JsonResponse(helperGlist(request))

def lookUpByPk(request):

    return JsonResponse(
        {str(i):Recipes.objects.get(
        pk=i).returnJson() for i in request.GET.getlist('PK')})



