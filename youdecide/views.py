from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .menu_programs import find_recipes, helperGlist
from .models import Recipes


def home(request):
    return render(request, 'youdecide/home.html')

def meals(request, days=0):
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



