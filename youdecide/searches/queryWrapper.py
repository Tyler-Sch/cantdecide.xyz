import json
def writeAFile(func, name, recipes):
    f=open('youdecide/searches/searchFiles/'+ name +'.json', 'w')
    x = [i.id for i in recipes if func(i)]
    f.write(json.dumps(x))
    f.close
        
    
