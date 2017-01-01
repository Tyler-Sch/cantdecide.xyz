# -*- coding: utf-8 -*-
from youdecide.models import Recipes

def helperGlist(request):
    '''
    removes salt and pepper from the visible ingredient list.
    Both ingredients appear in almost every recipe, and they are often
    written differently. So this exists to prevent having a pile up 
    of salt entries
    '''
    xpk = request.GET.getlist('PK')
    ingredients = {}
    discard = set(
        ['&nbsp','kosher salt and ground black pepper',
        'kosher salt and freshly ground black pepper',
        'ground pepper','ground black pepper','kosher salt',
        'water','salt','pepper', 'salt and pepper', 'salt and black pepper']
        )
    for i in xpk:
        recipe = Recipes.objects.get(pk=i).ingredients()
        for it in recipe:
            display = it.original_txt
            if it.item:
                item = it.item
            else:
                item = it.original_txt

            if item.lower() not in discard:
                try:
                    ingredients[item.lower()] += '<br>'+ display
                except KeyError:
                    ingredients[item.lower()] = display
    return ingredients
