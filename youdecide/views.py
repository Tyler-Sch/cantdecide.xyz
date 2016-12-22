from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .menu_programs import find_recipes, helperGlist
from .models import Recipes
from youdecide import config
import pickle


def home(request):

    return render(request, 'youdecide/home.html')

def meals(request, days=0):

    list_ = request.GET.getlist('PK')
    if list_:
        pk1=",".join(str(x) for x in request.GET.getlist('PK'))

    return render(
        request, 'youdecide/table.html',{'pk':pk1}
        ) if list_ else render(request,'youdecide/table.html')

def newRecipeAjax(request,test_=False):
    with open(config.PATHS['PICKLEDSEARCH'],'rb') as f:
        searchClass = pickle.loads(f.read())
    if test_==True:
        with open(config.TESTPATHS['PICKLEDSEARCH'],'rb') as f:
            searchClass = pickle.loads(f.read())

    return JsonResponse(
        Recipes.objects.get(
            pk=searchClass.find_recipes(request)[0]).returnJson())

def recipeAjax(request):

    return JsonResponse(helperGlist(request))

def lookUpByPk(request):

    return JsonResponse(
        {str(i):Recipes.objects.get(
        pk=i).returnJson() for i in request.GET.getlist('PK')})



