import sys
import os

if len(sys.argv) < 3:
    print('Usage: filename inputFileName outputfileName')
    sys.exit()
inputFile = str(sys.argv[1])
outputFile = str(sys.argv[2])

os.system('python ../NYTimesRecipeTK/ingredient-phrase-tagger-master/bin/parse-ingredients.py ' + inputFile + ' > results.txt')

os.system('python ../NYTimesRecipeTK/ingredient-phrase-tagger-master/bin/convert-to-json.py results.txt > ' + outputFile +'.json')


os.remove('results.txt')









