import json
def writeAFile(func,args, name, recipes):
    f=open('youdecide/searches/searchFiles/'+ name +'.json', 'w')
    x = [i.id for i in recipes if func(i,args)]
    f.write(json.dumps(x))
    f.close
        
    
