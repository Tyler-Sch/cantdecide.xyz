import os
import json

def translateIngredients(ingredients):
    '''
    take list of ingredients, creates a file, and sends it to the NY
    times ingredient parser
    '''
    toWrite = "\n".join(ingredients)
    f = open("recipes/temp/ingredientsTemp.txt",'w')
    f.write(toWrite)
    f.close()

    os.system('python youdecide/scripts/loadIngredients.py recipes/temp/ingredientsTemp.txt recipes/temp/ingredientsEnd')
    os.remove('recipes/temp/ingredientsTemp.txt')

    f = open('recipes/temp/ingredientsEnd.json','r')
    ingredientList = json.loads(f.read())
    f.close()
    os.remove('recipes/temp/ingredientsEnd.json')
    return ingredientList


if __name__== "__main__":
    print(translateIngredients(['1 pound of ground chicken','3 tablespoons of black pepper', '4 granny smith apples']))
    
