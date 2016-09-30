from selenium import webdriver
from bs4 import BeautifulSoup as BS
import json
def saveurScrapeFindHtml():
    '''
        Robotically visits pages at saveur.com and extract urls to recipe webpages.
        
        Currently moddified to find mains only: skipping over apps, breakfast, dessert, etc. 
        
        SO. SO. SLOW
        Should switch to phantomjs and add some threading
    '''
    browser = webdriver.PhantomJS()
    start_html = 'http://www.saveur.com/recipes-search'
    browser.get(start_html)
    soup = BS(browser.page_source,'lxml')
    x = soup.find_all('div', class_='result_title')
    html_list = ["".join(['http://saveur.com', x[i].find_all('a')[0].attrs['href']]) for i in range(len(x))]
    begin_page = 2
    max_page = 42 #should be 149 for all recipes as of september 20th 2016 or NOT HARD CODED AT ALL
    while begin_page < max_page:
        browser.get(start_html + '?page={}&filter[3]=1000961'.format(begin_page))
        soup = BS(browser.page_source,'lxml')
        x = soup.find_all('div', class_='result_title')
        more_html = ["".join(['http://saveur.com', x[i].find_all('a')[0].attrs['href']]) for i in range(len(x))]
        html_list.extend(more_html)
        begin_page += 1
    browser.quit()
    return html_list

if __name__ =='__main__':
    x=saveurScrapeFindHtml()
    f = open('saveurHtmlMainsOnly.json','w')
    f.write(json.dumps(x))
    f.close
    print(len(x))

    
