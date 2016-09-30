from bs4 import BeautifulSoup as BS
from selenium import webdriver
import sys
from multiprocessing import Pool
import json
import time
def saveurExtractRecipe(url_list):
    browser =webdriver.Firefox()
    recipes = []
    
    for recipe_link in url_list:
        browser.get(recipe_link)
        soup = BS(browser.page_source, 'lxml')
        d = {}
        d['title'] = soup.title.text
        d['url'] = recipe_link
        d['ingredients'] = [i.text.strip() for i in soup.find_all('div',class_='ingredient')]
        d['instructions'] = [i.text.strip() for i in soup.find_all('div', class_='instruction')]
        d['active_time'] = 999
        try:
            d['yiel'] = soup.find_all('div', class_='yield')[0].text.strip()
        except IndexError:
            d['yiel']=99
        try:
            d['total_time'] = soup.find_all('div', class_='cook-time')[0].text.strip()
        except IndexError:
            d['total_time'] = 999
        try:
            d['picture_url'] = soup.find_all('img')[2].attrs['src'] #this one is a gamble.
        except IndexError:
            d['picture_url'] = 'error'
        recipes.append(d)
    browser.quit()    
    return recipes
        
        
if __name__=='__main__':
    start = time.time()
    f = open('saveurHtmlMainsOnly.json')
    urls = json.loads(f.read())
    f.close()
    start = int(sys.argv[1])
    stop = int(sys.argv[2])
    shortList = (urls[start:stop][i:i+5] for i in range(0,len(urls[start:stop]),5))
    
    pool=Pool(4)
    results = pool.map(saveurExtractRecipe,shortList)
    end_results = []
    for i in results:
        for z in i:
            end_results.append(z)
    newFile = open('saveurMainCourseRecipes{}-{}.json'.format(start, stop),'w')
    newFile.write(json.dumps(end_results))
    newFile.close()
    stop=time.time()
    print('{} new recipes have been added'.format(len(end_results)))
    print(str((stop-start)/60)+ ':seconds')
        
        
