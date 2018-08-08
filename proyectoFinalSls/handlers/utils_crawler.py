
import requests
from bs4 import BeautifulSoup
import urllib.request
import uuid
import os
import shutil

 

#Funcion unificada para los 4 periodicos
def descargar_imagenes_portadas_periodicos(periodico, url_periodico):
    
    page = requests.get(url_periodico)
    soup = BeautifulSoup(page.content, 'lxml')
    
    imgs = soup.find_all('img')
    rutas = []
    for img in imgs:
        if(periodico == 'elpais' or periodico == 'abc'):
            url = img.get_attribute_list('data-src')[0]
            if(url != None):
                rutas.append('https:'+str(url))
        elif(periodico == 'elmundo'):
            url = img.get_attribute_list('src')[0]
            if(url != None and 'e00-elmundo.uecdn.es' in url):
                rutas.append(url)
        elif(periodico == 'diarioes'):
            url = img.get_attribute_list('src')[0]
            if(url != None and 'jpg' in url):
                rutas.append(url_periodico + url)
        else:
            print('Periodico no encontrado')
    
    try:
        shutil.rmtree('/tmp/' + periodico, ignore_errors=True)
    except:
        print('Error al borrar el directorio ' + periodico)
        
    os.mkdir('/tmp/' + periodico)
    
    for i in range(5):
        extension = rutas[i].split('/')[-1].split('.')[-1]
        urllib.request.urlretrieve(rutas[i], '/tmp/'+ periodico + '/' + str(uuid.uuid4()) + '.' + extension)
