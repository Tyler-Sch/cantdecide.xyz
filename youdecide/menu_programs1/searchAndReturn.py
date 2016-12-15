from youdecide.models import Recipes
import random
import json

class RecipeSearchAndReturn(object):

    CURRENT_RECIPE_COUNT = 9415

    def __init__(self,request,searchDictPath, quantity):
        self.request = request
        self.quantity = quantity
        with open(searchDictPath, 'r') as f:
            self.searchDict = json.loads(f.read())

    def __str__(self):
        pass


    def find_recipes(self):
        restrictions = self.request.GET.getlist('restrictions')
        search = self.request.GET.getlist('search')
        if search: search = search[0].split(',')

        optionSet = set(self.searchDict[''])
        search += restrictions

        optionSet = self.searchHelp(
            search)if search else set(self.searchDict[''])

        if len(optionSet) < self.quantity:
            returnList = [_ for _ in optionSet]
            if returnList[-1] != 1:
                returnList.append(1)
            return returnList

        return random.sample(optionSet,self.quantity)


    def searchHelp(self, searchList):
        searchResults = []
        for item in searchList:
            item = item.lower().strip()
            if item not in self.searchDict:
                with open(
                    'youdecide/searches/searchFiles/\
                    errorLog.txt','a') as f:
                    f.write(item)
            else:
                searchResults.append(set(self.searchDict[item]))

        return set.intersection(
            *searchResults) if searchResults else {1}




