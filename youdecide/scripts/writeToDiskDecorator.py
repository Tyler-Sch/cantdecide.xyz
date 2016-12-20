import json

def writeJson(path):
    def writeJsonToDisk(func):
        def wrapper(*args,**kwargs):
            with open(path,'w') as f:
                out = func(*args,**kwargs)
                f.write(json.dumps(out))
            return
        return wrapper
    return writeJsonToDisk

@writeJson('./testdeco.json')
def blah(di):
    return di

if __name__ == '__main__':
    blah({'poop':3,'blah':'bar'})
