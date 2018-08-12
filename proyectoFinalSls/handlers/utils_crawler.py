
import requests
from bs4 import BeautifulSoup
import urllib.request
import uuid
import os
import shutil

def download_images_covers_newspaper(newspaper, url_newspaper):    
    page = requests.get(url_newspaper)
    soup = BeautifulSoup(page.content, 'lxml')
    
    imgs = soup.find_all('img')
    routes = []
    for img in imgs:
        if(newspaper == 'elpais' or newspaper == 'abc'):
            url = img.get_attribute_list('data-src')[0]
            if(url != None):
                routes.append('https:'+str(url))
        elif(newspaper == 'elmundo'):
            url = img.get_attribute_list('src')[0]
            if(url != None and 'e00-elmundo.uecdn.es' in url):
                routes.append(url)
        elif(newspaper == 'diarioes'):
            url = img.get_attribute_list('src')[0]
            if(url != None and 'jpg' in url):
                routes.append(url_newspaper + url)
        else:
            print('newspaper not found', newspaper)
    
    try:
        shutil.rmtree('/tmp/' + newspaper, ignore_errors=True)
    except:
        print('Error delete directory', newspaper)
        
    os.mkdir('/tmp/' + newspaper)
    
    for i in range(5):
        extension = routes[i].split('/')[-1].split('.')[-1]
        urllib.request.urlretrieve(routes[i], '/tmp/'+ newspaper + '/' + str(uuid.uuid4()) + '.' + extension)
