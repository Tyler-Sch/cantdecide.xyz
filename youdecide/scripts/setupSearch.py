from youdecide.models import Ingredient, Recipes
import json
from .writeToDiskDecorator import writeJson

class ConstructSearchDict():
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
        self, test=False, ingredients=Ingredient.objects.all(),
        recipes=Recipes.objects.all()):

        self.ingredients = [i.item.lower() for i in ingredients]
        self.recipes = recipes
        self.ingredientDict = {}
        self.popularIngredients = {}
        self.test = test

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

        deleteList = []

        for ingredient in self.popularIngredients:
            if self.popularIngredients[ingredient] < 2:
                deleteList.append(ingredient)

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

    def writeAFile(self, input_,outputPath):
        with open(outputPath, 'w') as f:
            f.write(json.dumps(input_))

    def setupAll(self, outputPath):
        self.buildPopularIngredients()
        self.reverseIngredient()
        self.writeAFile(self.ingredientDict, outputPath)



