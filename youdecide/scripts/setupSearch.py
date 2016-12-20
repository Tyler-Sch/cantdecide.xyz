from youdecide.models import Ingredient, Recipes
import json
from .writeToDiskDecorator import writeJson
import re
import pickle

class ConstructSearchDict(object):
    RESTRICTIONS = ['vegan','vegetarian']
    '''
        use when constucting a new search dictionary
        ALWAYS USE AFTER POPULATING  DATABASE

        the methods should be run sequentially
        1. buildPopularIngredients
        2. reverseIngredient
        3. writeDictionaryToFile
        ------ OR -----
        run setupAll(output)

    '''
    def __init__(
            self, test=False,
            ingredients=Ingredient.objects.all(),
            recipes=Recipes.objects.all()):

        self.ingredients = [i.item.lower() for i in ingredients]
        self.recipes = recipes
        self.ingredientDict = {}
        self.popularIngredients = {}
        self.test = test
        with open(
            'youdecide/scripts/searchTemplates/veganTemplate.json','r') as veg:
            with open(
                    'youdecide/scripts/searchTemplates/vegetarianTemplate.json','r'
                ) as veggie:
                vegan = json.loads(veg.read())
                vegetarian = json.loads(veggie.read())
                self.retrictions = dict(
                    vegan=set(vegan), vegetarian=set(vegetarian))

    def buildPopularIngredients(self):
        '''
            constructs a list of ingredients that
            appear at least twice in the recipes

            gets rid of pesky errors from the
            ingredient converter
        '''
        for ingredient in self.ingredients:
            try:
                self.popularIngredients[ingredient] += 1
            except KeyError:
                self.popularIngredients[ingredient] = 1

        deleteList = [i for i in self.popularIngredients
                    if self.popularIngredients[i] < 2 ]

        #for ingredient in self.popularIngredients:
        #    if self.popularIngredients[ingredient] < 2:
        #        deleteList.append(ingredient)

        if not self.test:
            for dI in deleteList:
                del self.popularIngredients[dI]

    def reverseIngredient(self):
        '''
            constucts reverse ingredient search dictionary

            The ingredient is the key and the values
            are a list of PK numbers corresponding to
            the database
        '''
        self.ingredientDict = {
            i:[] for i in self.popularIngredients
            }

        for recipe in self.recipes:
            title = recipe.title
            ingredients = " ".join(
                _.item for _ in recipe.ingredients())
            for ingredient in self.popularIngredients:
                if ingredient.title() in title:
                    self.ingredientDict[ingredient].append(
                        recipe.pk)
                else:
                    if ingredient in ingredients:
                        self.ingredientDict[ingredient].append(
                            recipe.pk)

    def restrictions(self, recipe, restriction):
        '''
        take a recipe object
        checks the title for any non-vegan items
        then checks each ingredient

        restriction variable can be vegan or vegetarian

        WILL HAVE PROBLEMS WITH VEGAN FOOD WITH NON-VEGAN
        NAMES UNLESS 'VEGAN' IS SAID IN THE INGREDIENTS OR TITLE
        ie: un-turkey, faux chicken
    '''
        title = recipe.title.lower()
        if restriction in title.lower(): return True
        restrictDict = {'vegan':set(
            ['pancetta','mussels','butter','bass','turbot','flounder','oxtail',
            'veal','porterhouse','grouper','snapper','tuna','cod','trout',
            'prawns','branzino','sole','anchovy','anchovies','sardines','calamari',
            'halibut','prime rib','lobster','lobsters','foie gras','quail','rabbit',
            'venison','crabs','crab','goat','proscuitto','fontina','chedder','ricotta',
            'yogurt','cream','marscapone','mascarpone','guanciale','squid','ribs',
            'spareribs','rib','bacon','bratwurst','turkey','steak','steaks',
            'mozzarella','scallops','meat','pig','chicken','goose', 'beef','pork',
            'bison','filet', 'egg ','eggs','huevos','cheese','milk','fish','sardine',
            'haddock','shrimp','duck','lamb','ham','carne','clams','salmon',
            'herring','chorizo','mackeral','catfish']
            ),'vegetarian':set(
            ['pancetta','mussels','bass','turbot','flounder','oxtail','veal',
            'porterhouse','grouper','snapper','tuna','cod','trout','prawns',
            'branzino','sole','anchovy','anchovies','sardines','calamari','halibut',
            'prime rib','lobster','lobsters','foie gras','quail','rabbit',
            'venison','crabs','crab','proscuitto','guanciale','squid','ribs',
            'spareribs','rib','bacon','bratwurst','turkey','steak','steaks',
            'scallops','meat','pig','chicken','goose', 'beef','pork','bison',
            'fish','sardine','haddock','shrimp','duck','lamb','ham','carne',
            'clams','salmon']
            )}
        #delete me
        with open('veganTemplate.json','w') as veg:
            with open('vegetarianTemplate.json','w') as veget:
                veget.write(json.dumps(list(restrictDict['vegetarian'])))
                veg.write(json.dumps(list(restrictDict['vegan'])))


        if restriction not in restrictDict:
            raise KeyError('restriction not in restrictDict')

        #check title
        result = True if not len(set(
            re.split(r'\W+', title)).intersection(restrictDict[restriction])
            ) else False
        #check ingredients
        if result:
            ingredients = (x.original_txt.lower()
                for x in recipe.ingredient_set.all()
            )
            joinedSet = set(re.split(r'\W+'," ".join(ingredients)))
            if restriction in joinedSet: return True
            if len(joinedSet.intersection(restrictDict[restriction])):
                return False

        return result

    def constructRestrictions(self):
        for restrict in self.RESTRICTIONS:
            self.ingredientDict[restrict] = []
        for recipe in self.recipes:
            for restriction in self.RESTRICTIONS:
                if self.restrictions(recipe, restriction):
                    self.ingredientDict[restriction].append(recipe.pk)

    def writeAFile(self, input_,outputPath):
        with open(outputPath, 'w') as f:
            f.write(json.dumps(input_))

    def setupAll(self, outputPath):
        self.buildPopularIngredients()
        self.reverseIngredient()
        self.constructRestrictions()
        self.writeAFile(self.ingredientDict, outputPath)



