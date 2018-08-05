
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
        print('Error al borrar el directorio')
        
    os.mkdir('/tmp/elpais')
    
    for i in range(5):
        extension = rutas[i].split('/')[-1].split('.')[-1]
        urllib.request.urlretrieve(rutas[i], '/tmp/elpais/' + str(uuid.uuid4()) + '.' + extension)