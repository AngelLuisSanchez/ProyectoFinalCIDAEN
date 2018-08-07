
import requests
from bs4 import BeautifulSoup
import urllib.request
import uuid
import os
import shutil


#Funcion para descargar las imagenes de el periodico el pais
def images_el_pais():

    page = requests.get('https://elpais.com/')
    soup = BeautifulSoup(page.content, 'lxml')
    
    imgs = soup.find_all('img')
    rutas = []
    for img in imgs:
        url = img.get_attribute_list('data-src')[0]
        if(url != None):
            rutas.append('https:'+str(url))
            
    try:
        shutil.rmtree('/tmp/elpais', ignore_errors=True)
    except:
        print('Error al borrar el directorio el pais')
        
    os.mkdir('/tmp/elpais')
    
    for i in range(5):
        extension = rutas[i].split('/')[-1].split('.')[-1]
        urllib.request.urlretrieve(rutas[i], '/tmp/elpais/' + str(uuid.uuid4()) + '.' + extension)


#Funcion para descargar las imagenes de el periodico el mundo
def images_el_mundo():

    page = requests.get('http://www.elmundo.es/')
    soup = BeautifulSoup(page.content, 'lxml')
    
    imgs = soup.find_all('img')
    rutas = []
    for img in imgs:
        url = img.get_attribute_list('src')[0]
        if(url != None and 'e00-elmundo.uecdn.es' in url):
            rutas.append(url)
            
    try:
        shutil.rmtree('/tmp/elmundo', ignore_errors=True)
    except:
        print('Error al borrar el directorio el mundo')
        
    os.mkdir('/tmp/elmundo')
    
    for i in range(5):
        extension = rutas[i].split('/')[-1].split('.')[-1]
        urllib.request.urlretrieve(rutas[i], '/tmp/elmundo/' + str(uuid.uuid4()) + '.' + extension)